import numpy as np

'''
List of accumulated livetime *in years*
'''
days_to_years = 1./365.
available_livetime = {
    "s11" : 375,
    "s12" : 161,
    "s13" : 333,
    "s14" : 0,
    "s21" : 346,
    "s22" : 176,
    "s23" : 317,
    "s24" : 323
}
for l in available_livetime:
    available_livetime[l] = available_livetime[l]*days_to_years

existing_livetime = 0.
for k in available_livetime.keys():
    existing_livetime += available_livetime[k]



'''
    Effective volumes
    energy in GeV
    veff in km^3 sr
'''
steradian = 4 * np.pi
veff = {
    "wp" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([4.24E-03, 2.76E-02, 1.14E-01, 3.05E-01, 6.56E-01, 1.15E+00, 1.70E+00, 2.15E+00])*steradian
    },
    "deep_high_low_1Hz" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([3.896e-04,  3.842e-03,  2.220e-02,  9.383e-02,  2.907e-01, 7.191e-01,  1.965e+00,  3.486e+00])*steradian
    },
    "simple_threshold_2" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([3.586e-03,  2.327e-02,  8.989e-02,  2.771e-01,  7.419e-01,1.541e+00,  3.338e+00,  5.682e+00])*steradian
    },
    "simple_threshold_2.5" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([2.284e-03,  1.679e-02,  6.545e-02,  2.190e-01,  6.244e-01, 1.311e+00,  2.894e+00,  5.113e+00])*steradian
    },
    "simple_threshold_2.5_downsampled" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([1.605e-03,  1.168e-02,  5.175e-02,  1.876e-01,  5.345e-01, 1.171e+00,  2.689e+00,  4.774e+00])*steradian
    },
    "simple_threshold_3_downsampled" : {
        "energy" : 10**np.array([16.50, 17.00, 17.50, 18.00, 18.50, 19.00, 19.50, 20])/1E9,
        "veff": np.array([1.146e-03,  9.014e-03,  4.066e-02,  1.569e-01,  4.493e-01, 1.037e+00,  2.417e+00,  4.413e+00])*steradian
    },

}
