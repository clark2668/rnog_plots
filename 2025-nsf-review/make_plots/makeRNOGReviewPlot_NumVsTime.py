import numpy as np
from scipy.interpolate import splrep, splev
import matplotlib.pyplot as plt
from pylab import setp

from scipy import interpolate

NucleonMass = 1.67e-24 #nucleon mass in grams
EarthDensity = 3.8 #g/cm^2

def get_Lint(energy_eV, which_sigma=None):
    """
    get_Lint

    This is a parameterization of the neutrino effective length.
    By default, it will use a cross section 
    measurement from Ghandi et. al. (10.1103/PhysRevD.58.093009)


    Parameters
    ----------
    logev (float): energy in eV
        energy of your neutrino in electron volts

    Returns
    -------
    Lint (float): interaction length
        interaction length of a neutrino in centimeters
    """
    Lint=0.

    if(which_sigma==None):
        #by default, assuem Ghandi et. al. (10.1103/PhysRevD.58.093009)

        sigma = 7.84e-36 * ((energy_eV/1.e9)**0.363)
        Lint = NucleonMass / (EarthDensity * sigma)

    return Lint

def get_flux(resource_name, energy_vals_logeV):
    """
    get_flux

    Return the flux of neutrinos as a function of energy


    Parameters
    ----------
    resource_name: name of the flux you want
        name of the flux you want
    energy_vals_logeV:
        the energies you want the flux evaluted at, in units of log10(eV)

    Returns
    -------
    flux: ndarray
        the flux prediction in units of 1/cm^2/s/sr/eV

    """
    flux = np.array([])

    if(resource_name=='icecube_thrumu'):
        def icecube_thrumu_function(E):
            return 3.03 * ((E/1.e14)**-2.19) * 1e-27
        flux = icecube_thrumu_function(np.power(10.,energy_vals_logeV))
    elif(resource_name=='icecube_combined'):
        def icecube_combined_function(E):
            return 6.7 * ((E/1.e14)**-2.50) * 1e-27
        flux = icecube_combined_function(np.power(10.,energy_vals_logeV))
    elif(resource_name=='icecube_marco'):
        def icecube_marco(E):
            return 4.32 * ((E/1.e14)**-2.37) * 1e-27
        flux = icecube_marco(np.power(10.,energy_vals_logeV))
        print(flux)
    elif(resource_name=='transgzk'):
        data_transgzk = np.genfromtxt("data/trans_gzk_protons.csv",delimiter=",", names=["energy", "flux"])
        loge_transgzk = np.log10(data_transgzk["energy"]) # original data is eV
        flux_transgzk = np.log10(data_transgzk["flux"]) # original data is GeV/cm2/s/sr
        interp_transgzk = interpolate.Akima1DInterpolator( loge_transgzk, flux_transgzk, method="makima")
        interp_transgzk.extrapolate = False
        flux = np.power(10.,interp_transgzk(energy_vals_logeV)) # 10 ^ (output of spline), to get back to GeV/cm2/s/sr
        flux = np.nan_to_num(flux) # convert nans to zeros
        energy_vals_eV = np.power(10., energy_vals_logeV)
        energy_vals_GeV = energy_vals_eV/1E9
        flux = flux/energy_vals_GeV/energy_vals_eV
    elif(resource_name=='pulsars'):
        data_transgzk = np.genfromtxt("data/pulsars.csv",delimiter=",", names=["energy", "flux"])
        loge_transgzk = np.log10(data_transgzk["energy"]) # original data is eV
        flux_transgzk = np.log10(data_transgzk["flux"]) # original data is GeV/cm2/s/sr
        interp_transgzk = interpolate.Akima1DInterpolator( loge_transgzk, flux_transgzk, method="makima")
        interp_transgzk.extrapolate = False
        flux = np.power(10.,interp_transgzk(energy_vals_logeV)) # 10 ^ (output of spline), to get back to GeV/cm2/s/sr
        flux = np.nan_to_num(flux) # convert nans to zeros
        energy_vals_eV = np.power(10., energy_vals_logeV)
        energy_vals_GeV = energy_vals_eV/1E9
        flux = flux/energy_vals_GeV/energy_vals_eV,
    elif(resource_name=='agn'):
        data_transgzk = np.genfromtxt("data/agn.csv",delimiter=",", names=["energy", "flux"])
        loge_transgzk = np.log10(data_transgzk["energy"]) # original data is eV
        flux_transgzk = np.log10(data_transgzk["flux"]) # original data is GeV/cm2/s/sr
        interp_transgzk = interpolate.Akima1DInterpolator( loge_transgzk, flux_transgzk, method="makima")
        interp_transgzk.extrapolate = False
        flux = np.power(10.,interp_transgzk(energy_vals_logeV)) # 10 ^ (output of spline), to get back to GeV/cm2/s/sr
        flux = np.nan_to_num(flux) # convert nans to zeros
        energy_vals_eV = np.power(10., energy_vals_logeV)
        energy_vals_GeV = energy_vals_eV/1E9
        flux = flux/energy_vals_GeV/energy_vals_eV
    elif(resource_name=='bllacs'):
        data_transgzk = np.genfromtxt("data/bllacs.csv",delimiter=",", names=["energy", "flux"])
        loge_transgzk = np.log10(data_transgzk["energy"]) # original data is eV
        flux_transgzk = np.log10(data_transgzk["flux"]) # original data is GeV/cm2/s/sr
        interp_transgzk = interpolate.Akima1DInterpolator( loge_transgzk, flux_transgzk, method="makima")
        interp_transgzk.extrapolate = False
        flux = np.power(10.,interp_transgzk(energy_vals_logeV)) # 10 ^ (output of spline), to get back to GeV/cm2/s/sr
        flux = np.nan_to_num(flux) # convert nans to zeros
        energy_vals_eV = np.power(10., energy_vals_logeV)
        energy_vals_GeV = energy_vals_eV/1E9
        flux = flux/energy_vals_GeV/energy_vals_eV
    elif(resource_name=='crnu'):
        data_muzio_1EeV = np.genfromtxt("data/bestfit_IC_KM3NeThi_xmaxShift_UHEp_sibyll_retuneNuSum.txt",
                                    names=["energy", "flux", "e", "mu", "tau", "low"]
                                    )
        loge = data_muzio_1EeV["energy"] # original data is logeV
        flux = np.log10(data_muzio_1EeV["flux"]) # original data is GeV/cm2/s/sr
        print(flux)
        interp = interpolate.Akima1DInterpolator( loge, flux, method="makima")
        interp.extrapolate = False
        flux = np.power(10.,interp(energy_vals_logeV)) # 10 ^ (output of spline), to get back to GeV/cm2/s/sr
        flux = np.nan_to_num(flux) # convert nans to zeros
        energy_vals_eV = np.power(10., energy_vals_logeV)
        energy_vals_GeV = energy_vals_eV/1E9
        flux = flux/energy_vals_GeV/energy_vals_eV
    return flux

def beautify_counts(this_ax):

	"""
	beautify_counts

	Beautifies a histogram of the counts

	Parameters
	----------
	this_ax (matplotlib.axes) : name of the axis you want beautified
		a matplotlib axis object

	Returns
	-------
	None:
		the function modifies the axes passed to it

	"""

	sizer=20
	xlow =  1.e15 #the lower x limit
	xup = 1e21 #the uppper x limit
	this_ax.set_xlabel('Energy [eV]',size=sizer) #give it a title
	this_ax.set_ylabel('Events',size=sizer)
	this_ax.set_xscale('log')
	this_ax.tick_params(labelsize=sizer)
	this_ax.set_xlim([xlow,xup]) #set the x limits of the plot
	this_ax.grid()
	this_legend = this_ax.legend(loc='upper right',title='Event Counts')
	setp(this_legend.get_texts(), fontsize=17)
	setp(this_legend.get_title(), fontsize=17)

energies = np.asarray([ 3.162e+07,  1.000e+08,  3.162e+08,  1.000e+09,  3.162e+09,
        1.000e+10,  3.162e+10,  1.000e+11]) * 1E9

# units of cm3 sr seconds
data = {2024: np.asarray([ 8.591e+20,  8.472e+21,  4.895e+22,  2.069e+23,  6.410e+23,
        1.586e+24,  4.333e+24,  7.687e+24]), 2025: np.asarray([ 5.097e+21,  4.118e+22,  1.879e+23,  7.028e+23,  2.092e+24,
        4.804e+24,  1.204e+25,  2.132e+25]), 2026: np.asarray([ 1.345e+22,  9.853e+22,  4.104e+23,  1.416e+24,  4.061e+24,
        8.918e+24,  2.103e+25,  3.693e+25]), 2027: np.asarray([ 2.750e+22,  1.928e+23,  7.754e+23,  2.568e+24,  7.207e+24,
        1.547e+25,  3.532e+25,  6.155e+25]), 2028: np.asarray([ 4.722e+22,  3.239e+23,  1.283e+24,  4.160e+24,  1.153e+25,
        2.447e+25,  5.490e+25,  9.517e+25]), 2029: np.asarray([ 7.263e+22,  4.919e+23,  1.933e+24,  6.191e+24,  1.703e+25,
        3.592e+25,  7.977e+25,  1.378e+26]), 2030: np.asarray([ 1.018e+23,  6.845e+23,  2.678e+24,  8.515e+24,  2.331e+25,
        4.899e+25,  1.082e+26,  1.864e+26]), 2031: np.asarray([ 1.310e+23,  8.771e+23,  3.423e+24,  1.084e+25,  2.959e+25,
        6.206e+25,  1.366e+26,  2.351e+26]), 2032: np.asarray([ 1.602e+23,  1.070e+24,  4.168e+24,  1.316e+25,  3.587e+25,
        7.513e+25,  1.650e+26,  2.837e+26]), 2033: np.asarray([ 1.894e+23,  1.262e+24,  4.913e+24,  1.549e+25,  4.215e+25,
        8.820e+25,  1.934e+26,  3.323e+26]), 2034: np.asarray([ 2.186e+23,  1.455e+24,  5.658e+24,  1.781e+25,  4.844e+25,
        1.013e+26,  2.218e+26,  3.810e+26]), 2035: np.asarray([ 2.478e+23,  1.648e+24,  6.403e+24,  2.013e+25,  5.472e+25,
        1.143e+26,  2.502e+26,  4.296e+26]), 2036: np.asarray([ 2.770e+23,  1.840e+24,  7.148e+24,  2.246e+25,  6.100e+25,
        1.274e+26,  2.786e+26,  4.783e+26]), 2037: np.asarray([ 3.062e+23,  2.033e+24,  7.892e+24,  2.478e+25,  6.728e+25,
        1.405e+26,  3.070e+26,  5.269e+26]), 2038: np.asarray([ 3.354e+23,  2.225e+24,  8.637e+24,  2.711e+25,  7.356e+25,
        1.536e+26,  3.354e+26,  5.755e+26]), 2039: np.asarray([ 3.646e+23,  2.418e+24,  9.382e+24,  2.943e+25,  7.985e+25,
        1.666e+26,  3.638e+26,  6.242e+26]), 2040: np.asarray([ 3.938e+23,  2.611e+24,  1.013e+25,  3.175e+25,  8.613e+25,
        1.797e+26,  3.922e+26,  6.728e+26])}


logeV = np.log10(energies)
num_vs_time = {}

# models = ["transgzk", "pulsars", "agn", "bllacs"]
models = ["pulsars", "agn", "bllacs", "crnu"]
# labels = {"transgzk": "Trans GZK Protons", "pulsars": "Pulsars", "agn": "AGN", "bllacs": "BLLacs"}
labels = {"pulsars": "Pulsars", "agn": "AGN", "bllacs": "BLLacs", "crnu": r"CR+$\nu$ Joint Fit"}
for model in models:
    num_events = {}
    for y in data.keys():
        exposure_cm3srs = data[y]
        exposure_cm2srs = exposure_cm3srs/get_Lint(np.power(10., logeV))
        interpolator = splrep(logeV, np.log10(exposure_cm2srs))

        counts = []
        energy_bins = []
        bins = np.arange(15.5, 21, 0.5)
        for bin in bins:
            temp_logev = np.arange(bin,bin+0.5,0.1)
            temp_energy = np.power(10.,temp_logev)
            temp_aeff = np.power(10.,splev(temp_logev, interpolator))
            temp_flux = get_flux(model,temp_logev)
            temp_counts = np.trapz(temp_flux*temp_aeff,temp_energy)

            counts.append(temp_counts)
            energy_bins.append(np.power(10.,bin))

        counts=np.array(counts)
        energy_bins=np.array(energy_bins)

        fig = plt.figure(figsize=(5,5))
        ax_counts = fig.add_subplot(1,1,1)
        n, bins, patches= ax_counts.hist(energy_bins,
                                            bins=np.power(10.,np.arange(15,22,0.5)),
                                            weights=counts,
                                            label=r'IceCube Thru-Mu E$^{-2.19}$: %.2f'%counts.sum(),
                                            fill=False, 
                                            stacked=True, 
                                            histtype='step', 
                                            edgecolor='blue',
                                            linewidth=4)
        # beautify_counts(ax_counts)
        # fig.savefig(f"example_{y}.png",edgecolor='none',bbox_inches="tight") #save the figure

        num_events[y] = n.sum()
    num_vs_time[model] = num_events

import matplotlib
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.rc('axes', labelsize=18)
matplotlib.rcParams['lines.linewidth'] = 3
matplotlib.rc('font',**{'family':'serif','serif':['Palatino']})
matplotlib.rc('text', usetex=True)

fig = plt.figure(figsize=(5,5))
ax_ratevstime = fig.add_subplot(1,1,1)
for model in models:
    ax_ratevstime.plot(num_vs_time[model].keys(), num_vs_time[model].values(), label=f"{labels[model]}")
ax_ratevstime.set_yscale('log')
ax_ratevstime.legend(fontsize=12, loc="lower right")
ax_ratevstime.set_xlabel("Year", fontsize=16)
ax_ratevstime.set_ylabel("Number of Neutrinos", fontsize=16)
ax_ratevstime.tick_params(axis='both', which='major', labelsize=14)

#### mark LVK

LIGO_04_start = 2023.25
LIGO_04_end = 2024.4

LIGO_05_start = 2025.9
LIGO_05_end = 2028.9

ax_ratevstime.axvspan(LIGO_04_start,LIGO_04_end,color='blueviolet',alpha=0.2)
ax_ratevstime.axvspan(LIGO_05_start,LIGO_05_end,color='violet',alpha=0.2)

ax_ratevstime.annotate('LVK\nO4', weight='bold',
            xy=(2023.8,22), xycoords='data',
            horizontalalignment='center', color='blueviolet', rotation=0, fontsize=14)

ax_ratevstime.annotate('LVK\nO5', weight='bold',
            xy=(2027.5,22), xycoords='data',
            horizontalalignment='center', color='violet', rotation=0, fontsize=14)


# mark VRO 

import matplotlib.patches as mpatches

arr = mpatches.FancyArrowPatch((2025, 12), (2028, 12),
                               arrowstyle="->,head_width=.30",
                               mutation_scale=20,
                               color="C1", lw=2,
                               )
ax_ratevstime.add_patch(arr)
ax_ratevstime.annotate(f"VRO", (2025, 13), ha="left", va="bottom", color="C1", fontsize=15)
ax_ratevstime.set_ylim([0.02, 50])

ax_ratevstime.grid()

fig.tight_layout()
fig.savefig(f"num_vs_time.pdf", dpi=300)
fig.savefig(f"num_vs_time.png", dpi=300)
