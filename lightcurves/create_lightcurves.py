import numpy as np
from gwemlightcurves.KNModels import KNTable
from astropy.table import Table, Column
from gwemlightcurves import lightcurve_utils
import os


def Me2017_model_modified(m1, mb1, c1, m2, mb2, c2, beta, kappa_r):
    tini = 0.00
    tmax = 50.0
    dt = 0.01

    samples = {}
    samples["tini"] = tini
    samples["tmax"] = tmax
    samples["dt"] = dt
    samples["m1"] = m1
    samples["mb1"] = mb1
    samples["c1"] = c1
    samples["m2"] = m2
    samples["mb2"] = mb2
    samples["c2"] = c2
    samples["beta"] = beta
    samples["kappa_r"] = kappa_r

    model = "Me2017"

    return model, samples

def DiUj2017_model_ejecta_modified(mej, vej, th, ph):
    tini = 0.00
    tmax = 50.0
    dt = 0.01

    vave = 0.267
    vmin = 0.00
    kappa = 10.0
    eps = 1.58 * (10**10)
    alp = 1.2
    eth = 0.5

    flgbct = 1

    samples = {}
    samples["tini"] = tini
    samples["tmax"] = tmax
    samples["dt"] = dt
    samples["mej"] = mej
    samples["vej"] = vej
    samples["th"] = th
    samples["ph"] = ph
    samples["vmin"] = vmin
    samples["kappa"] = kappa
    samples["eps"] = eps
    samples["alp"] = alp
    samples["eth"] = eth
    samples["flgbct"] = flgbct

    model = "DiUj2017"

    t = Table()
    for key in samples.keys():
        val = samples[key]
        t.add_column(Column(data=[val], name=key))
    samples = t

    return model, samples

print ('generating samples..')

#Kanchan: modifying mej value from 1e-1 to 1e-2
model, samples = DiUj2017_model_ejecta_modified(mej=1e-2, vej=0.1, th=0.3, ph=90)

t = KNTable.model(model, samples)

t = lightcurve_utils.calc_peak_mags(t)
t = lightcurve_utils.interpolate_mags_lbol(t)

print ('initiating lightcurves directory..')
os.makedirs("lightcurves", exist_ok=True)
for key in t.keys():
    if key.startswith("mag_"):
        print(key)
        np.savetxt(
            f"lightcurves/lightcurve_{key}.dat",
            np.array([t["t"].value[0], t[key].value[0]]).T,
        )
                                                                                                          88,5          Bot

