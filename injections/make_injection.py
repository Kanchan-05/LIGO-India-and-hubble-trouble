#!/usr/bin/env python

import sys
import bilby
import numpy as np
from astropy.cosmology import Planck18
from pycbc.inject import InjectionSet
from pycbc.io import FieldArray
import argparse, logging

# parser = argparse.ArgumentParser(description=__doc__)
# group = parser.add_mutually_exclusive_group(required=True)

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number-of-injections', metavar='N',
                    help='Input the number of injections', type=int)
parser.add_argument("-o", "--output-file",required=True,
                    help="File to store the injection parameters" )
parser.add_argument('--gps-start-time', type=float,required=True,
                   help='Input gps start time')
parser.add_argument('--gps-end-time',type=float,required=True,
                   help='Input gps end time')
args = parser.parse_args()


def gaussian_mass_function(N, mass_function):
    if mass_function == "farrow":
        mu = 1.33
        sigma = 0.09
    elif mass_function == "kiziltan":
        mu = 1.33
        sigma = 0.22

    m1 = np.random.normal(mu, sigma, N)
    m2 = np.random.normal(mu, sigma, N)
    idxs = np.where(m2 > m1)
    m1[idxs], m2[idxs] = m2[idxs], m1[idxs]
    return m1, m2


dtype = [('mass1', float), ('mass2', float),
         ('spin1z', float), ('spin2z', float),
         ('tc', float),
         ('ra', float), ('dec', float),
         ('distance', float),
         ('inclination', float),
         ('approximant', 'S32'),('amp_order','int_4s')]


static_params = {'f_lower': 15.,
                 'f_ref': 15.,
                 'taper': 'TAPER_STARTEND',
                 'coa_phase': 0.,
                 'polarization': 0.}


NSAMPLES = args.number_of_injections
samples_dict = FieldArray(NSAMPLES, dtype=dtype)

m1s, m2s = gaussian_mass_function(NSAMPLES, mass_function="farrow")
redshift = bilby.gw.prior.UniformSourceFrame(name="redshift", minimum=0.005, maximum=0.2).sample(NSAMPLES)
samples_dict["mass1"] = m1s * (1 + redshift)
samples_dict["mass2"] = m2s * (1 + redshift)
samples_dict["distance"] = Planck18.luminosity_distance(redshift).value
samples_dict["ra"] = bilby.core.prior.Uniform(name='ra', minimum=0, maximum=2 * np.pi).sample(NSAMPLES)
samples_dict["dec"] = bilby.core.prior.Cosine(name='dec').sample(NSAMPLES)
samples_dict["inclination"] = bilby.core.prior.Sine(name='theta_jn').sample(NSAMPLES)
samples_dict["tc"] = bilby.core.prior.Uniform(minimum=args.gps_start_time, maximum=args.gps_end_time, boundary='periodic').sample(NSAMPLES)

#samples_dict["dec"] = bilby.core.prior.Uniform(name='dec', minimum=0, maximum=2 * np.pi).sample(NSAMPLES)
# samples_dict["polarization"] = bilby.core.prior.Uniform(name='psi', minimum=0, maximum=np.pi, boundary='periodic').sample(NSAMPLES)
# samples_dict["coa_phase"] = bilby.core.prior.Uniform(name='phase', minimum=0, maximum=2 * np.pi, boundary='periodic').sample(NSAMPLES)

samples_dict["spin1z"] = bilby.core.prior.Uniform(minimum=0, maximum=0.05).sample(NSAMPLES)
samples_dict["spin2z"] = bilby.core.prior.Uniform(minimum=0, maximum=0.05).sample(NSAMPLES)

#SpinTaylorT2threePointFivePN
#SpinTaylorT4
samples_dict['approximant'] = ['SpinTaylorT4']
# samples_dict['taper'] = ['TAPER_STARTEND']
samples_dict['amp_order'] = ['-1']
# samples_dict['f_lower'] = ['14']
# samples_dict['f_ref'] = ['14']

InjectionSet.write(args.output_file, samples_dict, static_args=static_params,
                   injtype='cbc', cmd=" ".join(sys.argv))
                                                                          
