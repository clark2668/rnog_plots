import numpy as np
import units
import json
import os
import pickle
from io import StringIO

# ==============
energyBinsPerDecade = 1.
plotUnitsEnergy = units.eV
plotUnitsEnergyStr = "eV"
plotUnitsFlux = units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
flavorRatio = 1. 
DIFFUSE = True
livetime = 10 * units.year
plotUnitsLivetime = '5 years or 100 days'
#=================

# GRAND white paper,
# numerical values, Bustamante
GRAND_energy = np.array(([48192296.5, 67644231.1, 94947581.6, 133271428.0, 
                          187063990.0, 262568931.0, 368550053.0, 517308507.0,
                          726110577.0, 1019191760.0, 1430569790.0, 2007992980.0,
                          2818482440.0, 3956111070.0, 5552922590.0, 7794257720.0,
                          10940266600.0, 15356104100.0, 21554313200.0, 30254315500.0,
                          42465913900.0, 59606499400.0, 83665567300.0, 117435636000.0, 
                          164836371000.0]))#, 231369543000.0, 324757606000.0, 455840043000.0,
                          # 639831498000.0, 898087721000.0, 1260584320000.0, 1769396010000.0,
                          # 2483580190000.0, 3486031680000.0, 4893104280000.0, 6868115880000.0,
                          # 9640304610000.0, 13531436400000.0, 18993151900000.0, 26659388600000.0]))

GRAND_energy *= units.GeV

GRAND_10k = np.array(([8.41513361e-08, 7.38147706e-08, 5.69225180e-08, 3.46647934e-08,
                       1.95651137e-08, 1.40651565e-08, 1.25782087e-08, 1.24621707e-08,
                       1.31123151e-08, 1.45812119e-08, 1.65528260e-08, 1.91930521e-08,
                       2.31554429e-08, 2.87477813e-08, 3.55164030e-08, 4.42563884e-08,
                       5.63965197e-08, 7.45183330e-08, 1.01159657e-07, 1.39040439e-07,
                       1.98526677e-07, 2.61742251e-07, 3.40870828e-07, 4.82745531e-07,
                       6.55876763e-07]))# 9.07706655e-07, 1.67125879e-06, 1.76142511e-05,
                       #2.55022320e-04, 1.88371074e-03, 6.71431813e-03, 1.14286198e-02,
                       #1.14294614e-02, 1.72447830e-02, 7.48579143e-02, 3.31883351e-01,
                       #8.57786094e-01, 1.24824516e+00, 1.42294586e+00, 1.80135089e+00]))

GRAND_10k *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
# GRAND_10k /= 2 #halfdecade bins
GRAND_10k *= energyBinsPerDecade
# The expected sensitivities for GRAND are given for 3 years, rescaling them to given years
GRAND_10k *= 3 * units.year / livetime
GRAND_10k *= flavorRatio

GRAND_200k = np.array(([4.26219753e-09, 3.58147708e-09, 2.75670137e-09, 1.85254042e-09,
                        1.13825106e-09, 7.70141315e-10, 6.51758930e-10, 6.35878242e-10,
                        6.69261628e-10, 7.37439217e-10, 8.38784832e-10, 9.81688683e-10,
                        1.18493794e-09, 1.45699379e-09, 1.80867621e-09, 2.26948852e-09,
                        2.91952068e-09, 3.86790849e-09, 5.24530715e-09, 7.31211288e-09,
                        9.98848945e-09, 1.33523293e-08, 1.80893102e-08, 2.46582187e-08,
                        3.41054825e-08,]))# 5.39140368e-08, 3.36553610e-07, 4.57179717e-06,
                        #3.59391218e-05, 1.47550853e-04, 3.33777479e-04, 4.92873322e-04,
                        #6.68381070e-04, 1.72553598e-03, 7.06643413e-03, 2.10754560e-02,
                        #4.06319101e-02, 5.88162853e-02, 7.45423652e-02]))# 8.83700084e-02]))

GRAND_200k *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
# GRAND_200k /= 2 #halfdecade bins
GRAND_200k *= energyBinsPerDecade
# The expected sensitivities for GRAND are given for 3 years, rescaling them to 10 years
GRAND_200k *= 3 * units.year / livetime
# convert to nutau
GRAND_200k *= flavorRatio

# RADAR proposed from https://arxiv.org/pdf/1710.02883.pdf

# Radar = np.array(([
#     (1.525e+01, 6.870e-09, 3.430e-07),
#     (1.575e+01, 9.797e-10, 3.113e-08),
#     (1.625e+01, 4.728e-09, 1.928e-07),
#     (1.675e+01, 6.359e-09, 3.706e-07),
#     (1.725e+01, 9.128e-09, 8.517e-07),
#     (1.775e+01, 1.619e-08, 1.835e-06),
#     (1.825e+01, 2.995e-08, 2.766e-06),
#     (1.875e+01, 5.562e-08, 8.253e-06),
#     (1.925e+01, 1.072e-07, 1.849e-05)]))

# RADAR updated April 2022. Private communication with S. Prohira
# all flavor, ten year, full-decade and PRELIMARY.
Radar = np.array(([
    (15.25, 1.01085e-08),
    (15.75, 9.10238e-09),
    (16.25, 5.20686e-09),
    (16.75, 3.38319e-09),
    (17.25, 1.60787e-09),
    (17.75, 8.37262e-10),
    (18.25, 6.42559e-10),
    (18.75, 7.67415e-10),
    (19.25, 1.18121e-09),
    (19.75, 2.1649e-09)
]))

Radar[:, 0] = 10 ** Radar[:, 0] * units.eV
Radar[:, 1] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
Radar[:, 1] /= 1.0  # fulldecade bins
Radar[:, 1] *= energyBinsPerDecade
Radar[:, 1] *= 10. * units.year / livetime
Radar[:, 1] *= 1.0 * flavorRatio
#Radar[:, 2] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
#Radar[:, 2] /= 2  # halfdecade bins
#Radar[:, 2] *= energyBinsPerDecade
#Radar[:, 2] *= 10. * units.year / livetime

# BEACON high frequency and low frequency design, 3 years, half decade, all flavor
BEACON_energy = np.array([1.00000000e+07, 3.16227766e+07, 1.00000000e+08, 3.16227766e+08, 1.00000000e+09, 3.16227766e+09, 1.00000000e+10, 3.16227766e+10, 1.00000000e+11, 3.16227766e+11, 1.00000000e+12])
BEACON_LF_100 = np.array([5.68408199e-05, 1.63484517e-06, 1.58905043e-07, 3.46887030e-08, 1.84151378e-08, 2.56663885e-08, 5.69651628e-08, 1.61897437e-07, 5.22561508e-07, 1.84652554e-06, 6.84893692e-06])
BEACON_LF_1000 = np.array([5.68408199e-06, 1.63484517e-07, 1.58905043e-08, 3.46887030e-09, 1.84151378e-09, 2.56663885e-09, 5.69651628e-09, 1.61897437e-08, 5.22561508e-08, 1.84652554e-07, 6.84893692e-07])
BEACON_HF_100 = np.array([1.01459826e-05, 5.25910446e-07, 8.16365020e-08, 2.90054480e-08, 2.57153151e-08, 4.39470678e-08, 1.06058213e-07, 3.10497544e-07, 1.01472755e-06, 3.57230670e-06, 1.35441025e-05])
BEACON_HF_1000 = np.array([1.01459826e-06, 5.25910446e-08, 8.16365020e-09, 2.90054480e-09,2.57153151e-09, 4.39470678e-09, 1.06058213e-08, 3.10497544e-08, 1.01472755e-07, 3.57230670e-07, 1.35441025e-06])
BEACON_LF_100 *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
BEACON_LF_100 /= 2 * energyBinsPerDecade# half-decade energy bins
BEACON_LF_100 *= 3 * units.year / livetime
BEACON_LF_100 *= flavorRatio
BEACON_LF_1000 *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
BEACON_LF_1000 /= 2 # half-decade energy bins
BEACON_LF_1000 *= 3 * units.year / livetime
BEACON_LF_1000 *= flavorRatio
BEACON_HF_100 *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
BEACON_HF_100 /= 2 # half-decade energy bins
BEACON_HF_100 *= 3 * units.year / livetime
BEACON_HF_100 *= flavorRatio
BEACON_HF_1000 *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
BEACON_HF_1000 /= 2 * energyBinsPerDecade# half-decade energy bins
BEACON_HF_1000 *= 3 * units.year / livetime
BEACON_HF_1000 *= flavorRatio
BEACON_energy *= units.GeV

# TAMBO
# full decade, tau flavor sensitivyt, 5 years
tambo = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data',  "tambo-E2-sensitivity.csv"), delimiter=',',)
TAMBO_energy = tambo.T[:,0] * units.GeV
TAMBO = tambo.T[:,1] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
TAMBO *= energyBinsPerDecade
TAMBO *= 10 * units.year / livetime
TAMBO *= 3.0 * flavorRatio

# Trinity 
# full decade, all-flavor

# 2020 Snwomass panel, 10 year observations, x 3
# Trinity = np.array([993956.7715863951, 1.2502400423112297e-8,
# 1586785.1338202823, 5.229816945008047e-9,
# 2641445.9055291982, 2.924140098417545e-9,
# 5434882.455108475, 1.634363883974857e-9,
# 9844817.973931914, 1.0563830278866512e-9,
# 17453307.682168357, 8.186380954246969e-10,
# 36661171.1186107, 6.042617845827115e-10,
# 62282364.213070355, 5.349352063152472e-10,
# 103577008.37568721, 5.09220702311963e-10,
# 158217689.11633533, 5.471375763446372e-10,
# 268658836.961115, 6.320030667872033e-10,
# 410294919.6965676, 7.663565155139216e-10,
# 613463411.0357083, 9.293057691963835e-10,
# 917072897.588413, 1.2413760281283111e-9,
# 1342317446.5001554, 1.5799950109964071e-9,
# 2006733781.104083, 2.060137471032793e-9,
# 3949516324.0568304, 3.503271836228786e-9,
# 5779611206.184445, 5.0320781397714825e-9,
# 9704276186.426899, 8.254475641443274e-9,
# 14657298065.435661, 1.2903385937289992e-8,
# 24869746172.245544, 2.2485281782959967e-8])
# Trinity_energy = Trinity[::2] * units.GeV
# Trinity_E2F = Trinity[1::2] * units.GeV * units.cm**-2 * units.second ** -1 * units.sr ** -1 
# Trinity_E2F *= energyBinsPerDecade
# Trinity_E2F *= 10 * units.year / livetime
# Trinity_E2F *= flavorRatio

# 2021 Snowmass nutau 
# tau flavor, 5 yearas, full decade 18 telescopes
#Trinity = np.array([9.81E+04,        8.10E-08,
#6.31E+05,        1.64E-08,        
#1.00E+06,        7.23E-09,
#1.58E+06,        3.39E-09,
#2.51E+06,        1.89E-09,
#3.98E+06,        1.27E-09,
#6.31E+06,        9.10E-10,
#1.00E+07,        6.71E-10,
#1.58E+07,        5.15E-10,
#2.51E+07,        4.30E-10,
#3.98E+07,        3.70E-10,
#6.31E+07,        3.36E-10,
#1.00E+08,        3.39E-10,
#1.58E+08,        3.53E-10,
#2.51E+08,        4.19E-10,
#3.98E+08,        5.03E-10,
#6.31E+08,        6.37E-10,
#1.00E+09,        8.58E-10,
#1.58E+09,        1.14E-09,
#2.51E+09,        1.62E-09,
#3.98E+09,        2.36E-09,
#6.31E+09,        3.68E-09,
#1.00E+10,        5.56E-09,
#1.58E+10,        9.19E-09,
#2.51E+10,        1.52E-08])
#Trinity sensitivity, all flavor, 18 telescopes for 10 years, Nepomuk email 6/27/2022
# Nu energy [GeV] and All flavor sensitivity E**2*phi [GeV/cm2/s/sr]
Trinity = np.array([1e+06, 1.2e-08,
1.58489e+06,5.3e-09,
2.51189e+06,  3.15e-09,
3.98107e+06,  2.08e-09,
6.30957e+06,  1.44e-09,
1e+07,  1.05e-09,
1.58489e+07,  8.4e-10,
2.51189e+07,  6.87e-10,
3.98107e+07,  5.77e-10,
6.30957e+07,  5.23e-10,
1e+08,  5.07e-10,
1.58489e+08,  5.3e-10,
2.51189e+08,  6.29e-10,
3.98107e+08,  7.53e-10,
6.30957e+08,  9.53e-10,
1e+09,  1.29e-09,
1.58489e+09,  1.71e-09,
2.51189e+09,  2.43e-09,
3.98107e+09,  3.53e-09,
6.30957e+09,  5.5e-09,
1e+10,  8.3e-09,
1.58489e+10,  1.38e-08,
2.51189e+10,  2.28e-08])

        
Trinity_energy = Trinity[::2] * units.GeV
Trinity_E2F = Trinity[1::2] * units.GeV * units.cm**-2 * units.second ** -1 * units.sr ** -1 
Trinity_E2F *= energyBinsPerDecade
Trinity_E2F *= 10 * units.year / livetime
Trinity_E2F *= flavorRatio * 1.0 # all-flavor


#################
#
# LOFAR, projected for SKA https://arxiv.org/pdf/1903.08472.pdf
# 200 hour observations
# all flavor

lofar = np.array(([1.0312831606721869e+21, 40256749.91527908,
1.3503140378698722e+21, 19512934.22635966,
1.5873361110102054e+21, 7568891.123391609,
3.376199441111333e+21, 1345960.324155367,
6.804181968927093e+21, 689778.5379387672,
1.5273778503907e+22, 467040.8184503117,
3.818913304781847e+22, 395161.107144985,
9.548455102782186e+22, 417799.33263875253,
2.387406771860637e+23, 467040.8184503117,
5.969249509970703e+23, 583618.4760920019,
1.4141701702890154e+24, 771075.2692535555,
3.5358593665351545e+24, 1018742.7149936829,
8.84073340152499e+24, 1345960.324155367,
1.984535457805787e+25, 1880154.542858146,
9.47520530280647e+25, 3668733.1930182246,
])) 

lofar_energy = lofar[::2] * units.eV
lofar_flux = lofar[1::2] * units.eV * units.m**-2 * units.second ** -1 * units.sr **-1
lofar_flux *= energyBinsPerDecade /  np.log(10) # binned in energy decases
lofar_flux *= flavorRatio

# --------------------------------------------------------------------
# Published data and limits

# IceCube
# log (E^2 * Phi [GeV cm^02 s^-1 sr^-1]) : log (E [Gev])
# Phys Rev D 98 062003 (2018)
# Numbers private correspondence Shigeru Yoshida
ice_cube_limit = np.array(([
    #(6.199999125, -7.698484687),
    #(6.299999496, -8.162876678),
    #(6.400000617, -8.11395291),
    (6.500000321, -8.063634144),
    (6.599999814, -8.004841781),
    (6.699999798, -7.944960162),
    (6.799999763, -7.924197388),
    (6.899999872, -7.899315263),
    (7.299999496, -7.730561153),
    (7.699999798, -7.670680637),
    (8.100001583, -7.683379711),
    (8.500000321, -7.748746801),
    (8.899999872, -7.703060304),
    (9.299999496, -7.512907553),
    (9.699999798, -7.370926525),
    (10.10000158, -7.134626026),
    (10.50000032, -6.926516638),
    (10.89999987, -6.576523031)
]))

ice_cube_limit[:, 0] = 10 ** ice_cube_limit[:, 0] * units.GeV
ice_cube_limit[:, 1] = 10 ** ice_cube_limit[:, 1] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ice_cube_limit[:, 1] *= energyBinsPerDecade

# Fig. 2 from PoS ICRC2017 (2018) 981
# IceCube preliminary, per flavor flux
# E (GeV); E^2 dN/dE (GeV cm^-2 s-1 sr-1); yerror down; yerror up

# HESE 6 years
# ice_cube_hese = np.array(([
#
#     (6.526e+04,  2.248e-08,  9.96e-9,  1.123e-8),
#     (1.409e+05,  2.692e-08,  5.91e-9,  7.56e-9),
#     (3.041e+05,  7.631e-09,  3.746e-9, 4.61e-9),
#     (6.644e+05,  2.022e-09,  7.03e-10, 0.),
#     (1.434e+06,  5.205e-09,  3.183e-9,  4.57e-9),
#     (3.096e+06,  4.347e-09,  3.142e-9,  5.428e-9),
#     (6.684e+06,  1.544e-09,  5.37e-10, 0.),
#     (1.46e+07,  4.063e-09,   1.353e-9, 0.),
#     (3.153e+07,  6.093e-09,  2.03e-9,  0.),
#     (6.806e+07,  1.046e-08,  3.641e-9, 0.)
# ]))
# ice_cube_hese[:, 0] = ice_cube_hese[:, 0] * units.GeV
# ice_cube_hese[:, 1] = ice_cube_hese[:, 1] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
# ice_cube_hese[:, 1] *= 3
# ice_cube_hese[:, 2] = ice_cube_hese[:, 2] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
# ice_cube_hese[:, 2] *=  3
# ice_cube_hese[:, 3] = ice_cube_hese[:, 3] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
# ice_cube_hese[:, 3] *= 3

# HESE 8 years
# log(E (GeV)); log(E^2 dN/dE (GeV cm^-2 s-1 sr-1)); format x y -dy +dy
ice_cube_hese = np.array(([
(4.78516, 	 -7.63256, 		0.223256, 	0.167442),
(5.10938, 	 -7.66977, 		0.139535, 	0.102326),
(5.42969, 	 -8.36744, 		0.930233, 	0.297674),
(5.75391, 	 -8.51628, 		0.2, 	0.),
(6.07813, 	 -8.38605, 		0.604651, 	0.288372),
(6.39844, 	 -8.35814, 		0.455814, 	0.334884),
(6.72266, 	 -9.0, 		0.2 , 	0)
]))

# get uncertainties in right order
ice_cube_hese[:, 2] = 10 ** ice_cube_hese[:, 1] - 10 ** (ice_cube_hese[:, 1] - ice_cube_hese[:, 2])
ice_cube_hese[:, 3] = 10 ** (ice_cube_hese[:, 1] + ice_cube_hese[:, 3]) - 10 ** ice_cube_hese[:, 1]

ice_cube_hese[:, 0] = 10 ** ice_cube_hese[:, 0] * units.GeV
ice_cube_hese[:, 1] = 10 ** ice_cube_hese[:, 1] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ice_cube_hese[:, 1] *= 3
ice_cube_hese[:, 1] *= flavorRatio

ice_cube_hese[:, 2] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ice_cube_hese[:, 2] *= 3
ice_cube_hese[:, 2] *= flavorRatio

ice_cube_hese[:, 3] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ice_cube_hese[:, 3] *= 3
ice_cube_hese[:, 3] *= flavorRatio

print("Ice Cube HESE")
print(ice_cube_hese[:,1]/plotUnitsFlux)

# Ice cube
# ice cube nu_mu data points 9.5 years analysis
nu_mu_data = np.array([[4.64588, -7.69107, -7.87555, -7.5549, ],
                       [5.44266, -7.95022, -8.06881, -7.85359, ],
                       [6.25755, -8.51245, -8.8287, -8.29283],
                       [7.29276, -8.40264, 0, 0]])
# nu_mu_data[:, 2] = 10 ** nu_mu_data[:, 1] - 10 ** (nu_mu_data[:, 1] - nu_mu_data[:, 2])
# nu_mu_data[:, 3] = 10 ** (nu_mu_data[:, 1] + nu_mu_data[:, 3]) - 10 ** nu_mu_data[:, 1]
# convert energy to correct units
nu_mu_data[:, 1:] = (10 ** nu_mu_data[:, 1:]) * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)  
nu_mu_data[:, 2] = np.abs(nu_mu_data[:, 1] - nu_mu_data[:, 2])
nu_mu_data[:, 3] = np.abs(nu_mu_data[:, 1] - nu_mu_data[:, 3])

nu_mu_data[-1, 3] = 0
nu_mu_data[-1, 2] = 2e-9 * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
nu_mu_data[:, 0] = 10 ** nu_mu_data[:, 0] * units.GeV

# ApJ slope=-2.13, offset=0.9 (https://arxiv.org/pdf/1607.08006.pdf)
# ICR2017 slope=-2.19, offset=1.01 (https://pos.sissa.it/301/1005/)
# ICRC2019 slope=2.28, offset=1.44
# 9.5 years analysis 2.37+0.08-0.09, offset 1.36 + 0.24 - 0.25, Astrophysical normalization @ 100TeV: 1.36 × 10−8GeV−1cm−2s−1sr−1

# using ICRC2019 results for now which are the last published results. No Piecewise-Unfolding was already done at that time, so we don't have "data points".

# using IceCueb 2021 numu https://arxiv.org/pdf/2111.10299.pdf
nu_mu_slope = -2.37
nu_mu_slope_up = -(2.28 + 0.09)
nu_mu_slope_down = -(2.28 - 0.09)
nu_mu_offset = (1.44) * 3.0 * flavorRatio
nu_mu_offset_up = (1.44 + 0.25)  * 3.0 * flavorRatio
nu_mu_offset_down = (1.44 - 0.26)* 3.0 * flavorRatio
nu_mu_show_data_points = False


def ice_cube_nu_fit(energy, slope=nu_mu_slope, offset=nu_mu_offset):
    flux = offset * (energy / (100 * units.TeV)) ** slope * 1e-18 * \
        (units.GeV ** -1 * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
    return flux


def get_ice_cube_mu_range():
    energy = np.arange(2.5e4, 5e6, 1e5) * units.GeV
#     upper = np.maximum(ice_cube_nu_fit(energy, offset=0.9, slope=-2.), ice_cube_nu_fit(energy, offset=1.2, slope=-2.13)) # APJ
#     upper = np.maximum(ice_cube_nu_fit(energy, offset=1.01, slope=-2.09),
#                     ice_cube_nu_fit(energy, offset=1.27, slope=-2.19), ice_cube_nu_fit(energy, offset=1.27, slope=-2.09))  # ICRC
    slope = nu_mu_slope
    slope_up = nu_mu_slope_up
    slope_down = nu_mu_slope_down
    offset_up = nu_mu_offset_up
    offset_down = nu_mu_offset_down
    upper = np.maximum(ice_cube_nu_fit(energy, offset=offset_up, slope=slope_up),
#                     ice_cube_nu_fit(energy, offset=offset_up, slope=slope),
                    ice_cube_nu_fit(energy, offset=offset_up, slope=slope_down))  # 9.5 years
    upper *= energy ** 2
#     lower = np.minimum(ice_cube_nu_fit(energy, offset=0.9, slope=-2.26),
#                        ice_cube_nu_fit(energy, offset=0.63, slope=-2.13)) #ApJ
#     lower = np.minimum(ice_cube_nu_fit(energy, offset=1.01, slope=-2.29),
#                        ice_cube_nu_fit(energy, offset=0.78, slope=-2.19))  # ICRC
    lower = np.minimum(ice_cube_nu_fit(energy, offset=offset_down, slope=slope_up),
#                        ice_cube_nu_fit(energy, offset=offset_down, slope=slope),
                       ice_cube_nu_fit(energy, offset=offset_down, slope=slope_down))  # 9.5 years
    lower *= energy ** 2
    return energy, upper, lower


def get_ice_cube_hese_range():
    energy = np.arange(1e5, 5e6, 1e5) * units.GeV
    upper = np.maximum(ice_cube_nu_fit(energy, offset=2.46, slope=-2.63),
                       ice_cube_nu_fit(energy, offset=2.76, slope=-2.92))
    upper *= energy ** 2
    lower = np.minimum(ice_cube_nu_fit(energy, offset=2.46, slope=-3.25),
                       ice_cube_nu_fit(energy, offset=2.16, slope=-2.92))
    lower *= energy ** 2
    return energy, upper, lower

# 2020 Cascades PRL https://arxiv.org/pdf/2011.03545.pdf
def get_ice_cube_hese_range():
    energy = np.arange(25e3, 2.8e6, 1e5) * units.GeV
    slope=-2.87
    slope_err_high= 0.21
    slope_err_low = 0.19 
    offset = 6.37 * flavorRatio
    offset_high_err = 1.1 * flavorRatio
    offset_low_err = 1.2 * flavorRatio
    upper = np.maximum(ice_cube_nu_fit(energy, offset=offset+offset_high_err, slope=slope+slope_err_high),
                       ice_cube_nu_fit(energy, offset=offset+offset_high_err, slope=slope))
    upper = np.maximum(upper,
                       ice_cube_nu_fit(energy, offset=offset, slope=slope+slope_err_high))

    upper *= energy ** 2
    lower = np.minimum(ice_cube_nu_fit(energy, offset=offset-offset_low_err, slope=slope-slope_err_low),
                       ice_cube_nu_fit(energy, offset=offset-offset_low_err, slope=slope))
    lower = np.minimum(lower,
                       ice_cube_nu_fit(energy, offset=offset, slope=slope-slope_err_low))
    lower *= energy ** 2
    return energy, upper, lower

# IceCube Glashow
# Paper: https://doi.org/10.1038/s41586-021-03256-1
# Dataset: https://doi.org/10.21234/gr2021
# https://icecube.wisc.edu/data-releases/2021/03/icecube-data-for-the-first-glashow-resonance-candidate/
# NB: the csv file gives per-flavor, but we want all flavor, so multiply by 3


i3_glashow_data = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'data', "icecube_glashow.csv"),
    skip_header=2, delimiter=',', names=['E_min', 'E_max', 'y', 'y_lower', 'y_upper'])
i3_glashow_emin = i3_glashow_data['E_min'] * units.GeV / plotUnitsEnergy
i3_glashow_emax = i3_glashow_data['E_max'] * units.GeV / plotUnitsEnergy
i3_glashow_y = 3. * i3_glashow_data['y'] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1) * 1E-8 / plotUnitsFlux * flavorRatio
i3_glashow_y_lower = 3. * i3_glashow_data['y_lower'] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1) * 1E-8 / plotUnitsFlux * flavorRatio
i3_glashow_y_upper = 3. * i3_glashow_data['y_upper'] * (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1) * 1E-8 / plotUnitsFlux * flavorRatio


#####
# IC Butterfly curves
#####

def ic_butterfly(energy, source="hans"):
    ic_contour = get_ic_contour(source="hans")
    print(ic_contour)
    flux = (
        energy ** 2
        * 1e-18
	* (
            ic_contour[:, 1][:, None] * 3.
            * (energy[None, :] / 1e5) ** (-ic_contour[:, 0][:, None])
        )
    )
    return flux.min(axis=0), flux.max(axis=0)
    
def get_ic_contour(source="hans"):
    if source == "hans":
        dat =  np.loadtxt(
            StringIO(
                """2.508 1.271
                2.502 1.276
                2.492 1.284
                2.476 1.304
                2.468 1.316
                2.459 1.332
                2.449 1.357
                2.443 1.374
                2.436 1.398
                2.427 1.439
                2.427 1.441
                2.421 1.480
                2.417 1.520
                2.414 1.561
                2.413 1.602
                2.413 1.643
                2.413 1.684
                2.415 1.724
                2.418 1.765
                2.422 1.806
                2.426 1.847
                2.427 1.851
                2.432 1.888
                2.439 1.929
                2.443 1.953
                2.447 1.969
                2.458 2.010
                2.459 2.013
                2.476 2.047
                2.481 2.051
                2.492 2.058
                2.508 2.053
                2.510 2.051
                2.524 2.033
                2.536 2.010
                2.541 2.001
                2.553 1.969
                2.557 1.956
                2.565 1.929
                2.573 1.899
                2.576 1.888
                2.585 1.847
                2.590 1.826
                2.594 1.806
                2.601 1.765
                2.606 1.733
                2.607 1.724
                2.613 1.684
                2.618 1.643
                2.622 1.604
                2.623 1.602
                2.625 1.561
                2.627 1.520
                2.627 1.480
                2.625 1.439
                2.622 1.422
                2.619 1.398
                2.610 1.357
                2.606 1.345
                2.595 1.316
                2.590 1.306
                2.573 1.283
                2.565 1.276
                2.557 1.270
                2.541 1.264
                2.524 1.265
                2.508 1.271
               
            """

            
            )
        )
        return np.array(dat) 


def _load_pickle(pickle_file):
        """                                                                                                                                                                                                 
        Returns the content of a pickle file.                                                                                                                                                               
        Compatible with python2 AND python3 pickle files.                                                                                                                                                   
        """
        try:
            with open(pickle_file, 'rb') as f:
                pickle_data = pickle.load(f)
        except UnicodeDecodeError as e:
            with open(pickle_file, 'rb') as f:
                pickle_data = pickle.load(f, encoding='latin1')
        except Exception as e:
            print('Unable to load data ', pickle_file, ':', e)
            raise
        return pickle_data

# Cascades contour 2020        
IC_Cascades2020_en = np.logspace(np.log10(16000), np.log10(2600000), 101) * units.GeV
IC_Cascades2020_flux =   ic_butterfly(IC_Cascades2020_en / units.GeV, "hans")                  

# Muon neutrinos contour Icecube 2021                                                                                                                                                                                          
diffusenumu = _load_pickle("./data/DiffuseNuMu_9.5y_E2_envelope.pickle")                                                                              
SinglePL_68envelope = diffusenumu["68pc"]      
IC_numu2021_en = SinglePL_68envelope["energies"] * units.GeV 
IC_numu2021_flux_min = 3*SinglePL_68envelope["E2_envelope"][0] * plotUnitsFlux
IC_numu2021_flux_max = 3*SinglePL_68envelope["E2_envelope"][1] * plotUnitsFlux 

'''
Regarding ANITA Limits
# ====================================================

ANITA uses a *super* unusual differential limit bin width.

A limit is generally given by:

     E dN                           Sup
---------------  =   -----------------------------------
dE dA dOmega dt       T  * Efficiency * Aeff * BinWidth

For most experiments, BinWidth is transformed into log space for convenience:
               BinWidth = LN(10) * dlog10(E)
And then a decade wide binning is assumed: dlog10(E) = 1

But, in ANITA, they set BinWidth = 4 (!!!!!!!!!!!!!!)
See eq D1 of the ANITA-III paper.
"... the factor Delta = 4 follows the normalization convention..."

This means that the ANITA limit is a factor of LN(10)/4 too strong
when naively compared to other experiments, e.g. IceCube.
So, below, we multply by by 4/LN(10) to fix the bin width.

'''

# ANITA I - III
# https://arxiv.org/abs/1803.02719
# Phys. Rev. D 98, 022001 (2018)
anita_limit = np.array(([
    (9.94e17, 3.79e-14 * 9.94e17 / 1e9),
    (2.37e18, 2.15e-15 * 2.37e18 / 1e9),
    (5.19e18, 2.33e-16 * 5.19e18 / 1e9),
    (1.10e19, 3.64e-17 * 1.10e19 / 1e9),
    (3.55e19, 4.45e-18 * 3.55e19 / 1e9),
    (1.11e20, 9.22e-19 * 1.11e20 / 1e9),
    (4.18e20, 2.97e-19 * 4.18e20 / 1e9),
    (9.70e20, 1.62e-19 * 9.70e20 / 1e9)
]))
anita_limit[:, 0] *= units.eV
anita_limit[:, 1] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
anita_limit[:, 1] *= (4 / np.log(10))  # see discussion above about strange anita binning
anita_limit[:, 1] *= energyBinsPerDecade
anita_limit[:, 1] *= flavorRatio

# ANITA I - IV
# https://arxiv.org/abs/1902.04005
# Phys. Rev. D 99, 122001 (2019)
# NB: The ANITA I-IV is indeed weaker than the ANITA I-III limit (!!)
# The reason is not understood, but can be seen easily comparing the two limits side-by-side
anita_i_iv_limit = np.array(([
    (1.000e+18, 3.1098E+04),
    (3.162e+18, 3.7069E+03),
    (1.000e+19, 6.0475E+02),
    (3.162e+19, 2.5019E+02),
    (1.000e+20, 1.4476E+02),
    (3.162e+20, 1.5519E+02),
    (1.000e+21, 2.0658E+02)
]))
anita_i_iv_limit[:, 0] *= units.eV
anita_i_iv_limit[:, 1] *= (units.eV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
anita_i_iv_limit[:, 1] *= (4 / np.log(10))  # see discussion above about strange anita binning
anita_i_iv_limit[:, 1] *= energyBinsPerDecade
anita_i_iv_limit[:, 1] *= flavorRatio

# From 2020 PUEO whitepaper 
# 30 day livetime
#PUEO Proposal Values (First Column: Energy [log10(E/eV)], Second Column: Acceptance [km^2 str])
pueo_30 = np.array(([
	(1e+17,1.40661e-13),
	(1.20226e+17,7.72532e-14),
	(1.44544e+17,4.33634e-14),
	(1.7378e+17,2.49001e-14),
    (2.0893e+17,1.46405e-14),
    (2.51189e+17,8.82258e-15),
    (3.01995e+17,5.45414e-15),
    (3.63078e+17,3.38518e-15),
    (4.36516e+17,2.03077e-15),
    (5.24807e+17,9.90641e-16),
    (6.30957e+17,3.93959e-16),
    (7.58578e+17,1.50751e-16),
    (9.12011e+17,6.36039e-17),
	(1.09648e+18,3.0993e-17),
	(1.31826e+18,1.74503e-17),
	(1.58489e+18,1.11695e-17),
	(1.90546e+18,7.98744e-18),
    (2.29087e+18,6.18675e-18),
    (2.75423e+18,5.03289e-18),
    (3.31131e+18,4.17669e-18),
    (3.98107e+18,3.4715e-18),
    (4.7863e+18,2.88097e-18),
    (5.7544e+18,2.38973e-18),
    (6.91831e+18,1.98369e-18),
    (8.31764e+18,1.64999e-18),
	(1e+19,1.37677e-18),
	(1.20226e+19,1.15279e-18),
	(1.44544e+19,9.67092e-19),
	(1.7378e+19,8.10987e-19),
    (2.0893e+19,6.78235e-19),
    (2.51189e+19,5.63874e-19),
    (3.01995e+19,4.65052e-19),
    (3.63078e+19,3.79995e-19),
    (4.36516e+19,3.08359e-19),
    (5.24807e+19,2.49666e-19),
    (6.30957e+19,2.02641e-19),
    (7.58578e+19,1.65641e-19),
    (9.12011e+19,1.37238e-19),
	(1.09648e+20,1.15678e-19),
	(1.31826e+20,9.92882e-20),
	(1.58489e+20,8.6598e-20),
	(1.90546e+20,7.65754e-20),
    (2.29087e+20,6.84952e-20),
    (2.75423e+20,6.18367e-20),
    (3.31131e+20,5.63007e-20),
    (3.98107e+20,5.14816e-20),
    (4.7863e+20,4.71717e-20),
    (5.7544e+20,4.32138e-20),
    (6.91831e+20,3.94904e-20),
    (8.31764e+20,3.59175e-20),
	(1e+21,3.24404e-20)
	]))

#100 day livetime
#PUEO Proposal Values (First Column: Energy [log10(E/eV)], Second Column: Acceptance [km^2 str])
pueo_100 = np.array(([
	(1e+17,4.21982e-14),
    (1.20226e+17,2.31759e-14),
    (1.44544e+17,1.3009e-14),
	(1.7378e+17,7.47003e-15),
	(2.0893e+17,4.39215e-15),
	(2.51189e+17,2.64677e-15),
	(3.01995e+17,1.63624e-15),
	(3.63078e+17,1.01555e-15),
	(4.36516e+17,6.09231e-16),
	(5.24807e+17,2.97192e-16),
	(6.30957e+17,1.18188e-16),
	(7.58578e+17,4.52252e-17),
	(9.12011e+17,1.90812e-17),
	(1.09648e+18,9.29791e-18),
	(1.31826e+18,5.2351e-18),
	(1.58489e+18,3.35084e-18),
	(1.90546e+18,2.39623e-18),
	(2.29087e+18,1.85602e-18),
	(2.75423e+18,1.50987e-18),
	(3.31131e+18,1.25301e-18),
	(3.98107e+18,1.04145e-18),
	(4.7863e+18,8.64291e-19),
	(5.7544e+18,7.16919e-19),
	(6.91831e+18,5.95108e-19),
	(8.31764e+18,4.94998e-19),
	(1e+19,4.13032e-19),
	(1.20226e+19,3.45836e-19),
	(1.44544e+19,2.90128e-19),
	(1.7378e+19,2.43296e-19),
	(2.0893e+19,2.0347e-19),
	(2.51189e+19,1.69162e-19),
	(3.01995e+19,1.39515e-19),
	(3.63078e+19,1.13998e-19),
	(4.36516e+19,9.25076e-20),
	(5.24807e+19,7.48999e-20),
	(6.30957e+19,6.07923e-20),
	(7.58578e+19,4.96923e-20),
	(9.12011e+19,4.11715e-20),
	(1.09648e+20,3.47034e-20),
	(1.31826e+20,2.97864e-20),
	(1.58489e+20,2.59794e-20),
	(1.90546e+20,2.29726e-20),
	(2.29087e+20,2.05485e-20),
	(2.75423e+20,1.8551e-20),
	(3.31131e+20,1.68902e-20),
	(3.98107e+20,1.54445e-20),
	(4.7863e+20,1.41515e-20),
	(5.7544e+20,1.29641e-20),
	(6.91831e+20,1.18471e-20),
	(8.31764e+20,1.07753e-20),
	(1e+21,9.73213e-21)
]))
PUEO30_energy = pueo_30[:,0] * units.eV
PUEO30 = pueo_30[:,1] 
PUEO30 *= PUEO30_energy/units.GeV * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
PUEO30 *= (4 / np.log(10))  # see discussion above about anita binning
PUEO30 *= 2.44 # convert from single event sensitivty to 90% confidence level
PUEO30 *= energyBinsPerDecade
PUEO30 *= flavorRatio

PUEO100_energy = pueo_100[:,0] * units.eV
PUEO100 = pueo_100[:,1] 
PUEO100 *= PUEO100_energy/units.GeV * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
PUEO100 *= (4 / np.log(10))  # see discussion above about anita binning
PUEO100 *= 2.44 # convert from single event sensitivty to 90% confidence level
PUEO100 *= energyBinsPerDecade
PUEO100 *= flavorRatio

''' POEMMA Private communication, Austin Cummings, John Krizmanic
half-decade, all-flavor, 5 years livetime
 ====================================================
'''
poemma = np.array(([
    (	7.05E+00	,	2.90735021022595E-03	),
    (	7.08989898989899E+00	,	2.689298446204E-04	),
    (	7.12979797979798E+00	,	4.92316664007849E-05	),
    (	7.16969696969697E+00	,	1.65140528885579E-05	),
    (	7.20959595959596E+00	,	7.69668457203465E-06	),
    (	7.24949494949495E+00	,	4.73733289218856E-06	),
    (	7.28939393939394E+00	,	3.03432810508337E-06	),
    (	7.32929292929293E+00	,	2.21926949078092E-06	),
    (	7.36919191919192E+00	,	1.75087576470389E-06	),
    (	7.40909090909091E+00	,	1.39497968668861E-06	),
    (	7.4489898989899E+00	,	1.09963501801102E-06	),
    (	7.48888888888889E+00	,	8.87989784441239E-07	),
    (	7.52878787878788E+00	,	7.46024224513819E-07	),
    (	7.56868686868687E+00	,	6.45966290206983E-07	),
    (	7.60858585858586E+00	,	5.63612750526781E-07	),
    (	7.64848484848485E+00	,	4.87785882829145E-07	),
    (	7.68838383838384E+00	,	4.28826960699721E-07	),
    (	7.72828282828283E+00	,	3.74093340159383E-07	),
    (	7.76818181818182E+00	,	3.35156211173734E-07	),
    (	7.80808080808081E+00	,	3.09176980051536E-07	),
    (	7.8479797979798E+00	,	2.83658354268724E-07	),
    (	7.88787878787879E+00	,	2.63338766294396E-07	),
    (	7.92777777777778E+00	,	2.42730183402238E-07	),
    (	7.96767676767677E+00	,	2.24874324537016E-07	),
    (	8.00757575757576E+00	,	2.10268205755708E-07	),
    (	8.04747474747475E+00	,	1.98364517003677E-07	),
    (	8.08737373737374E+00	,	1.8900132281437E-07	),
    (	8.12727272727273E+00	,	1.79404970454481E-07	),
    (	8.16717171717172E+00	,	1.70996189174827E-07	),
    (	8.20707070707071E+00	,	1.6409672302318E-07	),
    (	8.2469696969697E+00	,	1.58047704297749E-07	),
    (	8.28686868686869E+00	,	1.53397012091967E-07	),
    (	8.32676767676768E+00	,	1.49126052907826E-07	),
    (	8.36666666666667E+00	,	1.45684830920374E-07	),
    (	8.40656565656566E+00	,	1.42872576791667E-07	),
    (	8.44646464646465E+00	,	1.39445685130987E-07	),
    (	8.48636363636364E+00	,	1.36975766634826E-07	),
    (	8.52626262626263E+00	,	1.3491787326118E-07	),
    (	8.56616161616162E+00	,	1.33529655871197E-07	),
    (	8.60606060606061E+00	,	1.32601274482493E-07	),
    (	8.6459595959596E+00	,	1.30991846823899E-07	),
    (	8.68585858585859E+00	,	1.3015404960621E-07	),
    (	8.72575757575758E+00	,	1.2898544358158E-07	),
    (	8.76565656565657E+00	,	1.28502025351658E-07	),
    (	8.80555555555556E+00	,	1.29171003972217E-07	),
    (	8.84545454545455E+00	,	1.29220151707535E-07	),
    (	8.88535353535353E+00	,	1.2992731914698E-07	),
    (	8.92525252525252E+00	,	1.30365894248351E-07	),
    (	8.96515151515151E+00	,	1.30973133255436E-07	),
    (	9.0050505050505E+00	,	1.32048880576793E-07	),
    (	9.0449494949495E+00	,	1.32870244993269E-07	),
    (	9.08484848484849E+00	,	1.3432226260578E-07	),
    (	9.12474747474748E+00	,	1.35438591845954E-07	),
    (	9.16464646464647E+00	,	1.36660433570365E-07	),
    (	9.20454545454545E+00	,	1.38433624571811E-07	),
    (	9.24444444444444E+00	,	1.40398925781994E-07	),
    (	9.28434343434343E+00	,	1.43033214312108E-07	),
    (	9.32424242424242E+00	,	1.45543738463946E-07	),
    (	9.36414141414141E+00	,	1.48277598476823E-07	),
    (	9.4040404040404E+00	,	1.51566329055903E-07	),
    (	9.4439393939394E+00	,	1.54436677873785E-07	),
    (	9.48383838383839E+00	,	1.58021502868446E-07	),
    (	9.52373737373738E+00	,	1.62301676771116E-07	),
    (	9.56363636363636E+00	,	1.67291268673429E-07	),
    (	9.60353535353535E+00	,	1.72941883864386E-07	),
    (	9.64343434343434E+00	,	1.78934107094116E-07	),
    (	9.68333333333333E+00	,	1.85643332635231E-07	),
    (	9.72323232323232E+00	,	1.9298970753465E-07	),
    (	9.76313131313131E+00	,	2.01246191029005E-07	),
    (	9.8030303030303E+00	,	2.10810836838484E-07	),
    (	9.84292929292929E+00	,	2.2183095457267E-07	),
    (	9.88282828282828E+00	,	2.3378643761797E-07	),
    (	9.92272727272727E+00	,	2.46862584391508E-07	),
    (	9.96262626262626E+00	,	2.61101818818855E-07	),
    (	1.00025252525253E+01	,	2.76521010733848E-07	),
    (	1.00424242424242E+01	,	2.9370970587025E-07	),
    (	1.00823232323232E+01	,	3.12261200780351E-07	),
    (	1.01222222222222E+01	,	3.32599897238887E-07	),
    (	1.01621212121212E+01	,	3.54805535054783E-07	),
    (	1.02020202020202E+01	,	3.78732486804182E-07	),
    (	1.02419191919192E+01	,	4.04008597790994E-07	),
    (	1.02818181818182E+01	,	4.31239522664107E-07	),
    (	1.03217171717172E+01	,	4.62767341157508E-07	),
    (	1.03616161616162E+01	,	4.98751746737976E-07	),
    (	1.04015151515152E+01	,	5.37740155176102E-07	),
    (	1.04414141414141E+01	,	5.81447465090403E-07	),
    (	1.04813131313131E+01	,	6.28820826694368E-07	),
    (	1.05212121212121E+01	,	6.81192992053853E-07	),
    (	1.05611111111111E+01	,	7.38992028512535E-07	),
    (	1.06010101010101E+01	,	8.01802666772865E-07	),
    (	1.06409090909091E+01	,	8.70989186585003E-07	),
    (	1.06808080808081E+01	,	9.46221292569195E-07	),
    (	1.07207070707071E+01	,	1.02759533681609E-06	),
    (	1.07606060606061E+01	,	1.11732737791095E-06	),
    (	1.08005050505051E+01	,	1.2198710792862E-06	),
    (	1.0840404040404E+01	,	1.32225430761947E-06	),
    (	1.0880303030303E+01	,	1.43341076639373E-06	),
    (	1.0920202020202E+01	,	1.55360643746832E-06	),
    (	1.0960101010101E+01	,	1.68357686032341E-06	),
    (	1.1E+01	,	1.82465998171989E-06	)
]))

poemma_f = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "POEMMA-90CLperDecade-AllFlavor+TauOnlyFlavor-5year-Sensitivity-GQRS.txt"))

poemma_360 = np.array(([    
    (7.05E+00,	2.42279184185496E-04),
    (7.08989898989899E+00,	2.24108203850333E-05),
    (7.12979797979798E+00,	4.10263886673207E-06),
    (7.16969696969697E+00,	1.37617107404649E-06),
    (7.20959595959596E+00,	6.41390381002887E-07),
    (7.24949494949495E+00,	3.94777741015714E-07),
    (7.28939393939394E+00,	2.52860675423614E-07),
    (7.32929292929293E+00,	1.84939124231743E-07),
    (7.36919191919192E+00,	1.45906313725324E-07),
    (7.40909090909091E+00,	1.16248307224051E-07),
    (7.4489898989899E+00,	9.16362515009181E-08),
    (7.48888888888889E+00,	7.39991487034366E-08),
    (7.52878787878788E+00,	6.21686853761516E-08),
    (7.56868686868687E+00,	5.38305241839152E-08),
    (7.60858585858586E+00,	4.6967729210565E-08),
    (7.64848484848485E+00,	4.06488235690954E-08),
    (7.68838383838384E+00,	3.57355800583101E-08),
    (7.72828282828283E+00,	3.11744450132819E-08),
    (7.76818181818182E+00,	2.79296842644778E-08),
    (7.80808080808081E+00,	2.5764748337628E-08),
    (7.8479797979798E+00,	2.36381961890603E-08),
    (7.88787878787879E+00,	2.19448971911996E-08),
    (7.92777777777778E+00,	2.02275152835198E-08),
    (7.96767676767677E+00,	1.87395270447513E-08),
    (8.00757575757576E+00,	1.75223504796423E-08),
    (8.04747474747475E+00,	1.65303764169731E-08),
    (8.08737373737374E+00,	1.57501102345308E-08),
    (8.12727272727273E+00,	1.495041420454E-08),
    (8.16717171717172E+00,	1.42496824312356E-08),
    (8.20707070707071E+00,	1.36747269185983E-08),
    (8.2469696969697E+00,	1.31706420248124E-08),
    (8.28686868686869E+00,	1.27830843409973E-08),
    (8.32676767676768E+00,	1.24271710756522E-08),
    (8.36666666666667E+00,	1.21404025766978E-08),
    (8.40656565656566E+00,	1.19060480659722E-08),
    (8.44646464646465E+00,	1.16204737609156E-08),
    (8.48636363636364E+00,	1.14146472195688E-08),
    (8.52626262626263E+00,	1.12431561050983E-08),
    (8.56616161616162E+00,	1.11274713225997E-08),
    (8.60606060606061E+00,	1.10501062068744E-08),
    (8.6459595959596E+00,	1.09159872353249E-08),
    (8.68585858585859E+00,	1.08461708005175E-08),
    (8.72575757575758E+00,	1.07487869651317E-08),
    (8.76565656565657E+00,	1.07085021126382E-08),
    (8.80555555555556E+00,	1.07642503310181E-08),
    (8.84545454545455E+00,	1.07683459756279E-08),
    (8.88535353535353E+00,	1.08272765955817E-08),
    (8.92525252525252E+00,	1.0863824520696E-08),
    (8.96515151515151E+00,	1.09144277712863E-08),
    (9.0050505050505E+00,	1.10040733813994E-08),
    (9.0449494949495E+00,	1.10725204161058E-08),
    (9.08484848484849E+00,	1.1193521883815E-08),
    (9.12474747474748E+00,	1.12865493204961E-08),
    (9.16464646464647E+00,	1.13883694641971E-08),
    (9.20454545454545E+00,	1.15361353809843E-08),
    (9.24444444444444E+00,	1.16999104818328E-08),
    (9.28434343434343E+00,	1.1919434526009E-08),
    (9.32424242424242E+00,	1.21286448719955E-08),
    (9.36414141414141E+00,	1.23564665397353E-08),
    (9.4040404040404E+00,	1.26305274213252E-08),
    (9.4439393939394E+00,	1.28697231561488E-08),
    (9.48383838383839E+00,	1.31684585723705E-08),
    (9.52373737373738E+00,	1.35251397309264E-08),
    (9.56363636363636E+00,	1.39409390561191E-08),
    (9.60353535353535E+00,	1.44118236553655E-08),
    (9.64343434343434E+00,	1.49111755911764E-08),
    (9.68333333333333E+00,	1.54702777196026E-08),
    (9.72323232323232E+00,	1.60824756278875E-08),
    (9.76313131313131E+00,	1.67705159190838E-08),
    (9.8030303030303E+00,	1.75675697365403E-08),
    (9.84292929292929E+00,	1.84859128810559E-08),
    (9.88282828282828E+00,	1.94822031348309E-08),
    (9.92272727272727E+00,	2.05718820326257E-08),
    (9.96262626262626E+00,	2.17584849015712E-08),
    (1.00025252525253E+01,	2.3043417561154E-08),
    (1.00424242424242E+01,	2.44758088225208E-08),
    (1.00823232323232E+01,	2.60217667316959E-08),
    (1.01222222222222E+01,	2.77166581032406E-08),
    (1.01621212121212E+01,	2.95671279212319E-08),
    (1.02020202020202E+01,	3.15610405670152E-08),
    (1.02419191919192E+01,	3.36673831492495E-08),
    (1.02818181818182E+01,	3.59366268886756E-08),
    (1.03217171717172E+01,	3.8563945096459E-08),
    (1.03616161616162E+01,	4.1562645561498E-08),
    (1.04015151515152E+01,	4.48116795980085E-08),
    (1.04414141414141E+01,	4.84539554242003E-08),
    (1.04813131313131E+01,	5.2401735557864E-08),
    (1.05212121212121E+01,	5.67660826711544E-08),
    (1.05611111111111E+01,	6.15826690427112E-08),
    (1.06010101010101E+01,	6.68168888977387E-08),
    (1.06409090909091E+01,	7.25824322154169E-08),
    (1.06808080808081E+01,	7.88517743807662E-08),
    (1.07207070707071E+01,	8.56329447346739E-08),
    (1.07606060606061E+01,	9.31106148259125E-08),
    (1.08005050505051E+01,	1.0165592327385E-07),
    (1.0840404040404E+01,	1.10187858968289E-07),
    (1.0880303030303E+01,	1.19450897199478E-07),
    (1.0920202020202E+01,	1.2946720312236E-07),
    (1.0960101010101E+01,	1.40298071693618E-07),
    (1.1E+01,	1.52054998476658E-07),
]))

POEMMA_energy = pow(10, poemma[:,0]) * units.GeV
POEMMA = poemma[:,1] 
POEMMA /= 2 # half decade binning
POEMMA *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
POEMMA *= energyBinsPerDecade
POEMMA *= flavorRatio
#POEMMA *= 5. * units.year / livetime#, 5 years is as realistic as it could be


POEMMA_fluor_energy = pow(10, poemma_f[:,0]) * units.GeV
POEMMA_fluor_flux = poemma_f[:,2]
POEMMA_fluor_flux *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
POEMMA_fluor_flux *= energyBinsPerDecade
POEMMA_fluor_flux *= flavorRatio
#POEMMA_fluor_flux *= 5. * units.year / livetime #, 5 years is as realistic as it could be


POEMMA360_energy = pow(10, poemma_360[:,0]) * units.GeV
POEMMA360 = poemma_360[:,1] 
POEMMA360 *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)

POEMMA360 *= energyBinsPerDecade
POEMMA360 *= flavorRatio
#POEMMA360 *= 5. * units.year / livetime#, 5 years is as realistic as it could be



''' EUSO-SBP Private communication, Austin Cummings, John Krizmanic
half-decade, all-flavor, 100 days flighttime
 ====================================================
'''

euso_sbp = np.array(([
    (	6E+00	,	1.73818624724762E-02),
    (	6.05050505050505E+00	,	1.57151656494517E-02),
    (	6.1010101010101E+00	,	1.47446401869234E-02),
    (	6.15151515151515E+00	,	1.32348175895553E-02),
    (	6.2020202020202E+00	,	1.22152149206776E-02),
    (	6.25252525252525E+00	,	9.1675421273974E-03),
    (	6.3030303030303E+00	,	7.40943155041521E-03),
    (	6.35353535353535E+00	,	4.3036161798476E-03),
    (	6.4040404040404E+00	,	3.24568026688684E-03),
    (	6.45454545454546E+00	,	2.64373236026653E-03),
    (	6.5050505050505E+00	,	2.15798298570899E-03),
    (	6.55555555555556E+00	,	1.25226279422307E-03),
    (	6.60606060606061E+00	,	9.45952891138652E-04),
    (	6.65656565656566E+00	,	7.89718557483611E-04),
    (	6.70707070707071E+00	,	7.04207528065654E-04),
    (	6.75757575757576E+00	,	6.30459365451928E-04),
    (	6.80808080808081E+00	,	5.0188659640424E-04),
    (	6.85858585858586E+00	,	3.78742516484314E-04),
    (	6.90909090909091E+00	,	3.19873471128958E-04),
    (	6.95959595959596E+00	,	2.86429365826541E-04),
    (	7.01010101010101E+00	,	2.54081761919253E-04),
    (	7.06060606060606E+00	,	2.02304769656553E-04),
    (	7.11111111111111E+00	,	1.75842224516638E-04),
    (	7.16161616161616E+00	,	1.60661436749998E-04),
    (	7.21212121212121E+00	,	1.47161550224007E-04),
    (	7.26262626262626E+00	,	1.28427678018472E-04),
    (	7.31313131313131E+00	,	1.13733436653826E-04),
    (	7.36363636363636E+00	,	9.72748535765333E-05),
    (	7.41414141414142E+00	,	8.81760790880594E-05),
    (	7.46464646464646E+00	,	8.29318855275562E-05),
    (	7.51515151515152E+00	,	7.62052722094722E-05),
    (	7.56565656565656E+00	,	6.60501223357074E-05),
    (	7.61616161616162E+00	,	6.03628745663242E-05),
    (	7.66666666666667E+00	,	5.70898284285807E-05),
    (	7.71717171717172E+00	,	5.53415788319151E-05),
    (	7.76767676767677E+00	,	5.35697288520356E-05),
    (	7.81818181818182E+00	,	4.98085569646396E-05),
    (	7.86868686868687E+00	,	4.57533195863105E-05),
    (	7.91919191919192E+00	,	4.34372188216257E-05),
    (	7.96969696969697E+00	,	4.22032355277208E-05),
    (	8.02020202020202E+00	,	4.0561311223328E-05),
    (	8.07070707070707E+00	,	3.83629147654289E-05),
    (	8.12121212121212E+00	,	3.71909718169546E-05),
    (	8.17171717171717E+00	,	3.67178155615811E-05),
    (	8.22222222222222E+00	,	3.60336016950733E-05),
    (	8.27272727272727E+00	,	3.51198382038725E-05),
    (	8.32323232323232E+00	,	3.40691114729732E-05),
    (	8.37373737373737E+00	,	3.29243830558277E-05),
    (	8.42424242424243E+00	,	3.24345467836403E-05),
    (	8.47474747474747E+00	,	3.24268084963092E-05),
    (	8.52525252525253E+00	,	3.20707150030823E-05),
    (	8.57575757575757E+00	,	3.15386277547255E-05),
    (	8.62626262626263E+00	,	3.14884597409206E-05),
    (	8.67676767676768E+00	,	3.18188577360963E-05),
    (	8.72727272727273E+00	,	3.24677113470161E-05),
    (	8.77777777777778E+00	,	3.31671483440473E-05),
    (	8.82828282828283E+00	,	3.35442379684058E-05),
    (	8.87878787878788E+00	,	3.39518642016398E-05),
    (	8.92929292929293E+00	,	3.46814872450742E-05),
    (	8.97979797979798E+00	,	3.57047257332901E-05),
    (	9.03030303030303E+00	,	3.68144292475296E-05),
    (	9.08080808080808E+00	,	3.80883120214164E-05),
    (	9.13131313131313E+00	,	3.96188368388541E-05),
    (	9.18181818181818E+00	,	4.14171157615307E-05),
    (	9.23232323232323E+00	,	4.33884015993497E-05),
    (	9.28282828282828E+00	,	4.55958424674642E-05),
    (	9.33333333333333E+00	,	4.80389328752548E-05),
    (	9.38383838383838E+00	,	5.07694760978383E-05),
    (	9.43434343434343E+00	,	5.37863490449494E-05),
    (	9.48484848484848E+00	,	5.71403251597115E-05),
    (	9.53535353535354E+00	,	6.11536334902871E-05),
    (	9.58585858585858E+00	,	6.57149644539193E-05),
    (	9.63636363636364E+00	,	7.06992922280885E-05),
    (	9.68686868686869E+00	,	7.61775322923385E-05),
    (	9.73737373737374E+00	,	8.21396155657618E-05),
    (	9.78787878787879E+00	,	8.99247280539903E-05),
    (	9.83838383838384E+00	,	9.81300265267783E-05),
    (	9.88888888888889E+00	,	1.06895565789062E-04),
    (	9.93939393939394E+00	,	1.16350221828627E-04),
    (	9.98989898989899E+00	,	1.26703646689401E-04),
    (	1.0040404040404E+01	,	1.39232396586222E-04),
    (	1.00909090909091E+01	,	1.53378175072805E-04),
    (	1.01414141414141E+01	,	1.68599803895352E-04),
    (	1.01919191919192E+01	,	1.85317242946823E-04),
    (	1.02424242424242E+01	,	2.03103501468379E-04),
    (	1.02929292929293E+01	,	2.2259008969412E-04),
    (	1.03434343434343E+01	,	2.44632479794072E-04),
    (	1.03939393939394E+01	,	2.69078559509134E-04),
    (	1.04444444444444E+01	,	2.95335546266571E-04),
    (	1.04949494949495E+01	,	3.24214051942955E-04),
    (	1.05454545454545E+01	,	3.54738490792712E-04),
    (	1.05959595959596E+01	,	3.88237957775603E-04),
    (	1.06464646464646E+01	,	4.24567192547631E-04),
    (	1.06969696969697E+01	,	4.64564873729969E-04),
    (	1.07474747474747E+01	,	5.06851194170193E-04),
    (	1.07979797979798E+01	,	5.6005891857061E-04),
    (	1.08484848484848E+01	,	6.13430871527095E-04),
    (	1.08989898989899E+01	,	6.72043897708836E-04),
    (	1.09494949494949E+01	,	7.33033604356799E-04),
    (	1.1E+01	,	8.00151928912973E-04),
]))

EUSOSPB_energy = pow(10,euso_sbp[:,0]) * units.GeV
EUSOSPB= euso_sbp[:,1] 
EUSOSPB *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
EUSOSPB /= 2 # half decade binning
EUSOSPB *= energyBinsPerDecade
EUSOSPB *= flavorRatio
EUSOSPB *= 5. * units.year / livetime

'''
Regarding Auger Limits
# ====================================================

Auger publishes a limit that only applies to a single flavor, tau neutrinos
Because this is a limit, multiplying by 3 makes the limit *weaker*.
Also, Auger uses half decade bins.
The net factor of 3/2, on a log-log plot, leaves the limit's position (relative
to other experiments) essentially unchanged.

'''

# Auger neutrino limit (2019, 14.7 years)
# JCAP 10 (2019) 022
# https://arxiv.org/abs/1906.07422
auger_limit = np.array(([
    (5.677E+16, 9.398E-08),
    (1.771E+17, 2.298E-08),
    (5.677E+17, 1.467E-08),
    (1.771E+18, 1.881E-08),
    (5.677E+18, 3.382E-08),
    (1.771E+19, 7.179E-08),
    (5.677E+19, 1.725E-07),
    (1.771E+20, 4.412E-07)
]))

###
#auger_limit = np.array(([
#    (5.62e+16, 1.101e-07),
#    (1.78e+17, 2.75e-08),
#    (5.62e+17, 1.716e-08),
#    (1.78e+18, 2.327e-08),
#    (5.62e+18, 4.626e-08),
#    (1.78e+19, 1.198e-07),
#    (5.62e+19, 3.603e-07),
##    (1.78e+20, 1.156e-06)
#]))

auger_limit[:, 0] *= units.eV
auger_limit[:, 1] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
auger_limit[:, 1] /= 2  # half-decade binning
auger_limit[:, 1] *= energyBinsPerDecade
auger_limit[:, 1] *= 3. * flavorRatio

# ARA Published 2sta x 1yr analysis level limit:
ara_1year = np.array((
[9.80923e+15, 3.11547e+16, 9.79329e+16, 3.1057e+17, 9.75635e+17,
3.0924e+18, 9.80103e+18, 3.07732e+19, 9.75028e+19],
[0.000166106, 1.24595e-05, 4.06271e-06, 2.04351e-06, 1.48811e-06,
1.42649e-06, 1.50393e-06, 2.10936e-06, 3.25384e-06]
))

ara_1year = ara_1year.T

ara_1year[:, 0] *= units.eV
ara_1year[:, 1] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ara_1year[:, 1] /= 1  # binning is dLogE = 1
ara_1year[:, 1] *= energyBinsPerDecade
ara_1year[:, 1] *= flavorRatio

# Analysis from https://doi.org/10.1103/PhysRevD.102.043021  https://arxiv.org/abs/1912.00987
# 2 stations (A2 and A3), approx 1100 days of livetime per station
ara_4year_E, ara_4year_limit, t1, t2 = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "limit_a23.txt"), unpack=True)
ara_4year_E *= units.eV
ara_4year_limit *= units.eV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
ara_4year_limit *= energyBinsPerDecade
ara_4year_limit *= flavorRatio

# ARA 2023 projection
'''
This estimate is built by using the actual recorded livetime for the ARA stations 
through June 2021. Specifically:
1747 days of A1
5627 days of A2 + A3 + A4
826 days of A5

And then adding projected livetime
A1: 7/12 of a year for 2021, then 1 year of 2022, and 1 year of 2023
A2: no more data for 2021, no data for 2022, 1 year of 2023
A3: 7/12 of a year for 2021, then 1 year of 2022, and 1 year of 2023
A4: no more data for 2021, no data for 2022, 1 year of 2023
A5: 7/12 of a year for 2021, then 1 year of 2022, and 1 year of 2023

Total livetime = 

We do include different effective areas for A1, A2/3/4, and A5,
since A1 is smaller (only being at 100m), while A5 is larger (having the phased array).

We also included the trigger level and analysis level estimate.
The analysis level option assumes the A2 analysis efficiency for stations A1-4,
and a (preliminary) analysis efficiency estimate from the phased-array analysis.

'''
ara_2023_E_TL, ara_2023_limit_TL, t1, t2 = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "limit_ara_2023_projected_trigger.txt"), unpack=True)
ara_2023_E_TL *= units.GeV
ara_2023_limit_TL *= units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
ara_2023_limit_TL *= energyBinsPerDecade
ara_2023_limit_TL *= 2.44  # convert to 90%CL limit to be comparable with information from other experiments
ara_2023_limit_TL *= flavorRatio # convert from all-flavor to nutau

ara_2023_E, ara_2023_limit, t1, t2 = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "limit_ara_2023_projected_analysis.txt"), unpack=True)
ara_2023_E *= units.GeV
ara_2023_limit *= units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
ara_2023_limit *= energyBinsPerDecade
ara_2023_limit *= 2.44  # convert to 90%CL limit to be comparable with information from other experiments
ara_2023_limit *= flavorRatio  # convert from all-flavor to nutau


ARIANNA_HRA = np.array([[1.00000003e+07, 3.16228005e+07, 9.99999984e+07, 3.16227997e+08,
                         9.99999984e+08, 3.16228010e+09, 9.99999998e+09, 3.16228010e+10,
                         1.00000002e+11, 3.16227988e+11, 1.00000002e+12],
                         [8.66913580e-06, 4.31024784e-06, 3.02188396e-06, 1.95297917e-06,
                          1.67624432e-06, 2.09537200e-06, 2.90309617e-06, 4.41176250e-06,
                          7.49194972e-06, 1.33386048e-05, 2.57394786e-05]])
ARIANNA_HRA = ARIANNA_HRA.T
ARIANNA_HRA[:, 0] *= units.GeV
ARIANNA_HRA[:, 1] /= 1
ARIANNA_HRA[:, 1] *= (units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1)
ARIANNA_HRA[:, 1] *= energyBinsPerDecade
ARIANNA_HRA[:, 1] *= flavorRatio

# Gen2 Radio
# flux limit for 5 years, Gen2 Whitepaper
# has a factor of 2 discrepancy. Warn against using. 
# If you do use it, divide E2^2 flux by 2
gen2_E = np.array([1.04811313e+07, 1.32571137e+07, 1.67683294e+07, 2.12095089e+07,
         2.68269580e+07, 3.39322177e+07, 4.29193426e+07, 5.42867544e+07,
         6.86648845e+07, 8.68511374e+07, 1.09854114e+08, 1.38949549e+08,
         1.75751062e+08, 2.22299648e+08, 2.81176870e+08, 3.55648031e+08,
         4.49843267e+08, 5.68986603e+08, 7.19685673e+08, 9.10298178e+08,
         1.15139540e+09, 1.45634848e+09, 1.84206997e+09, 2.32995181e+09,
         2.94705170e+09, 3.72759372e+09, 4.71486636e+09, 5.96362332e+09,
         7.54312006e+09, 9.54095476e+09, 1.20679264e+10, 1.52641797e+10,
         1.93069773e+10, 2.44205309e+10, 3.08884360e+10, 3.90693994e+10,
         4.94171336e+10, 6.25055193e+10, 7.90604321e+10]) * units.GeV
gen2_flux = np.array([4.31746055e-09, 3.35020540e-09, 3.05749445e-09, 2.03012634e-09,
         1.63506056e-09, 1.40330116e-09, 1.15462951e-09, 9.20314379e-10,
         8.30543484e-10, 7.39576420e-10, 6.62805773e-10, 6.53304354e-10,
         5.41809080e-10, 5.34471053e-10, 5.23081048e-10, 5.20402393e-10,
         5.02987613e-10, 5.15328224e-10, 5.07092113e-10, 5.21866877e-10,
         5.30937694e-10, 5.38624813e-10, 5.66520488e-10, 5.71916762e-10,
         5.93193816e-10, 6.19149497e-10, 6.54847181e-10, 6.78492966e-10,
         7.15178112e-10, 7.64935941e-10, 8.08811879e-10, 8.58068389e-10,
         9.13675213e-10, 9.87276891e-10, 1.06320301e-09, 1.15183347e-09,
         1.25627989e-09, 1.36100197e-09, 1.49171667e-09]) * plotUnitsFlux
         
# Gen2 ICRC2021
gen2radio_E, gen2radio_flux = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/Gen2radio_sensitivity_ICRC2021.txt"))
gen2radio_E *= units.eV
gen2radio_flux *= units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
gen2radio_flux *= 10. * units.year / livetime
gen2radio_flux *= flavorRatio

# Gen2 projection
gen2proj = json.load(open("data/data_gen2wp.json"))
gen2proj_en = (np.array(gen2proj['data']['xlimits']).T[0] + np.array(gen2proj['data']['xlimits']).T[1]) / 2. * units.GeV
gen2proj_flux = 3e-8 * np.array(gen2proj['data']['ycenters']) *  units.GeV * units.cm ** -2 * units.s ** -1
gen2proj_flux_lims = 3e-8 * np.array(gen2proj['data']['ylimits']).T * units.GeV * units.cm ** -2 * units.s ** -1 
gen2proj_flux *= flavorRatio
#gen2proj_flux *= 10  * units.year / livetime
gen2proj_flux_lims *= flavorRatio
#gen2proj_flux_lims *= 10  * units.year / livetime
#g2fl_0 = gen2proj_flux_lims[0]
#g2fl_1 = gen2proj_flux_lims[1]
#gen2proj_flux_lims[0] = abs(g2fl_1 )
#gen2proj_flux_lims[1] = abs(g2fl_0 )#
gen2proj_flux_lims[0] = abs(gen2proj_flux - gen2proj_flux_lims[0])
gen2proj_flux_lims[1] = abs(gen2proj_flux_lims[1] - gen2proj_flux)

# Gen2 optical + radio
# energy [GeV], sensitivity for 10 years in GeV * cm ** -2 * second ** -1 * sr ** -1
gen2_E = np.array([      3.16227766e+04,           1.00000000e+05,           3.16227766e+05,           1.00000000e+06,           3.16227766e+06,           1.00000000e+07,           3.16227766e+07,           1.00000000e+08, 3.16227766e+08, 1.00000000e+09, 3.16227766e+09, 1.00000000e+10, 2.81838293e+10, 5.01187234e+10])
gen2_flux = np.array([   6.39048643e-10,           2.63971938e-10,           2.22188728e-10,           2.84591625e-10,           3.27334883e-10,           4.55529915e-10,           1.02329446e-09,           9.27354904e-10, 5.71972753e-10, 4.30260929e-10, 4.38008376e-10, 5.70960976e-10, 9.39718431e-10, 2.81674075e-09])
#gen2_E, gen2_flux = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/Gen2radio_sensitivity_ICRC2021.txt"))
gen2_E *= units.GeV
gen2_flux *= units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
gen2_flux *= 10. * units.year / livetime
gen2_flux *= flavorRatio
gen2_E = gen2_E[3:-1]
gen2_flux = gen2_flux[3:-1]

        
# flux limit for 5 years
RNOG_E = np.array([1.77827941e+07, 5.62341325e+07, 1.77827941e+08, 5.62341325e+08,
                   1.77827941e+09, 5.62341325e+09, 1.77827941e+10, 5.62341325e+10]) * units.GeV
RNOG_flux = np.array([4.51342568e-08, 1.57748718e-08, 1.03345333e-08, 7.98437261e-09,
                      7.22245212e-09, 7.62588582e-09, 9.28033358e-09, 1.28698605e-08]) * plotUnitsFlux
RNOG_flux *= flavorRatio
RNOG_flux *= 5 * units.year / livetime
 
# ARIANNA 200 predictions
# 10 year sensitivity
arianna_200 = np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', "expected_sensivity_ARIANNA-200.txt"))
arianna_200[:, 0] *= units.GeV
arianna_200[:, 1] *= units.GeV * units.cm ** -2 * units.s ** -1
arianna_200[:, 1] *= 10. * units.year / livetime
arianna_200[:, 1] *= flavorRatio

# TAROGE-M
# 10 stations, 5 year exposure, nutau only
#Log(Energy) GeV       Sensitivity*E^2 (GeV/cm^2 s sr)
taroge_m = np.array([8.5, 2.03E-05,
9.0,         1.80E-06,
9.5,         1.05E-06,
10.0,       1.45E-06,
10.5,       3.38E-06,
11.0,       9.20E-06])
taroge_m_E = pow(10,taroge_m[::2]) * units.GeV
taroge_m_flux = taroge_m[1::2] * units.GeV * units.cm ** -2 * units.s ** -1
taroge_m_flux *= 3.0 * flavorRatio
print(len(taroge_m_E), len(taroge_m_flux))

