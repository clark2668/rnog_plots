import numpy as np
import units
import os

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

from scipy.interpolate import interp1d


def get_TAGZK_flux(energy):
    """
    GZK neutrino flux from TA best fit from D. Bergmann privat communications
    """

    TA_data = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_combined_fit_m3.txt"))
    E = TA_data[:, 0] * units.GeV
    f = TA_data[:, 1] * plotUnitsFlux / E ** 2
    get_TAGZK_flux = interp1d(E, f, bounds_error=False, fill_value="extrapolate")
    return get_TAGZK_flux(energy)


def get_TAGZK_flux_ICRC2021(energy):
    """
    GZK neutrino flux from TA best fit ICRC2021
    https://pos.sissa.it/395/338/
    """
    TA_data = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_GZKprediction_ICRC2021.txt"))
    E = TA_data[:, 0] * units.GeV
    f = TA_data[:, 1] * plotUnitsFlux / E ** 2
    get_TAGZK_flux = interp1d(E, f, bounds_error=False, fill_value="extrapolate")
    return get_TAGZK_flux(energy)


def get_proton_10(energy):
    """
    10% proton flux at source for astrophysical parameters determined by Auger data, by van Vliet et al.
    """
    vanVliet_reas = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "ReasonableNeutrinos1.txt"))
    E = vanVliet_reas[0, :] * units.GeV
    f = vanVliet_reas[1, :] * plotUnitsFlux / E ** 2
    getE = interp1d(E, f, bounds_error=False, fill_value="extrapolate")
    return getE(energy)


def get_GZK_Auger_best_fit(energy):
    Heinze_band = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "talys_neu_bands.out"))
    E = Heinze_band[:, 0] * units.GeV
    f = Heinze_band[:, 1] / units.GeV / units.cm ** 2 / units.s / units.sr
    getE = interp1d(E, f, bounds_error=False, fill_value="extrapolate")
    return getE(energy)

#TA Combined fit
TA_data_low = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_combined_fit_low_exp_uncertainty.txt"))
TA_data_high = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_combined_fit_high_exp_uncertainty.txt"))

#TA Nominal
TA_data = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_combined_fit_m3.txt"))
          
# TA ICRC2021          
TA_data = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "TA_GZKprediction_ICRC2021.txt"))

# Cosmogenics from Auger combined fit bit (show_Auger) from van Vliet
vanVliet_max_1 = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "MaxNeutrinos1.txt"))
vanVliet_max_2 = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "MaxNeutrinos2.txt"))
vanVliet_reas = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "ReasonableNeutrinos1.txt")) 

vanVliet_max = np.maximum(vanVliet_max_1[1, :], vanVliet_max_2[1, :])

# Cosmogenics, pessimistic model with cutoffs in UHECR sources
# Henize
Heinze_band = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "talys_neu_bands.out"))
Heinze_evo = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "talys_neu_evolutions.out"))

tde = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/TDEneutrinos.txt"))
ll_grb = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/LLGRBneutrinos.txt"))
pulsars = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/Pulsar_Fang+_2014.txt"))
clusters = np.loadtxt(os.path.join(os.path.dirname(__file__), "data/cluster_Fang_Murase_2018.txt"))

# Fang & Metzger
data_ns_merger = np.array((
[164178.9149064658, 6.801708660714134e-11],
[336720.74740929523, 1.4132356758632395e-10],
[835305.4165187279, 3.649486484772094e-10],
[2160958.1870687287, 9.239856704429993e-10],
[8002898.345863899, 3.085108101843864e-9],
[20681309.183352273, 6.161686112812425e-9],
[61887155.98482043, 1.0930162266889215e-8],
[132044526.30261868, 1.3058095134564553e-8],
[253159530.43095005, 1.0506528126116853e-8],
[436411840.74101496, 6.5380862245683814e-9],
[635712891.7663972, 3.910881690144994e-9],
[944515747.1734984, 1.773891442500038e-9],
[1211896737.260516, 9.059026812485584e-10],
[1586152410.074502, 3.578063705414756e-10],
[1948716060.6917415, 1.358461111073226e-10],
[2344547243.608689, 5.26053655617631e-11]))

# Muzio, Unger, Farrar 2018 arXiv:1906.06233, EPOS
muf_epos_cosmo = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "MUF19_Fig9b_eposLHC.txt"))
muf_sibyll_cosmo = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "MUF19_Fig9b_sibyll23c.txt"))
muf_astro = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data', "MFU21_Fig1_flavor.txt"))            