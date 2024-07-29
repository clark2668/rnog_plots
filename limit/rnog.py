import numpy as np

'''
List of accumulated livetime
'''
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


'''
    Effective volumes
    energy in eV
    veff in km^3 sr (include your own factor of 4 pi)
'''
veff = {
    "SMT" : {
        "energy" : 10**np.array([16.0, 16.5, 
                             17.0, 17.5, 
                             18.0, 18.5, 
                             19.0, 19.5, 
                             20.0]),
        "veff" : np.array([3.1765e-3, 3.7186e-2,
                           2.2075e-1, 1.1656e+0,
                           3.8534e+0, 1.0198e+1,
                           2.1860e+1, 4.7970e+1,
                           9.1468e+1
                           ])
    },
    "PA": {
        "energy": np.array([]),
        "veff": np.array([])
    }
}

def compute_exposure():

    # the exposure with the 2/4 SMT so far
    existing_livetime = 0.
    for k in available_livetime.keys():
        existing_livetime += available_livetime[k]

    veff_smt = veff["SMT"]["veff"]
    exposure_smt = veff_smt * existing_livetime


    # the exposure with the PA trigger we will have


compute_exposure()
