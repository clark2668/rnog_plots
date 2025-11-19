import matplotlib
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.rc('axes', labelsize=18)
labelfontsize = 14
legendfontsize = 12.5

import matplotlib.pyplot as plt
import numpy as np
import units
import fluxes
import pandas as pd
import os
from expdata import *
from modeldata import *
from scipy import interpolate
from matplotlib.legend_handler import HandlerTuple
from matplotlib.container import ErrorbarContainer


# YOU NEED TO CHANGE THIS IN BOTH expdata.py and modeldata.py 
# TO UPDATE PROPERLY
energyBinsPerDecade = 1.
plotUnitsEnergy = units.eV
plotUnitsEnergyStr = "eV"
plotUnitsFlux = units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1
flavorRatio = 1.
DIFFUSE = True
livetime = 10 * units.year
plotUnitsLivetime = '5 years or 100 days'

# Unless you would like to work with the layout or the models/data from other experiments,
# you don't need to change anything below here
# --------------------------------------------------------------------
# Other planned experiments


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


def get_E2_limit_figure(fig=None, ax=None, show_model_legend=True,
                        diffuse=True,
                        show_ice_cube_EHE_limit=True,
                        show_ice_cube_EHE_limit_2025=True,
                        show_ice_cube_HESE_data=True,
                        show_ice_cube_HESE_fit=True,
                        show_ice_cube_mu=True,
                        nu_mu_show_data_points=True,
                        show_ice_cube_mu_extrap=False,
                        show_icecube_glashow=True,
                        show_anita_I_III_limit=False,
                        show_anita_I_IV_limit=True,
                        show_pueo30=True,
                        show_pueo100=False,
                        show_poemma=True,
                        show_poemma_fluor=True,
                        show_poemma360=True,
                        show_eusospb=True,
                        show_auger_limit=True,
                        show_ara=False,
                        show_ara_2023=True,
                        show_ara_2023_TL=False,
                        show_arianna=False,
                        show_neutrino_best_fit=False,
                        show_neutrino_best_case=False,
                        show_neutrino_worst_case=False,
                        show_grand_10k=False,
                        show_grand_200k=True,
                        show_beacon=True,
                        show_taroge=True,
                        show_tambo=True,
                        show_ska=False, 
                        show_trinity=True,
                        show_radar=True,
                        show_Heinze=False,
                        show_TA=False,
                        show_TA_nominal=False,
                        show_TA_ICRC2021=False,
                        show_RNOG=True,
                        show_IceCubeGen2_whitepaper=False,
                        show_IceCubeGen2_ICRC2021=False,
                        show_IceCubeGen2_combo=True,
                        show_IceCubeGen2_proj=True,
                        show_Auger_vanvliet=True,
                        show_ara_1year=False,
                        show_prediction_arianna_200=False,
                        show_muf_bestfit=True,
                        show_astro=True):

    # Limit E2 Plot
    # ---------------------------------------------------------------------------
    if fig == None or ax==None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
    # Neutrino Models
    # Version for a diffuse flux and for a source dominated flux
    if diffuse:
        legends = []
        # TA combined fit
        if(show_TA):
            TA_m3 = ax.fill_between(TA_data_low[:, 0] * units.GeV / plotUnitsEnergy,
                                     TA_data_low[:, 1] * flavorRatio, TA_data_high[:, 1] * flavorRatio,
                              label=r'UHECRs TA combined fit (1$\sigma$), Bergman et al.', color='C0', alpha=0.5, zorder=-1)
            legends.append(TA_m3)
        if(show_TA_nominal):
            E = TA_data[:, 0] * units.GeV
            f = TA_data[:, 1] * plotUnitsFlux * flavorRatio
            TA_nominal, = ax.plot(E / plotUnitsEnergy, f / plotUnitsFlux , "k-.", label="UHECRs TA combined fit, Bergman et al.")
            legends.append(TA_nominal)
        if(show_TA_ICRC2021):
            E = TA_data[:, 0] * units.GeV
            f = TA_data[:, 1] * plotUnitsFlux * flavorRatio
            TA_nominal, = ax.plot(E / plotUnitsEnergy, f / plotUnitsFlux, "k-.", label="UHECRs TA combined fit, Bergman et al.")
            legends.append(TA_nominal)

        
        if(show_Heinze):
#             best_fit, = ax.plot(Heinze_band[:, 0] * units.GeV / plotUnitsEnergy, Heinze_band[:, 1] * Heinze_band[:, 0] ** 2, c='k',
#                                 label=r'UHECR (Auger) combined fit, Heinze et al.', linestyle='-.')

#             Auger_bestfit = ax.fill_between(Heinze_band[:, 0],
#                                      Heinze_band[:, 2] * Heinze_band[:, 0] ** 2, Heinze_band[:, 3] * Heinze_band[:, 0] ** 2,
#                               label=r'UHECRs Auger combined fit, Heinze et al.', color='C1', alpha=0.5, zorder=1)

            Auger_bestfit = ax.fill_between(Heinze_evo[:, 0] * units.GeV / plotUnitsEnergy,
                                     Heinze_evo[:, 3] * Heinze_band[:, 0] ** 2 * flavorRatio, Heinze_evo[:, 4] * Heinze_band[:, 0] ** 2 * flavorRatio,
                              label=r'UHECRs Auger combined fit (3$\sigma$), Heinze et al.', color='C1', alpha=0.5, zorder=1)

#             Heinze_evo = np.loadtxt(os.path.join(os.path.dirname(__file__), "talys_neu_evolutions.out"))
#             best_fit_3s, = ax.plot(Heinze_evo[:, 0] * units.GeV / plotUnitsEnergy, Heinze_evo[:, 6] * Heinze_evo[:, 0] **
#                             2, color='0.5', label=r'UHECR (Auger) combined fit + 3$\sigma$, Heinze et al.', linestyle='-.')
            legends.append(Auger_bestfit)
#             legends.append(best_fit_3s)
        if show_muf_bestfit:
            muf_bestfit = ax.fill_between(pow(10, muf_epos_cosmo[:,0]) * units.eV / plotUnitsEnergy,
                                            muf_epos_cosmo[:,1] * flavorRatio, muf_epos_cosmo[:,2] * flavorRatio,
                                            label=r'Cosmo: UHECR + pure proton, Muzio',  color='#c6dbef')
            legends.append(muf_bestfit)
        if(show_Auger_vanvliet):

            #prot10, = ax.plot(vanVliet_reas[0, :] * units.GeV / plotUnitsEnergy, vanVliet_reas[1, :],
            #                  label=r'10% protons in UHECRs (Auger), m=3.4, van Vliet et al.', linestyle='--', color='k')

            prot = ax.fill_between(vanVliet_max_1[0, :] * units.GeV / plotUnitsEnergy, vanVliet_max * flavorRatio,
                                   vanVliet_reas[1, :] / 50 * flavorRatio, color='#9ecae1', label=r'Cosmo: UHECR constraints, van Vliet', zorder=-2)
            #legends.append(prot10)
            print(vanVliet_max_1[0, :] * units.GeV / plotUnitsEnergy)
            print(vanVliet_max * flavorRatio)
            
            legends.append(prot)

        if show_astro:
        
            muf_flux = muf_astro[:,3] + muf_astro[:,6]
            clusters_flux = clusters[:, 1]* flavorRatio
            tde_max_flux = tde[:, 2] * 3 * flavorRatio
            tde_min_flux = tde[:, 3] * 3 * flavorRatio
            
            astro_energies = np.logspace(11, 21.1, num=70)
            # interpolate in log space
            muf_interp = interpolate.interp1d( muf_epos_cosmo[:,0], np.log10(muf_flux), fill_value=-99., bounds_error=False,) 
            clusters_interp = interpolate.interp1d( np.log10(clusters[:, 0]) + 9., np.log10(clusters_flux),  fill_value=-99.,bounds_error=False,)
            tde_max_interp= interpolate.interp1d( np.log10(tde[:, 0]) + 9., np.log10(tde_max_flux),  fill_value=-99.,bounds_error=False,)
            tde_min_interp= interpolate.interp1d( np.log10(tde[:, 0]) + 9., np.log10(tde_min_flux),  fill_value=-99.,bounds_error=False,)
            
            muf_interp_flux = muf_interp(np.log10(astro_energies))
            clusters_interp_flux = clusters_interp(np.log10(astro_energies))
            tde_max_interp_flux = tde_max_interp(np.log10(astro_energies))
            tde_min_interp_flux = tde_min_interp(np.log10(astro_energies))
            
            muf_interp_flux[np.isinf(muf_interp_flux)] = -99.
            clusters_interp_flux[np.isinf(clusters_interp_flux)] = -99.
            tde_max_interp_flux[np.isinf(tde_max_interp_flux)] = -99.
            tde_min_interp_flux[np.isinf(tde_max_interp_flux)] = -99.

                        
            min_astro_flux =  np.minimum(muf_interp_flux, clusters_interp_flux)
            min_astro_flux =  np.minimum(min_astro_flux, tde_min_interp_flux)
            max_astro_flux =  np.maximum(muf_interp_flux, clusters_interp_flux)
            max_astro_flux =  np.maximum(max_astro_flux, tde_max_interp_flux)
            min_astro_flux = pow(10, min_astro_flux) * units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1   
            max_astro_flux = pow(10, max_astro_flux) * units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1   
        
            
            #plot_vals = np.where(min_astro_flux > 1e-12)
            plot_vals = np.ones(len(astro_energies), dtype=bool)
        
            
            print("astro energies", astro_energies[plot_vals]* units.eV / plotUnitsEnergy)
            print("min flux", min_astro_flux[plot_vals])
            print("max flux", max_astro_flux[plot_vals])
            # plot fills in between the maxima and minuma of the different fluxes
            
            #ax.plot(astro_energies[plot_vals], min_astro_flux[plot_vals]/plotUnitsFlux, "m")
            #ax.plot(astro_energies[plot_vals], max_astro_flux[plot_vals]/plotUnitsFlux, "b")
            
            astro_leg = ax.fill_between( astro_energies[plot_vals]* units.eV / plotUnitsEnergy,
                                            min_astro_flux[plot_vals]/plotUnitsFlux, max_astro_flux[plot_vals]/plotUnitsFlux,
                                            label=r'Astro: MMA constraints',  color='#6baed6')

            legends.append(astro_leg)
                        
            #muf_astro_leg, = ax.plot(pow(10, muf_epos_cosmo[:,0]) * units.eV / plotUnitsEnergy,
            #                                muf_astro[:,3] + muf_astro[:,6],
            #                                label=r'Astrophysical, UHECR + $\nu$ constraints, Muzio, et al',  color='k', linestyle='--')
            #p_cluster, = ax.plot(clusters[:, 0] * units.GeV / plotUnitsEnergy, clusters[:, 1]* flavorRatio, 
            #                        label="Clusters, Fang \& Murase", color="k", zorder=1, linestyle='-.')

            #p_tde, = ax.plot(tde[:, 0] * units.GeV / plotUnitsEnergy, tde[:, 1] * 3 * flavorRatio, 
            #                        label="TDE, Biehl et al.", color='k', linestyle=':', zorder=1)
            #legends.append(muf_astro_leg)
            #legends.append(p_cluster)
            #legends.append(p_tde)
            
                    
    else:

        data_ns_merger[:, 0] *= units.GeV
        data_ns_merger[:, 1] *= units.GeV * units.cm ** -2 * units.second ** -1 * units.sr ** -1

        ns_merger, = ax.plot(data_ns_merger[:, 0] / plotUnitsEnergy, data_ns_merger[:, 1] / plotUnitsFlux * flavorRatio, color='palevioletred', label='NS-NS merger, Fang & Metzger 1707.04263', linestyle=(0, (3, 5, 1, 5)))

        ax.fill_between(tde[:, 0] * units.GeV / plotUnitsEnergy, tde[:, 2] * 3 * flavorRatio, tde[:, 3] * 3, color='thistle', alpha=0.5)
        p_tde, = ax.plot(tde[:, 0] * units.GeV / plotUnitsEnergy, tde[:, 1] * 3 * flavorRatio, label="TDE, Biehl et al. (1711.03555)", color='darkmagenta', linestyle=':', zorder=1)

        ax.fill_between(ll_grb[:, 0] * units.GeV / plotUnitsEnergy, ll_grb[:, 2] * 3 * flavorRatio, ll_grb[:, 3] * 3, color='0.8')
        p_ll_grb, = ax.plot(ll_grb[:, 0] * units.GeV / plotUnitsEnergy, ll_grb[:, 1] * 3 * flavorRatio, label="LLGRB, Boncioli et al. (1808.07481)", linestyle='-.', c='k', zorder=1)

        p_pulsar = ax.fill_between(pulsars[:, 0] * units.GeV / plotUnitsEnergy, pulsars[:, 1]* flavorRatio, pulsars[:, 2] * flavorRatio, label="Pulsar, Fang et al. (1311.2044)", color='wheat', alpha=0.5)
        p_cluster, = ax.plot(clusters[:, 0] * units.GeV / plotUnitsEnergy, clusters[:, 1]* flavorRatio, label="Clusters, Fang & Murase, (1704.00015)", color="olive", zorder=1, linestyle=(0, (5, 10)))

        first_legend = plt.legend(handles=[p_tde, p_ll_grb, p_pulsar, p_cluster, ns_merger], loc=3, fontsize=legendfontsize, handlelength=3)

        #plt.gca().add_artist(first_legend)
    #-----------------------------------------------------------------------
    second_legend = []
    #textleg, = ax.plot([],[], ' ', label=r"\textbf{Particle showers}")
    #second_legend.append(textleg)
    if show_tambo:
        tamboleg, = ax.plot(TAMBO_energy / plotUnitsEnergy, TAMBO/plotUnitsFlux, linestyle="-.", color='#0D6759', label='TAMBO')
        #ax.annotate('BEACON-1k',
        #            xy=(7e9, 4e-10), xycoords='data',
        #            horizontalalignment='left', color='#F97807', rotation=35, fontsize=1.3*legendfontsize)
        second_legend.append(tamboleg)
    #textleg, = ax.plot([],[], ' ', label=r"\textbf{Optical/Fluorescence}")
    #second_legend.append(textleg)       
    if show_trinity:
        trinityleg, = ax.plot(Trinity_energy / plotUnitsEnergy, Trinity_E2F/plotUnitsFlux, linestyle='--', color='#57B155', label='Trinity 18')
        #ax.annotate('Trinity x 3',
        #            xy=(9e6, 1e-9), xycoords='data',
        #            horizontalalignment='left', color='#57B155', rotation=-20, fontsize=1.3*legendfontsize)
        second_legend.append(trinityleg)
        
    if show_ska:
        skaleg, = ax.plot(lofar_energy / plotUnitsEnergy, lofar_flux/plotUnitsFlux, linestyle='--', color="#667D8C", label='SKA, 200 hours')
        second_legend.append(skaleg)
        
    if show_poemma:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        poemmaleg, = ax.plot(POEMMA_energy / plotUnitsEnergy, POEMMA / plotUnitsFlux, linestyle="-.", color='#3FA33F', label='POEMMA30 (5 years)')
        #ax.annotate('POEMMA 360 (5 years)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        second_legend.append(poemmaleg)
    
    if show_poemma_fluor:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        poemmaleg, = ax.plot(POEMMA_fluor_energy / plotUnitsEnergy, POEMMA_fluor_flux / plotUnitsFlux, linestyle="-.", color='#3FA33F')
        #ax.annotate('POEMMA 360 (5 years)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        second_legend.append(poemmaleg)
        
    if show_poemma360:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        poemma360leg, = ax.plot(POEMMA360_energy / plotUnitsEnergy, POEMMA360 / plotUnitsFlux, linestyle=":", color='#3FA33F', label='POEMMA30(x12) Cherenkov (5 year mission)')
        #ax.annotate('POEMMA 360 (5 years)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        second_legend.append(poemma360leg)
        
    
    #textleg, = ax.plot([],[], ' ', label=r"\textbf{Earth-skimming radio}")
    #second_legend.append(textleg)   
    if show_grand_10k:
        grand10kleg, = ax.plot(GRAND_energy / plotUnitsEnergy, GRAND_10k / plotUnitsFlux, linestyle="--", color='#FD971E', label='GRAND 10k')
#         if energyBinsPerDecade == 2:
#             ax.annotate('GRAND 10k',
#                             xy=(0.9e10 * units.GeV / plotUnitsEnergy, 2e-8), xycoords='data',
#                             horizontalalignment='left', color='#FD971E', rotation=50, fontsize=legendfontsize)
        # else:
#             ax.annotate('GRAND 10k',
#                 xy=(1.2e19 * units.eV / plotUnitsEnergy, 5e-8), xycoords='data',
#                 horizontalalignment='left', va="top", color='#FD971E', rotation=47, fontsize=legendfontsize)
        second_legend.append(grand10kleg)
    if show_grand_200k:
        grand200kleg, = ax.plot(GRAND_energy / plotUnitsEnergy, GRAND_200k / plotUnitsFlux, linestyle="--", color='#FD971E', label='GRAND 200k')
       #  ax.annotate('GRAND 200k',
#                     xy=(1e10 * units.GeV / plotUnitsEnergy, 6e-9), xycoords='data',
#                     horizontalalignment='left', color='saddlebrown', rotation=40, fontsize=legendfontsize)
        second_legend.append(grand200kleg)
    if show_beacon:
        beaconleg, = ax.plot(BEACON_energy / plotUnitsEnergy, BEACON_LF_1000/plotUnitsFlux, linestyle="-.", color='#F97807', label='BEACON 1k')
        #ax.annotate('BEACON-1k',
        #            xy=(7e9, 4e-10), xycoords='data',
        #            horizontalalignment='left', color='#F97807', rotation=35, fontsize=1.3*legendfontsize)
        second_legend.append(beaconleg)
    if show_taroge:
        tarogeleg, = ax.plot(taroge_m_E / plotUnitsEnergy, taroge_m_flux / plotUnitsFlux, linestyle=(0, (3, 1, 1, 1, 1, 1)), color='#F06609', label='TAROGE-M 10')
        second_legend.append(tarogeleg)
    
    if show_anita_I_III_limit:
        ax.plot(anita_limit[:, 0] / plotUnitsEnergy, anita_limit[:, 1] / plotUnitsFlux, color='darkorange')
        if energyBinsPerDecade == 2:
            ax.annotate('ANITA I - III',
                        xy=(7e9 * units.GeV / plotUnitsEnergy, 1e-6), xycoords='data',
                        horizontalalignment='left', color='darkorange', fontsize=legendfontsize)
        else:
            ax.annotate('ANITA I - III',
                        xy=(7e9 * units.GeV / plotUnitsEnergy, 5e-7), xycoords='data',
                        horizontalalignment='left', color='darkorange', fontsize=legendfontsize)
        
    if show_anita_I_IV_limit:
        ax.plot(anita_i_iv_limit[:, 0] / plotUnitsEnergy, anita_i_iv_limit[:, 1] / plotUnitsFlux, color='grey', linewidth=4, alpha=0.5)
        if energyBinsPerDecade == 2:
            ax.annotate('ANITA I-IV',
                        xy=(7e9 * units.GeV / plotUnitsEnergy, 1e-6), xycoords='data',
                        horizontalalignment='left', color='grey', fontsize=legendfontsize)
        else:
            ax.annotate('ANITA I-IV',
                        xy=(2E18 * units.eV / plotUnitsEnergy, 1.2e-6* 3.0 * flavorRatio), xycoords='data',
                        horizontalalignment='left', color='grey', fontsize=labelfontsize, rotation=-55, alpha=0.75)
    if show_pueo30:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        pueo30leg, = ax.plot(PUEO30_energy / plotUnitsEnergy, PUEO30 / plotUnitsFlux, linestyle="--", color='green', label='PUEO (1 flight, 30 days)')
        #ax.annotate('PUEO 100 days (3 flights)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='#FB3F1A', rotation=15)

        ax.annotate('PUEO',
                            xy=(3.4E19, 3.4E-8), xycoords='data',
                            horizontalalignment='left', color='green', rotation=0, fontsize=15,
                            )



        second_legend.append(pueo30leg)
    
    if show_pueo100:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        pueo100leg, = ax.plot(PUEO100_energy / plotUnitsEnergy, PUEO100 / plotUnitsFlux, linestyle=(0, (3, 1, 1, 1, 1, 1)), color='#EA5A06', label='PUEO (3 flights, 100 days)')
        #ax.annotate('PUEO 100 days (3 flights)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='#FB3F1A', rotation=15)

        second_legend.append(pueo100leg)

        #textleg, = ax.plot([],[], ' ', label=r"\textbf{In-ice Radio}")  
        #second_legend.append(textleg) 
        #second_legend.append(pueo100leg)   
        
    if show_ice_cube_EHE_limit:
        ax.plot(ice_cube_limit[2:, 0] / plotUnitsEnergy, ice_cube_limit[2:, 1] / plotUnitsFlux * flavorRatio, color='grey', linewidth=4, alpha=0.5)

    if show_ice_cube_EHE_limit_2025:
        ax.plot(ice_cube_limit_25[2:, 0] / plotUnitsEnergy, ice_cube_limit_25[2:, 1] / plotUnitsFlux * flavorRatio, color='grey', linewidth=4, alpha=1)
        ax.annotate('IceCube',
                xy=(4e16 * units.eV / plotUnitsEnergy, 1e-9 * 3.0 * flavorRatio), xycoords='data',
                horizontalalignment='center', color='grey', rotation=5, fontsize=labelfontsize, alpha=1)


    if show_ice_cube_HESE_data:
        # data points
        uplimit = np.copy(ice_cube_hese[:, 3])
        uplimit[np.where(ice_cube_hese[:, 3] == 0)] = 1
        uplimit[np.where(ice_cube_hese[:, 3] != 0.)] = 0

        the_x_errs = np.diff(ice_cube_hese[:, 0]/2)
        # For plotting, we need to pad the array to match the length of 'a'
        the_x_errs = np.insert(the_x_errs, 0, the_x_errs[0])  # Duplicate first value for same length


        heseleg = ax.errorbar(ice_cube_hese[:, 0] / plotUnitsEnergy, 
                              ice_cube_hese[:, 1] / plotUnitsFlux, 
                              yerr=ice_cube_hese[:, 2:].T / plotUnitsFlux, 
                              uplims=uplimit, 
                              xerr=the_x_errs,
                              # color='#5CACE2', 
                              color="purple", alpha=0.5,
                              marker='o', markersize=4, ecolor='purple', linestyle='None', zorder=3,
                              label="Astro: IceCube and KM3NeT data"
                    )
        from matplotlib.lines import Line2D

        # Create errorbar-style markers with both vertical and horizontal bars
        purple_marker = Line2D([0], [0], marker='+', color='purple', 
                            markersize=14, markeredgewidth=2,
                            linestyle='', alpha=0.7)
        orange_marker = Line2D([0], [0], marker='+', color='C1', 
                            markersize=14, markeredgewidth=2,
                            linestyle='', alpha=0.7)

        legends.append((purple_marker, orange_marker))

        # legends.append(heseleg)

                    
    if show_ice_cube_HESE_fit:
        ice_cube_hese_range = get_ice_cube_hese_range()
        heseleg = ax.fill_between(IC_Cascades2020_en / plotUnitsEnergy, *IC_Cascades2020_flux, edgecolor='#5CACE2', facecolor='azure', alpha=0.7, zorder=2, label="Astro: IceCube and KM3NeT measurements")
        legends.append(heseleg)
        #ax.plot(ice_cube_hese_range[0] / plotUnitsEnergy, ice_cube_nu_fit(ice_cube_hese_range[0],
        #                                                                   offset=6.7*flavorRatio, slope=-2.5) * ice_cube_hese_range[0] ** 2 / plotUnitsFlux, color='#5CACE2')

        
        if energyBinsPerDecade == 2:
            flimflam=1
            # ax.annotate('IceCube',
            #         xy=(3e6 * units.GeV / plotUnitsEnergy, 4e-8), xycoords='data',
            #         horizontalalignment='center', color='grey', rotation=0, fontsize=labelfontsize)
        else:
            # ax.annotate('IceCube',
            #         xy=(10e15 * units.eV / plotUnitsEnergy, 4.5e-9 * 3.0 * flavorRatio), xycoords='data',
            #         horizontalalignment='center', color='grey', rotation=20, fontsize=labelfontsize)
            flimflam=1
            # ax.annotate('IceCube',
            #         xy=(4e16 * units.eV / plotUnitsEnergy, 7.2e-9 * 3.0 * flavorRatio), xycoords='data',
            #         horizontalalignment='center', color='grey', rotation=5, fontsize=labelfontsize, alpha=0.75)

    if show_ice_cube_mu:
        # mu fit
        ice_cube_mu_range = get_ice_cube_mu_range()
        #ax.fill_between(ice_cube_mu_range[0] / plotUnitsEnergy, ice_cube_mu_range[1] / plotUnitsFlux,
        #                ice_cube_mu_range[2] / plotUnitsFlux, hatch='\\', edgecolor='#5CACE2', facecolor='azure', alpha=0.7, zorder=2)
        ax.fill_between(IC_numu2021_en / plotUnitsEnergy, IC_numu2021_flux_min / plotUnitsFlux, IC_numu2021_flux_max / plotUnitsFlux,
                        hatch='\\', edgecolor='#5CACE2', facecolor='azure', alpha=0.7, zorder=2)
        #ax.plot(ice_cube_mu_range[0] / plotUnitsEnergy,
        #         ice_cube_nu_fit(ice_cube_mu_range[0]) * ice_cube_mu_range[0] ** 2 / plotUnitsFlux,
        #         color='#5CACE2')

        ax.annotate('IceCube',
                    xy=(4e4 * units.GeV / plotUnitsEnergy, 5), xycoords='data',
                    horizontalalignment='center', color='grey', rotation=0, fontsize=legendfontsize)

        uplimit = np.copy(nu_mu_data[:, 3])
        uplimit[np.where(nu_mu_data[:, 3] == 0)] = 1
        uplimit[np.where(nu_mu_data[:, 3] != 0.)] = 0

        if nu_mu_show_data_points:            
            ax.errorbar(nu_mu_data[:, 0] / plotUnitsEnergy, nu_mu_data[:, 1] / plotUnitsFlux,
                        yerr=nu_mu_data[:, 2:].T / plotUnitsFlux, uplims=uplimit, color='purple',
                        alpha=0.5, marker='o', ecolor='purple', linestyle='None', zorder=3,
                        markersize=7)
                        
    if show_ice_cube_mu_extrap:
        # Extrapolation
        energy_placeholder = np.array(([1e14, 1e19])) * units.eV
        plt.plot(energy_placeholder / plotUnitsEnergy,
                 ice_cube_nu_fit(energy_placeholder) * energy_placeholder ** 2 / plotUnitsFlux,
                 color='#5CACE2', linestyle=':')


    if show_icecube_glashow:
        # only plot the Glashow data point (the first (0) and last (2) entries are upper limits)
        point = 1
        glashow_x = (i3_glashow_emax[point] - i3_glashow_emin[point]) / 2 + i3_glashow_emin[point]
        glashow_y = i3_glashow_y[point]
        ax.errorbar(
            x=glashow_x,
            y=glashow_y,
            xerr=[[glashow_x - i3_glashow_emin[point]], [i3_glashow_emax[point] - glashow_x]],
            yerr=[[glashow_y - i3_glashow_y_lower[point]], [i3_glashow_y_upper[point] - glashow_y]],
            marker='o', markersize=7, color='#5CACE2', ecolor='#5CACE2',
            )

 

    if show_eusospb:
        #ax.plot(PUEO_energy / plotUnitsEnergy, PUEO / plotUnitsFlux, linestyle="--", color='goldenrod')
        #ax.annotate('PUEO 30 days',xy=(1.5e11, 4.e-8), xycoords='data',horizontalalignment='left', color='goldenrod', rotation=15)
        
        eusospbleg, = ax.plot(EUSOSPB_energy / plotUnitsEnergy, EUSOSPB / plotUnitsFlux, linestyle=(0, (3, 1, 1, 1, 1, 1)), color='#389237', label='EUSO-SPB (1 flight, 100 days)')
        #ax.annotate('EUSO SBP (100 days, 1 flight)',xy=(1.5e11, 1.5e-8), xycoords='data',horizontalalignment='left', color='black', rotation=15)
        second_legend.append(eusospbleg)
        
    if show_auger_limit:
        augerleg, = ax.plot(auger_limit[:, 0] / plotUnitsEnergy, auger_limit[:, 1] / plotUnitsFlux, color='grey', linewidth=4, alpha=0.5)
        if energyBinsPerDecade == 2:
            ax.annotate('Auger',
                        xy=(8e16 * units.eV / plotUnitsEnergy, 2.1e-7), xycoords='data',
                        horizontalalignment='left', color='grey', rotation=0, fontsize=labelfontsize)
        else:
            ax.annotate('Auger',
                        xy=(1.2e17 * units.eV / plotUnitsEnergy, 1.3e-8* 3.0 * flavorRatio), xycoords='data',
                        horizontalalignment='right', color='grey', rotation=-45,fontsize=labelfontsize, alpha=0.75)
        second_legend.append(augerleg)
        
    if show_ara_1year:
        ax.plot(ara_1year[:, 0] / plotUnitsEnergy, ara_1year[:, 1] / plotUnitsFlux, color='indigo')
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        if energyBinsPerDecade == 2:
            ax.annotate('ARA',
                        xy=(1.7e8 * units.GeV / plotUnitsEnergy, 6e-7), xycoords='data',
                        horizontalalignment='left', color='indigo', rotation=0, fontsize=labelfontsize)
        else:
            ax.annotate('ARA',
                    xy=(0.6e10 * units.GeV / plotUnitsEnergy, 1.05e-6* 3.0 * flavorRatio), xycoords='data',
                    horizontalalignment='left', color='indigo', rotation=0, fontsize=labelfontsize)
    if show_ara:
        ax.plot(ara_4year_E / plotUnitsEnergy, ara_4year_limit / plotUnitsFlux, color='grey', linewidth=4, alpha=0.5)
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        if energyBinsPerDecade == 2:
            ax.annotate('ARA',
                        xy=(5e8 * units.GeV / plotUnitsEnergy, 6e-7* 3.0 * flavorRatio), xycoords='data',
                        horizontalalignment='left', color='grey', rotation=0, fontsize=labelfontsize)
        else:
            ax.annotate('ARA',
                    xy=(7e16 * units.eV / plotUnitsEnergy, 2e-6* 3.0 * flavorRatio), xycoords='data',
                    horizontalalignment='right', color='grey', rotation=-60,  fontsize=labelfontsize, alpha=0.75)
    
    if show_ara_2023:
        ara2023leg, = ax.plot(ara_2023_E / plotUnitsEnergy, ara_2023_limit / plotUnitsFlux, color='#E94880', linestyle='--', label='ARA by 2023')
        # if energyBinsPerDecade == 2:
#             ax.annotate('ARA 2023',
#                         xy=(2E16 * units.eV / plotUnitsEnergy, 6e-7), xycoords='data',
#                         horizontalalignment='left', color='grey', rotation=0, fontsize=legendfontsize)
#         else:
#             ax.annotate('ARA 2023',
#                     xy=(4E17 * units.eV / plotUnitsEnergy, 6e-8), xycoords='data',
#                     horizontalalignment='left', color='grey', rotation=0, fontsize=legendfontsize)
        second_legend.append(ara2023leg)
    if show_ara_2023_TL:
        ara2023tlleg, = ax.plot(ara_2023_E_TL / plotUnitsEnergy, ara_2023_limit_TL / plotUnitsFlux, color='grey', linestyle='--')
        if energyBinsPerDecade == 2:
            ax.annotate('ARA 2023 \n(TL)',
                        xy=(1E16 * units.eV / plotUnitsEnergy, 6e-7), xycoords='data',
                        horizontalalignment='left', color='grey', rotation=0, fontsize=legendfontsize)
        else:
            ax.annotate('ARA 2023 \n(TL)',
                    xy=(1E16 * units.eV / plotUnitsEnergy, 6e-8), xycoords='data',
                    horizontalalignment='left', color='grey', rotation=0, fontsize=legendfontsize)
        second_legend.append(ara2023tlleg)
    if show_arianna:
        ax.plot(ARIANNA_HRA[:, 0] / plotUnitsEnergy, ARIANNA_HRA[:, 1] / plotUnitsFlux, color='grey', linewidth=4, alpha=0.5)
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        if energyBinsPerDecade == 2:
            ax.annotate('ARIANNA',
                        xy=(2e8 * units.GeV / plotUnitsEnergy, 6e-6), xycoords='data',
                        horizontalalignment='left', color='grey', rotation=0, fontsize=labelfontsize)
        else:
            ax.annotate('ARIANNA',
                    xy=(0.5e16 * units.eV / plotUnitsEnergy, 2.2E-6* 3.0 * flavorRatio), xycoords='data',
                    horizontalalignment='left', color='grey', rotation=-36, fontsize=labelfontsize, alpha=0.75)
        
    if show_RNOG:
        rnogleg, = ax.plot(RNOG_E / plotUnitsEnergy, RNOG_flux / 0.7 / plotUnitsFlux, color='#E42467', linestyle="-.", label='RNO-G')  # uses 70% uptime from RNO-G whitepaper and resacling to 10years
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #ax.annotate('RNO-G',
        #            xy=(8e18 * units.eV / plotUnitsEnergy, 1e-8), xycoords='data',
        #            horizontalalignment='left', va="top", color='red', rotation=10, fontsize=legendfontsize)
        second_legend.append(rnogleg)
    if show_prediction_arianna_200:
        arianna200leg, = ax.plot(arianna_200[:, 0] / plotUnitsEnergy, arianna_200[:, 1] / plotUnitsFlux, label='ARIANNA-200 (5 years)', color='#F48FB1', linestyle="--")
        ax.annotate('ARIANNA-200',
                    xy=(.9e19 * units.eV / plotUnitsEnergy, 1e-9), xycoords='data',
                    horizontalalignment='left', color='blue', rotation=30, fontsize=legendfontsize)

        second_legend.append(arianna200leg)
    
    if show_radar:
        #ax.fill_between(Radar[:, 0] / plotUnitsEnergy, Radar[:, 1] / plotUnitsFlux,
        #                Radar[:, 2] / plotUnitsFlux, facecolor='None', hatch='x', edgecolor='0.8')
        radarleg, = ax.plot(Radar[:, 0] / plotUnitsEnergy, Radar[:, 1] / plotUnitsFlux, linestyle=(0, (3, 1, 1, 1, 1, 1)), color='#E2004F', label='RET-N 10 x 100 kW Preliminary')
        #ax.annotate('Radar Preliminary',
        #            xy=(1e9 * units.GeV / plotUnitsEnergy, 4.5e-8), xycoords='data',
        #            horizontalalignment='left', color='0.7', rotation=45, fontsize=legendfontsize)
        second_legend.append(radarleg)
    

    if show_IceCubeGen2_whitepaper:
        gen2wpleg, = ax.plot(gen2_E / plotUnitsEnergy, gen2_flux / 2 / plotUnitsFlux, color='purple', linestyle=":")
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #ax.annotate('IceCube-Gen2 radio',
        #            xy=(.8e8 * units.GeV / plotUnitsEnergy, 1.6e-10), xycoords='data',
        #            horizontalalignment='left', color='purple', rotation=0, fontsize=legendfontsize)
        second_legend.append(gen2wpleg)
        
    if show_IceCubeGen2_ICRC2021:
        # https://pos.sissa.it/395/1183/
        # flux limit for 10 years
        gen2icrc2021, = ax.plot(gen2radio_E / plotUnitsEnergy, gen2radio_flux / plotUnitsFlux, color='#8801A0', linestyle="--", label='IceCube-Gen2 radio')
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #   ax.annotate('IceCube-Gen2 radio',
        #            xy=(.8e8 * units.GeV / plotUnitsEnergy, 1.6e-10), xycoords='data',
        #            horizontalalignment='left', color='purple', rotation=0, fontsize=legendfontsize)
        second_legend.append(gen2icrc2021)
    
    if show_IceCubeGen2_combo:
        # https://pos.sissa.it/395/1183/
        # flux limit for 10 years
        gen2combo, = ax.plot(gen2_E / plotUnitsEnergy, gen2_flux / plotUnitsFlux, color='#8801A0', linestyle="--", label='IceCube-Gen2 UHE')
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #   ax.annotate('IceCube-Gen2 radio',
        #            xy=(.8e8 * units.GeV / plotUnitsEnergy, 1.6e-10), xycoords='data',
        #            horizontalalignment='left', color='purple', rotation=0, fontsize=legendfontsize)
        second_legend.append(gen2combo)
        
    #textleg, = ax.plot([],[], ' ', label=r"\textbf{In-ice Optical + Radio}")
    #second_legend.append(textleg)   
    if show_IceCubeGen2_proj:

        gen2proj = ax.errorbar(gen2proj_en / plotUnitsEnergy, gen2proj_flux / plotUnitsFlux, yerr=gen2proj_flux_lims / plotUnitsFlux, color='#8801A0', linestyle='', marker='o', label='IceCube-Gen2')
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #   ax.annotate('IceCube-Gen2 radio',
        #            xy=(.8e8 * units.GeV / plotUnitsEnergy, 1.6e-10), xycoords='data',
        #            horizontalalignment='left', color='purple', rotation=0, fontsize=legendfontsize)
        second_legend.append(gen2proj)
        
        #gen2projpgamma = ax.errorbar(gen2projpgamma_en / plotUnitsEnergy, gen2projpgamma_flux / plotUnitsFlux, yerr=gen2projpgamma_flux_lims / plotUnitsFlux, color='#8801A0', linestyle='', marker='s', label='IceCube-Gen2 MMA astrophys. + cosmogenic', alpha=1.0)
#         ax.plot(ara_4year[:,0]/plotUnitsEnergy,ara_4year[:,1]/ plotUnitsFlux,color='indigo',linestyle='--')
        #   ax.annotate('IceCube-Gen2 radio',
        #            xy=(.8e8 * units.GeV / plotUnitsEnergy, 1.6e-10), xycoords='data',
        #            horizontalalignment='left', color='purple', rotation=0, fontsize=legendfontsize)
        #second_legend.append(gen2projpgamma)
        
    print(second_legend)
    # legend_2 = ax.legend(handles=second_legend, loc='upper left', fontsize=legendfontsize, handlelength=4, labelspacing=0.2)

    legends.reverse()

    # data_transgzk = np.genfromtxt("data/trans_gzk_protons.csv",delimiter=",", names=["energy", "flux"])
    # leg_transgz, = ax.plot(data_transgzk["energy"], data_transgzk["flux"], '-', color="blue", lw=2, alpha=0.65, label = "Trans-GZK Protons")

    # muzio best fit stuff
    # data_muzio_100PeV = np.genfromtxt("data/bestfit_IC_KM3NeTmid_xmaxShift_sibyll_retuneNuSum.txt",
    #                                 names=["E", "f", "e", "mu", "tau", "low"]
    #                                 )
    # ax.plot(10**data_muzio_100PeV["E"], data_muzio_100PeV["f"], color="cyan")

    data_pulsars = np.genfromtxt("data/pulsars.csv",delimiter=",", names=["energy", "flux"])
    leg_pulars, = ax.plot(data_pulsars["energy"], data_pulsars["flux"], '-', color="blue", lw=2, alpha=0.65, label="Pulsars")

    data_agn = np.genfromtxt("data/agn.csv",delimiter=",", names=["energy", "flux"])
    leg_agn, = ax.plot(data_agn["energy"], data_agn["flux"], '--', color="blue", lw=2, alpha=0.65, label="AGN")
 
    data_bllacs = np.genfromtxt("data/bllacs.csv",delimiter=",", names=["energy", "flux"])
    leg_bllacs, = ax.plot(data_bllacs["energy"], data_bllacs["flux"], '-.', color="blue", lw=2, alpha=0.65, label="BL Lacs")

    data_brl_inside = np.genfromtxt("data/blr_inside.txt",delimiter=",", names=["energy", "flux"])
    leg_brl_inside, = ax.plot(data_brl_inside["energy"]*1E9, data_brl_inside["flux"], linestyle=(0, (3, 1, 1, 1)), color="blue", lw=2, alpha=0.65, label="FSRQ (In BLR)")

    data_brl_outside = np.genfromtxt("data/blr_outside.txt",delimiter=",", names=["energy", "flux"])
    leg_brl_outside, = ax.plot(data_brl_outside["energy"]*1E9, data_brl_outside["flux"], linestyle=(0, (3, 5, 1, 5, 1, 5)), color="blue", lw=2, alpha=0.65, label="FSRQ (Out BLR)")

    data_muzio_1EeV = np.genfromtxt("data/bestfit_IC_KM3NeThi_xmaxShift_UHEp_sibyll_retuneNuSum.txt",
                                    names=["E", "f", "e", "mu", "tau", "low"]
                                    )
    leg_muziokm3, = ax.plot(10**data_muzio_1EeV["E"], data_muzio_1EeV["f"], ":", color="blue", lw=2, label=r"CR-$\nu$ Joint Fit")

    # legends.append(leg_transgz)
    legends.append(leg_pulars)
    legends.append(leg_agn)
    legends.append(leg_bllacs)
    legends.append(leg_muziokm3)
    legends.append(leg_brl_inside)
    legends.append(leg_brl_outside)

    # first_legend = plt.legend(handles=legends, loc='lower left', fontsize=legendfontsize, handlelength=3, ncol=2)
    # plt.gca().add_artist(first_legend)
    # Extract labels from legend handles (needed because some handles may be tuples)
    legend_labels = []
    for h in legends:
        if isinstance(h, tuple):
            legend_labels.append("Astro: IceCube and KM3NeT data")
        else:
            legend_labels.append(h.get_label())

    first_legend = plt.legend(handles=legends, labels=legend_labels, loc='lower left', 
                            fontsize=legendfontsize, handlelength=3, ncol=2,
                            handler_map={tuple: HandlerTuple(ndivide=None)})
    plt.gca().add_artist(first_legend)

    return fig, ax


def add_limit(ax, limit_labels, E, Veffsr, n_stations, label, livetime=3 * units.year, linestyle='-', color='r', linewidth=3, band=False):
    """
    add limit curve to limit plot
    """
    E = np.array(E)
    Veffsr = np.array(Veffsr)

    if band:

        limit_lower = fluxes.get_limit_e2_flux(energy=E,
                                         veff_sr=Veffsr[0],
                                         livetime=livetime,
                                         signalEff=n_stations,
                                         energyBinsPerDecade=energyBinsPerDecade,
                                         upperLimOnEvents=2.44,
                                         nuCrsScn='ctw')
        limit_upper = fluxes.get_limit_e2_flux(energy=E,
                                         veff_sr=Veffsr[1],
                                         livetime=livetime,
                                         signalEff=n_stations,
                                         energyBinsPerDecade=energyBinsPerDecade,
                                         upperLimOnEvents=2.44,
                                         nuCrsScn='ctw')

        plt1 = ax.fill_between(E / plotUnitsEnergy, limit_upper / plotUnitsFlux,
        limit_lower / plotUnitsFlux, color=color, alpha=0.2)

    else:

        limit = fluxes.get_limit_e2_flux(energy=E,
                                         veff_sr=Veffsr,
                                         livetime=livetime,
                                         signalEff=n_stations,
                                         energyBinsPerDecade=energyBinsPerDecade,
                                         upperLimOnEvents=2.44,
                                         nuCrsScn='ctw')

    #         _plt, = ax.plot(E/plotUnitsEnergy,limit/ plotUnitsFlux, linestyle=linestyle, color=color,
    #                         label="{2}: {0} stations, {1} years".format(n_stations,int(livetime/units.year),label),
    #                         linewidth=linewidth)
        _plt, = ax.plot(E / plotUnitsEnergy, limit / plotUnitsFlux, linestyle=linestyle, color=color,
                        label="{1}: {0} years".format(int(livetime / units.year), label),
                        linewidth=linewidth)

        limit_labels.append(_plt)

    return limit_labels


if __name__ == "__main__":
    # 50 meter
    veff = np.array((
    [1e+16, 3.162277660168379e+16, 1e+17, 3.1622776601683795e+17, 1e+18, 3.1622776601683794e+18, 1e+19, 3.162277660168379e+19],
    [0.007467602898257461, 0.06986834193426224, 0.5333379226865426, 2.1410489793474383, 5.896654567671568, 11.343574036186226, 18.415350759353128, 27.81614390854279]
    )).T

    veff[:, 0] *= units.eV
    veff[:, 1] *= units.km ** 3 * units.sr
    veff_label = 'One current design'

#     strawman_veff_pa = np.array(( [1.00000000e+16, 3.16227766e+16, 1.00000000e+17, 3.16227766e+17, 1.00000000e+18, 3.16227766e+18, 1.00000000e+19, 3.16227766e+19],
#                               [1.82805666e+07, 1.34497197e+08, 6.32044851e+08, 2.20387046e+09, 4.86050340e+09, 8.18585201e+09, 1.25636305e+10, 1.83360237e+10])).T
#
#     strawman_veff_pa[:,0] *= units.eV
#     strawman_veff_pa[:,1] *= units.m**3 * units.sr

#     strawman_pa_label = 'Strawman + PA@15m@2s'
#     strawman_pa_label = 'One current design'
    fig, ax = get_E2_limit_figure(diffuse=DIFFUSE,
                                  fig=None, ax=None,
                                                          show_ice_cube_EHE_limit=True,
                                                          show_ice_cube_HESE_data=True,
                                                          show_ice_cube_HESE_fit=True,
                                                          show_ice_cube_mu=True,
                                                          show_ice_cube_mu_extrap=False,
                                                          nu_mu_show_data_points=True,
                                                          show_icecube_glashow=False,
                                                          show_anita_I_III_limit=False,
                                                          show_anita_I_IV_limit=True,
                                                          show_pueo30=True,
                                                          show_pueo100=False,
                                                          show_poemma=True,
                                                          show_poemma_fluor=True,
                                                          show_poemma360=True,
                                                          show_eusospb=True,
                                                          show_auger_limit=True,
                                                          show_ara=False,
                                                          show_ara_2023=True,
                                                          show_ara_2023_TL=False,
                                                          show_arianna=False,
                                                          show_neutrino_best_fit=False,
                                                          show_neutrino_best_case=False,
                                                          show_neutrino_worst_case=False,
                                                          show_grand_10k=False,
                                                          show_grand_200k=True,
                                                          show_beacon=True,
                                                          show_taroge=True,
                                                          show_tambo=True,
                                                          show_trinity=True,
                                                          show_radar=True,
                                                          show_Heinze=False,
                                                          show_TA=False,
                                                          show_TA_nominal=False,
                                                          show_TA_ICRC2021=False,
                                                          show_RNOG=True,
                                                          show_IceCubeGen2_whitepaper=False,
                                                          show_IceCubeGen2_ICRC2021=True,
                                                          show_Auger_vanvliet=True,
                                                          show_ara_1year=False,
                                                          show_prediction_arianna_200=False,
                                                          show_mma_bestfit=True,
                                                          show_mma_pureproton=True,
                                                          show_astro=True)
    #labels = []
    #labels = add_limit(ax, labels, veff[:, 0], veff[:, 1], n_stations=100, livetime=5 * units.year, label=veff_label)
    #labels = add_limit(ax, labels, veff[:, 0], veff[:, 1], n_stations=1000, livetime=5 * units.year, label=veff_label)
    #plt.legend(handles=labels, loc=2)
    if DIFFUSE:
        name_plot = "Limit_diffuse.pdf"
    else:
        name_plot = "Limit_sources.pdf"
    #plt.savefig(name_plot)
    plt.show()