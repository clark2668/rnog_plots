import numpy as np

'''
List of accumulated livetime *in years*
'''

days_to_years = 1./365.

hilo_livetime = 3073.61 # days from 2021-2024
hilo_livetime = hilo_livetime * days_to_years
pa_livetime = 1165.12 # data we took in 2025
pa_livetime = pa_livetime * days_to_years

# 165 days of new livetime for every existing station
# 90 days of new livetime for every *new* station

'''
    Effective volumes
    energy in GeV
    veff in km^3 sr
'''
steradian = 4 * np.pi
veff = {
    "hilo" : {
        "energy" : 10**np.array([16.0, 16.5, 17.0, 17.5, 
                                 18.0, 18.5, 19.0, 19.5, 
                                 20.0, 20.5, 21.0])/1E9,
        "veff": np.array([5.07161981726308E-05, 6.10821140578283E-04, 4.40799764153179E-03, 2.63275189228185E-02, 
                          1.07360092009057E-01, 3.47613010768232E-01, 9.69779744928276E-01, 2.64979577734877E+00,
                          4.92403818243416E+00, 9.64007611958286E+00, 1.48490226038343E+01])*steradian
    },
    "pa" : {
        "energy" : 10**np.array([16.0, 16.5, 17.0, 17.5, 
                                 18.0, 18.5, 19.0, 19.5, 
                                 20.0, 20.5, 21.0])/1E9,
        "veff": np.array([1.44618202588028E-04, 1.34056609936527E-03, 1.02062260137554E-02, 5.19510413328914E-02,
                          1.84524121183946E-01, 5.47931496040555E-01, 1.45005147650225E+00, 3.66604275817319E+00,
                          6.56525389717405E+00, 1.21510388635034E+01, 1.74386690726701E+01])*steradian
    },
    "didaq" : {
        "energy" : 10**np.array([16.0, 16.5, 17.0, 17.5, 
                                 18.0, 18.5, 19.0, 19.5, 
                                 20.0, 20.5, 21.0])/1E9,
        "veff": np.array([1.91569204795727E-04, 1.70543857875877E-03, 1.31053401998672E-02, 6.47628025379279E-02,
                          2.23106135771391E-01, 6.48090738676717E-01, 1.69018734228923E+00, 4.1741662485854E+00,
                          7.38586175454399E+00, 1.34065202354636E+01, 1.8733492307088E+01])*steradian
    },
}
