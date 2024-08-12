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

'''
    Effective volumes
    energy in GeV
    veff in km^3 sr (include your own factor of 4 pi)
'''
veff = {
    # this comes from Martin's simulation of a single station
    "SMT_Martin" : {
        "energy" : 10**np.array([16.0, 16.5, 
                             17.0, 17.5, 
                             18.0, 18.5, 
                             19.0, 19.5, 
                             20.0])/1E9,
        "veff": np.array([1.108e-03, 3.112e-02,
                          2.030e-01, 7.434e-01,
                          2.642e+00, 7.020e+00,
                          1.664e+01, 4.001e+01,
                          7.632e+01
                          ])
    },
    # this comes from Aishwary's estimates
    "SMT" : {
        "energy" : 10**np.array([17.0, 18.0, 
                             19.0, 20.0])/1E9,
        "veff": np.array([0.001988, 0.3073,
                          2.227, 14.29,
                          ])
    },
    # this comes from the RNO-G white paper
    # the figure directly digitized is the 35 station array in km^3
    # so we need to divide by 35, and add the 4 pi to get "per station"
    "PA": {
        "energy" : 10**np.array([16.0, 16.5, 
                             17.0, 17.5, 
                             18.0, 18.5, 
                             19.0, 19.5, 
                             20.0])/1E9,
        "veff": np.array([1.4207e-2, 1.3884e-1,
                          9.2790e-1, 3.6940e+0,
                          1.0233e+1, 2.4266e+1,
                          5.0992e+1, 9.8288e+1,
                          1.8621e+2
                          ])/35*np.pi*4
    }
}

pa_efficiency = {
    "energy" : 10**np.array([16.00, 16.500, 17.000,
                             17.500, 18.000, 18.500, 
                             19.000, 19.500, 20.000]),
    "efficiency" : np.array([0.45, 0.50735344, 0.53663997, 
                             0.63748401, 0.73041842, 0.79534748,
                             0.84517992, 0.83591592, 0.83591592])
    }

a23_efficiency = {
    "energy" : 10**np.array([16.00, 16.500, 17.000,
                             17.500, 18.000, 18.500, 
                             19.000, 19.500, 20.000]),
    "efficiency" : np.array([0.05, 0.1595, 0.2426, 
                             0.3067, 0.3724, 0.4452,
                             0.5187, 0.5453, 0.5747])
    }

data_ara_200 = {
    "arasim": {
        "energy": 10**np.array([16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0]) / 1e9,
        "veff": np.array([1.105E-1, 5.195E-1, 1.826E+0, 5.259E+0,
                          1.106E+1, 2.077E+1, 3.431E+1, 5.073E+1])
    }
}



def compute_exposure(additional_years, uptime_fraction = 0.45):
    '''
    additional_years
        How many additional years of data do you want to assume we take?

    uptime_assumption
        How much of the year do you think we will be on and taking data?
        Currently, we're achieving "SBC on" about 70% of the time
        The digitizers are on about 45% of the time
        "Good science" data is more like 30%


    returns

    energies in GeV
    exposure in km^3 sr years (sorry about the years...)
    '''


    # the exposure with the 2/4 SMT so far
    existing_livetime = 0.
    for k in available_livetime.keys():
        existing_livetime += available_livetime[k]
    print(existing_livetime)

    veff_smt = veff["SMT"]["veff"]
    exposure_smt = veff_smt * existing_livetime # * a23_efficiency["efficiency"]

    # the exposure with the PA trigger we will have
    future_livetime = additional_years * uptime_fraction

    veff_pa = veff["PA"]["veff"]
    exposure_pa = veff_pa * future_livetime

    # return veff["PA"]["energy"], exposure_smt + exposure_pa
    return veff["SMT"]["energy"], exposure_smt


