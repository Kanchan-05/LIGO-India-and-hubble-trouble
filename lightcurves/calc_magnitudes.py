import numpy as np
import glob
import pandas
from scipy.interpolate import interp1d
import sys

"Aditya's code modified Kanchan"

def abs_to_app_mag(abs_mag, distance):
    return abs_mag + 5 * np.log10(distance) - 5


def app_to_abs_mag(app_mag, distance):
    return app_mag - 5 * np.log10(distance) + 5



interped_lightcurves = {}
for fname in glob.glob("lightcurves/*"):
    bandname = fname.split(".dat")[0][-1]
    print('band name = ',bandname)
    t, mag = np.loadtxt(fname, unpack=True)
    t = t * 24 * 60 * 60
    interped_lightcurves[bandname] = interp1d(t, mag)
for tag in ["with_LI", "without_LI"]:
    print ('calculating for results ', tag)
    injections = pandas.read_csv(
        f"results_plot/pycbc_run_results_for_94injections_{tag}.txt", delimiter=" "
    )

    for telescope in ['ztf','lsst','winter']:
        print('Calculating for', telescope, '...')

        # Read the electromagnetic counterpart data
        df_em = pandas.read_csv(f"results_schedule/{telescope}_output_{tag.lower()}.txt", delimiter=", ")
#         bands = df_em["Band"].dropna().unique()  # Drop NaN and get unique bands
        bands = df_em["Band"].unique()

        # Process for each band
        for bandname in bands:
            if str(bandname) == "nan":
                continue
            else:
                print('For band:', bandname)

                # Filter df_em for the current band
                df_em_band = df_em[df_em["Band"] == bandname]

                # Filter df_em_band based on InjectionTime matching with injections
                inj_main = np.array([np.round(float(i),2) for i in injections["tc"]])
                inj_check =  np.array([np.round(float(i),2) for i in df_em_band["InjectionTime"]])

                poscheck = np.array([i in inj_check for i in inj_main ])

                # Continue only if there are matching entries
		if not df_em_band.empty:

                    # Calculate magnitudes
                    abs_mags = interped_lightcurves[bandname](df_em_band["TimeDifference(seconds)"])
                    app_mags = abs_to_app_mag(abs_mags, injections["distance"][poscheck] * 1e6)

                    # Assign magnitudes
                    df_em_band[f"ApparentMagnitude_{bandname}"] = app_mags
                    df_em_band[f"AbsoluteMagnitude_{bandname}"] = abs_mags

             # Save df_em_band to a text file
            output_filename = f"results_schedule/{telescope}_output_{tag.lower()}_{bandname}_incl_mags.txt"
            df_em_band.to_csv(output_filename, index=False)
            print(f"DataFrame for {bandname} band saved as '{output_filename}'")


