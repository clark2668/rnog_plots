import matplotlib
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.rc('axes', labelsize=18)
matplotlib.rcParams['lines.linewidth'] = 3

#matplotlib.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
matplotlib.rc('font',**{'family':'serif','serif':['Palatino']})
matplotlib.rc('text', usetex=True)
legendfontsize = 13

import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import units
import fluxes
import os
import E2_fluxes_HESnowmass as nuplot

rnog_energies = np.asarray([ 3.162e+07,  1.000e+08,  3.162e+08,  1.000e+09,  3.162e+09,
        1.000e+10,  3.162e+10,  1.000e+11]) * 1E9
rnog_today = np.asarray([ 6.792e-06,  1.409e-06,  5.108e-07,  2.584e-07,  1.814e-07,
        1.619e-07,  1.325e-07,  1.691e-07])
rnog_2031 = np.asarray([ 4.749e-08,  1.466e-08,  7.729e-09,  5.169e-09,  4.133e-09,
        4.324e-09,  4.378e-09,  5.757e-09])
rnog_2040 = np.asarray([ 1.552e-08,  4.823e-09,  2.566e-09,  1.735e-09,  1.394e-09,
        1.467e-09,  1.496e-09,  1.973e-09])


# YOU NEED TO CHANGE THIS IN E2_fluxes_NuTauSnowmass,
# expdata.py AND modeldata.py 
# TO UPDATE PROPERLY
energyBinsPerDecade = 1.
plotUnitsEnergy = units.eV
plotUnitsEnergyStr = "eV"
plotUnitsFlux = units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
flavorRatio = 1.
DIFFUSE = True
livetime = 10 * units.year
subtitles = [""]

#subtitles = ['Water and Ice', "Atmosphere, Earth's Limb, Topography", "$\nu_\tau$ Only"]
def axtrans(x, ax, bx):
    return (np.log(x) - np.log(ax))/(np.log(bx) - np.log(ax))


# identify which subplot to include
show_icecube = [0]
show_icecube_uhe = [0]
show_anita = [0]
show_pueo = [1]
show_poemma = [1]
show_eusospb =[1]
show_auger = [0]
show_ara = [0]
show_arianna = [0]
show_grand = [1]
show_beacon = [1]
show_taroge = [1]
show_trinity = [1]
show_tambo = [1]
show_radar = [1]
show_rnog = [1]
show_gen2 = [1]

fig, axs = plt.subplots(1, 1, figsize=(8, 8))
second_axs = []     
for i in range(0,1):
    fig, ax = nuplot.get_E2_limit_figure(fig=fig, ax=axs,show_model_legend=True,
                                      diffuse=DIFFUSE,
                                                              show_ice_cube_EHE_limit=i in show_icecube_uhe,
                                                              show_ice_cube_HESE_data=False,
                                                              show_ice_cube_HESE_fit=i in show_icecube,
                                                              show_ice_cube_mu=i in show_icecube,
                                                              nu_mu_show_data_points=False,
                                                              show_ice_cube_mu_extrap=False,
                                                              show_icecube_glashow=False,
                                                              show_anita_I_III_limit=False,
                                                                show_anita_I_IV_limit=i in show_anita,
                                                              show_pueo30=False,
                                                              show_pueo100=i in show_pueo,
                                                              show_poemma=i in show_poemma,
                                                              show_poemma360=False,
                                                              show_poemma_fluor=i in show_poemma,
                                                              show_eusospb=False,
                                                              show_auger_limit=i in show_auger,
                                                              show_ara=i in show_ara,
                                                              show_ara_2023=False,
                                                              show_ara_2023_TL=False,
                                                              show_arianna=i in show_arianna,
                                                              show_grand_10k=False,
                                                              show_grand_200k=i in show_grand,
                                                              show_beacon=i in show_beacon,
                                                              show_taroge=False,
                                                              show_tambo=i in show_tambo,
                                                              show_trinity=i in show_trinity,
                                                              show_ska=False,
                                                              show_radar=i in show_radar,
                                                              show_RNOG=i in show_rnog,
                                                              show_IceCubeGen2_whitepaper=False,
                                                              show_IceCubeGen2_ICRC2021=False,
                                                              show_IceCubeGen2_combo=i in show_gen2,
                                                              show_IceCubeGen2_proj=False,
                                                              show_ara_1year=False,
                                                              show_prediction_arianna_200=False,
                                                              show_Heinze=False,
                                                              show_Auger_vanvliet=True,
                                                              show_TA=False,
                                                              show_TA_nominal=False,
                                                              show_TA_ICRC2021=False,
                                                              show_neutrino_best_fit=False,
                                                              show_neutrino_best_case=False,
                                                              show_neutrino_worst_case=False,
                                                              show_muf_bestfit=True,
                                                              show_astro=True)
    

    import numpy as np
    data_rodgrigues = np.genfromtxt("data/flux_rodrigues_all_agn_source.dat", names=["energy", "nue", "numu", "nutau", "nuebar", "numubar", "nutaubar"])
    flux_rodrigues = data_rodgrigues["nue"] + data_rodgrigues["numu"] + data_rodgrigues["nutau"] + data_rodgrigues["nuebar"] + data_rodgrigues["numubar"] + data_rodgrigues["nutaubar"]
    energy_rodrigues = data_rodgrigues["energy"]*1E9 #convert to eV


    # axs.plot(energy_rodrigues*1E9, flux_rodrigues)
    axs.fill_between(energy_rodrigues, flux_rodrigues*1E-10, flux_rodrigues, color='#6baed6')



    energy_fang = np.asarray([ 1.122e+03,  1.413e+03,  1.778e+03,  2.239e+03,  2.818e+03,
            3.548e+03,  4.467e+03,  5.623e+03,  7.079e+03,  8.913e+03,
            1.122e+04,  1.413e+04,  1.778e+04,  2.239e+04,  2.818e+04,
            3.548e+04,  4.467e+04,  5.623e+04,  7.079e+04,  8.913e+04,
            1.122e+05,  1.413e+05,  1.778e+05,  2.239e+05,  2.818e+05,
            3.548e+05,  4.467e+05,  5.623e+05,  7.079e+05,  8.913e+05,
            1.122e+06,  1.413e+06,  1.778e+06,  2.239e+06,  2.818e+06,
            3.548e+06,  4.467e+06,  5.623e+06,  7.079e+06,  8.913e+06,
            1.122e+07,  1.413e+07,  1.778e+07,  2.239e+07,  2.818e+07,
            3.548e+07,  4.467e+07,  5.623e+07,  7.079e+07,  8.913e+07,
            1.122e+08,  1.413e+08,  1.778e+08,  2.239e+08,  2.818e+08,
            3.548e+08,  4.467e+08,  5.623e+08,  7.079e+08,  8.913e+08,
            1.122e+09,  1.413e+09,  1.778e+09,  2.239e+09,  2.818e+09,
            3.548e+09,  4.467e+09,  5.623e+09,  7.079e+09,  8.913e+09,
            1.122e+10,  1.413e+10,  1.778e+10,  2.239e+10,  2.818e+10,
            3.548e+10,  4.467e+10,  5.623e+10,  7.079e+10,  8.913e+10,
            1.122e+11,  1.413e+11,  1.778e+11,  2.239e+11,  2.818e+11,
            3.548e+11,  4.467e+11,  5.623e+11,  7.079e+11,  8.913e+11,
            1.122e+12,  1.413e+12,  1.778e+12,  2.239e+12,  2.818e+12,
            3.548e+12,  4.467e+12,  5.623e+12,  7.079e+12,  8.913e+12])*1E9 # convert to eV

    flux_fang = np.asarray([ 4.645e-11,  5.350e-11,  6.148e-11,  7.064e-11,  8.121e-11,
            9.367e-11,  1.087e-10,  1.268e-10,  1.473e-10,  1.699e-10,
            1.945e-10,  2.216e-10,  2.522e-10,  2.862e-10,  3.243e-10,
            3.667e-10,  4.147e-10,  4.678e-10,  5.281e-10,  5.981e-10,
            6.758e-10,  7.622e-10,  8.600e-10,  9.696e-10,  1.090e-09,
            1.224e-09,  1.376e-09,  1.542e-09,  1.731e-09,  1.941e-09,
            2.168e-09,  2.414e-09,  2.686e-09,  2.993e-09,  3.340e-09,
            3.731e-09,  4.169e-09,  4.641e-09,  5.127e-09,  5.623e-09,
            6.145e-09,  6.691e-09,  7.241e-09,  7.827e-09,  8.458e-09,
            9.086e-09,  9.658e-09,  1.020e-08,  1.069e-08,  1.115e-08,
            1.168e-08,  1.214e-08,  1.239e-08,  1.260e-08,  1.260e-08,
            1.236e-08,  1.183e-08,  1.106e-08,  1.035e-08,  9.540e-09,
            8.676e-09,  7.701e-09,  6.807e-09,  5.762e-09,  4.668e-09,
            3.432e-09,  2.391e-09,  1.761e-09,  1.178e-09,  7.398e-10,
            3.932e-10,  1.378e-10,  4.994e-11,  2.130e-11,  3.280e-12,
            1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,
            1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,
            1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,
            1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,
            1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209,  1.000e-209])

    axs.fill_between(energy_fang, flux_fang*1E-10, flux_fang, color='#6baed6')

    # ara

    ara_energies = np.asarray([1.02E+07, 3.19E+07, 1.01E+08, 3.35E+08, 1.09E+09,
                               3.10E+09, 1.05E+10, 3.12E+10, 1.08E+11, 3.34E+11, 9.30E+11])
    ara_ses = np.asarray([5.75E-13, 2.87E-14, 2.43E-15, 3.01E-16, 6.00E-17,
                          1.78E-17, 5.23E-18, 2.20E-18, 9.26E-19, 4.57E-19, 2.80E-19]) * ara_energies # make E2
    ara_energies *= 1E9 # convert to eV for our plot

    ax.plot(ara_energies, ara_ses, color="grey", alpha=0.5, linewidth=4)

    ax.annotate('ARA-5',
                xy=(1.5E16 * units.eV / plotUnitsEnergy, 0.5e-6* 3.0 * flavorRatio), xycoords='data',
                horizontalalignment='left', color='grey', fontsize=14, rotation=-60, alpha=0.75)



    # gen2 
    gen2_energies = np.asarray([1.06E+07, 3.56E+07, 1.10E+08, 4.53E+08, 1.47E+09,
                                3.84E+09, 1.20E+10, 3.50E+10, 7.87E+10]) * 1E9 # to eV
    gen2_limit = np.asarray([2.18E-09, 6.99E-10, 3.46E-10, 2.60E-10, 2.81E-10,
                             3.21E-10, 4.19E-10, 5.78E-10, 7.69E-10])

    ax.plot(gen2_energies, gen2_limit, color="grey",linewidth=4)

    ax.annotate('Gen2',
                xy=(1.3E16 * units.eV / plotUnitsEnergy, 0.4e-9* 3.0 * flavorRatio), xycoords='data',
                horizontalalignment='left', color='grey', fontsize=14, rotation=-40)



    # handles = [leg_transgz, leg_pulars, leg_agn, leg_bllacs]

    # specific_model_legs = plt.legend(handles=handles, loc=6, fontsize=legendfontsize, handlelength=4)

    ax.plot(rnog_energies, rnog_today, lw=5, color="C1")
    ax.plot(rnog_energies, rnog_2031, lw=5, color="C3")
    ax.plot(rnog_energies, rnog_2040, lw=5, color="black")



    axs.set_yscale('log')
    axs.set_xscale('log')
    axs.set_xlabel(f'Neutrino Energy [{plotUnitsEnergyStr}]', fontsize=24)  
    axs.set_ylabel(r'$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]',fontsize=24)
    axs.set_title(subtitles[i])
    #second_axs.append(axs[i].secondary_yaxis('right', functions=(lambda x: 3. * x, lambda x: x / 3.)))
    #second_axs[i].set_ylabel(r"All Flavor $E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}]$", fontsize=12)
    # axs.grid(True, which='minor', alpha=0.1)
    # axs.grid(True, which='major', alpha=0.4)
    #axs[i].legend(loc='lower left', fontsize=12)
    
    
    minx = 1.2e15 * units.eV / plotUnitsEnergy
    maxx = 1e20 * units.eV / plotUnitsEnergy
    miny= 0.2e-10*3
    miny= 0.2e-11*3
    maxy =  1e-5*3
                   
    #axs.plot(3e15,1e-6, 'ko', marker=r'$\downarrow$', markersize=20)
    if DIFFUSE:
        
        axs.set_ylim(miny,maxy)
        axs.set_xlim(minx,maxx)
        #axs[i].set_yticks([1e-12, 1e-11,1e-10,1e-9,1e-8,1e-7, 1e-6, 1e-5])
        # axs.set_yticks([1e-10,1e-9,1e-8,1e-7, 1e-6, 1e-5])
        axs.set_yticks([1E-9, 1e-8,1e-7, 1e-6, 1e-5])
        axs.yaxis.set_minor_locator(tck.AutoMinorLocator())
        axs.minorticks_on()
        axs.tick_params(axis='both', which='major', labelsize=20)
        #axs[i].tick_params(axis='y', which='minor', left=True)

import matplotlib.patheffects as pe

axs.annotate('RNO-G-8',
                    xy=(2.5e9*1E9, 1.8E-7), xycoords='data',
                    horizontalalignment='center', color='C1', rotation=-20, fontsize=25,
                    path_effects=[pe.withStroke(linewidth=4, foreground="white")]
                    )

axs.annotate('RNO-G-35 2031',
                    xy=(2e9*1E9, 5E-9), xycoords='data',
                    horizontalalignment='center', color='firebrick', rotation=-10, fontsize=25,
                    path_effects=[pe.withStroke(linewidth=4, foreground="white")]
                    )


axs.annotate('RNO-G-35 2040',
                    xy=(2e9*1E9, 1.5E-9), xycoords='data',
                    horizontalalignment='center', color='black', rotation=-10, fontsize=25,
                    path_effects=[pe.withStroke(linewidth=4, foreground="white")]
                    )




# fig.suptitle("Diffuse Flux, 1:1:1 Flavor Ratio  ", fontsize=18)
# fig.subplots_adjust(top=0.94, hspace=0.18, bottom=0.09, right=0.92, left=0.08)
fig.tight_layout()
#labels = []
#labels = add_limit(ax, labels, veff[:, 0], veff[:, 1], n_stations=100, livetime=5 * units.year, label=veff_label)
#labels = add_limit(ax, labels, veff[:, 0], veff[:, 1], n_stations=1000, livetime=5 * units.year, label=veff_label)
#plt.legend(handles=labels, loc=2)
if DIFFUSE:
    name_plot = "Limit_diffuse_single.png"
else:
    name_plot = "Limit_sources.png"
plt.savefig(name_plot)

if DIFFUSE:
    name_plot = "Limit_diffuse_single.pdf"
else:
    name_plot = "Limit_sources.pdf"
plt.savefig(name_plot)
plt.show()