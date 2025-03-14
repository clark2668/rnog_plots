import numpy as np
import matplotlib.pyplot as plt
import scipy.constants

# This class based on Anna Nelles's plotting script:
# https://github.com/nu-radio/NuRadioMC/blob/138f8419e2db935bd07cb41d88ff2ea1b9ee99e1/NuRadioMC/examples/Sensitivities/E2_fluxes2.py
class LimitFigure:
    def __init__(self, figsize=(7, 6), xlims=(1e5, 1e11), ylims=(1e-11, 1e-5),
                 energy_units=1, flux_units=1, e_bins_per_decade=1, e_power=2,
                 font_size=12, tick_size=12):
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)

        self.ax.set_xscale('log')
        self.ax.set_yscale('log')

        self.ax.set_xlabel(r'Neutrino Energy [GeV]')
        if e_power==2:
            # self.ax.set_ylabel(r'$E^2 dN/(dE\ dA\ d\Omega\ dt)$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
            self.ax.set_ylabel(r'$E^2 \Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
        elif e_power==1:
            self.ax.set_ylabel(r'$E\ dN/(dE\ dA\ d\Omega\ dt)$ [cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
        else:
            raise ValueError("Invalid power ("+e_power+")")

        self.ax.set_xlim(*xlims)
        self.ax.set_ylim(*ylims)

        self.ax.title.set_fontsize(font_size)

        plt.tight_layout()

        self.ax.xaxis.label.set_fontsize(font_size)
        self.ax.yaxis.label.set_fontsize(font_size)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontsize(tick_size)

        self.e_power = e_power
        self.e_unit = energy_units
        self.f_unit = flux_units
        self.e_bins = e_bins_per_decade
        self.font_size = font_size
        
        self.neutrino_models = []
        self.custom_limits = []

    @staticmethod
    def _i3_nu_fit(energy, slope=-2.13, offset=0.9):
        flux = 3 * offset * (energy / (100 * 1e3))**slope * 1e-18
        return flux

    @classmethod
    def _get_i3_mu_range(cls):
        energy = np.arange(1e5, 5e6, 1e5)
        upper = np.maximum(cls._i3_nu_fit(energy, offset=0.9, slope=-2.),
                           cls._i3_nu_fit(energy, offset=1.2, slope=-2.13))
        lower = np.minimum(cls._i3_nu_fit(energy, offset=0.9, slope=-2.26),
                           cls._i3_nu_fit(energy, offset=0.63, slope=-2.13))
        return energy, upper, lower

    @classmethod
    def _get_i3_hese_range(cls):
        energy = np.arange(1e5, 5e6, 1e5)
        upper = np.maximum(cls._i3_nu_fit(energy, offset=2.46, slope=-2.63),
                           cls._i3_nu_fit(energy, offset=2.76, slope=-2.92))
        lower = np.minimum(cls._i3_nu_fit(energy, offset=2.46, slope=-3.25),
                           cls._i3_nu_fit(energy, offset=2.16, slope=-2.92))
        return energy, upper, lower

    units = {
        "eV":  1e-9,
        "keV": 1e-6,
        "MeV": 1e-3,
        "GeV": 1,
        "TeV": 1e3,
        "PeV": 1e6,
        
        "mm": 1e-1,
        "cm": 1,
        "m":  1e2,
        "km": 1e5,
        
        "ns": 1e-9,
        "us": 1e-6,
        "ms": 1e-3,
        "s":  1,
        "min": 60,
        "hr": 60*60,
        "yr": 365*24*60*60,
        
        "sr": 1,
    }

    @classmethod
    def _read_data(cls, file):
        energy_col = None
        flux_col = None
        min_col = None
        max_col = None
        e_power = None
        bins_per_decade = None
        data_type = None
        with open(file, 'r') as f:
            column_number = -1
            for line in f:
                line = line.rstrip()
                if line=='':
                    continue
                if not line.startswith('#'):
                    break
                line = line.strip('#')
                words = line.split()
                column_number += 1
                if 'data type:' in line.lower():
                    data_type = " ".join(words[2:]).lower()
                    continue
                if 'bins per decade' in line.lower():
                    bins_per_decade = float(words[-1])
                    continue
                if words[0].lower().startswith("column"):
                    column_number = -1
                    continue
                if words[0].lower()=='energy':
                    unit = words[1].strip('[').rstrip(']')
                    if unit not in cls.units:
                        raise ValueError("Unable to interpret unit "+words[2])
                    energy_unit = cls.units[unit]
                    energy_col = column_number
                elif words[0].lower()=='flux' and words[1].lower()!='band':
                    flux_unit = 1
                    for word in words[1:]:
                        word = word.strip('[').rstrip(']')
                        bits = word.split("^")
                        unit = bits[0]
                        power = float(bits[1]) if len(bits)>1 else 1
                        if unit not in cls.units:
                            raise ValueError("Unable to interpret unit ["+word+"]")
                        if unit.endswith('eV'):
                            e_power = power
                        elif unit.endswith('m'):
                            if power!=-2:
                                raise ValueError("Expected unit ["+word+"] to be to the -2 power")
                        else:
                            if power!=-1:
                                raise ValueError("Expected unit ["+word+"] to be to the -1 power")
                        flux_unit *= cls.units[unit]
                    flux_col = column_number
                elif 'minimum' in words:
                    min_col = column_number
                elif 'maximum' in words:
                    max_col = column_number

        data = np.loadtxt(file, comments='#')
        energies = data[:, energy_col] * energy_unit
        fluxes = data[:, flux_col] * flux_unit
        band_min = data[:, min_col] * flux_unit
        band_max = data[:, max_col] * flux_unit
        meta = {
            "energy_unit": energy_unit,
            "flux_unit": flux_unit,
            "energy_power": e_power,
            "data_type": data_type,
            "bins_per_decade": bins_per_decade
        }
        return energies, fluxes, band_min, band_max, meta


    def get_data(self, filename):
        energies, fluxes, band_min, band_max, meta = self._read_data(filename)
        energies /= self.e_unit
        fluxes /= self.f_unit
        band_min /= self.f_unit
        band_max /= self.f_unit
        e_power = self.e_power - 1 - meta['energy_power']
        fluxes *= energies**e_power
        band_min *= energies**e_power
        band_max *= energies**e_power
        if 'limit' in meta['data_type']:
            fluxes *= self.e_bins / meta['bins_per_decade']
            band_min *= self.e_bins / meta['bins_per_decade']
            band_max *= self.e_bins / meta['bins_per_decade']
        return energies, fluxes, band_min, band_max


    def add_model(self, name):
        if name=='heinze':
            energy, flux, band_min, band_max = self.get_data('models/heinze_cr.txt')
            heinze, = self.ax.plot(energy, flux,
                                   color='black', linestyle='-.',
                                   label=r'Best fit, Heinze et al.')
            #                        label=r'Best fit UHECR ($\pm$ 3$\sigma$), Heinze et al.')
            # self.ax.fill_between(energy, band_min, band_max,
            #                      color='0.8')
            self.neutrino_models.append(heinze)

        elif name=='van_vliet':
            energy, flux, band_min, band_max = self.get_data('models/van_vliet_10.txt')
            prot10, = self.ax.plot(energy, flux,
                                   color='orchid', linestyle='-.',
                                   label=r'10% protons, van Vliet et al.')
            # prot = self.ax.fill_between(energy, band_min, band_max,
            #                             color='orchid', alpha=0.25,
            #                             label=r'not excluded from UHECRs')
            # self.neutrino_models.append(prot)
            self.neutrino_models.append(prot10)

        elif name=='ahlers':
            energy, flux, _, _ = self.get_data('models/ahlers_100.txt')
            prot100, = self.ax.plot(energy, flux,
                                    color='mediumblue', linestyle='-.',
                                    label=r'100% protons, Ahlers & Halzen')
            energy, flux, _, _ = self.get_data('models/ahlers_10.txt')
            prot10, = self.ax.plot(energy, flux,
                                   color='royalblue', linestyle='-.',
                                   label=r'10% protons, Ahlers & Halzen')
            # energy, flux, _, _ = self.get_data('sensitivities/ahlers_1.txt')
            # prot1, = self.ax.plot(energy, flux,
            #                       color='cornflowerblue', linestyle='-.',
            #                       label=r'1% protons, Ahlers & Halzen') # (1208.4181)
            # self.neutrino_models.extend([prot100, prot10, prot1])
            self.neutrino_models.extend([prot100, prot10])

        elif name=='kotera':
            energy, _, band_min, band_max = self.get_data('models/kotera_band.txt')
            compositions = self.ax.fill_between(energy, band_min, band_max,
                                                color='cornflowerblue', alpha=0.25,
                                                label=r'UHECR, Olinto et al.')

            energy, flux, _, _ = self.get_data('models/kotera_high_e.txt')
            kotera_high, = self.ax.plot(energy, flux,
                                        color='darkblue', linestyle='--',
                                        label=r'SFR $E_{max}=10^{21.5}$, Kotera et al.') # (1009.1382)

            # energy, flux, _, _ = self.get_data('sensitivities/kotera_mid.txt')
            # kotera, = self.ax.plot(energy, flux,
            #                        color='darkmagenta', linestyle='--',
            #                        label=r'SFR $E_{max}=10^{20.5}$, Kotera et al.') # (1009.1382)
            self.neutrino_models.extend([compositions, kotera_high])
            # self.neutrino_models.extend([compositions, kotera_high, kotera])

        elif name=='fang_merger':
            energy, flux, _, _ = self.get_data('models/fang_ns_merger.txt')
            ns_merger, = self.ax.plot(energy, flux,
                                      color='palevioletred', linestyle=(0, (3, 5, 1, 5)),
                                      label='NS-NS merger, Fang & Metzger') # (1707.04263)
            self.neutrino_models.append(ns_merger)

        elif name=='fang_pulsar':
            energy, _, band_min, band_max = self.get_data('models/fang_pulsar.txt')
            p_pulsar = self.ax.fill_between(energy, band_min, band_max,
                                            color='pink', alpha=0.5,
                                            label="Pulsar, Fang et al.") # (1311.2044)
            self.neutrino_models.append(p_pulsar)
            
        elif name=='fang_cluster':
            energy, flux, _, _ = self.get_data('models/fang_cluster.txt')
            p_cluster, = self.ax.plot(energy, flux,
                                      color="mediumvioletred", zorder=1, linestyle=(0, (5, 10)),
                                      label="Clusters, Fang & Murase") # (1704.00015)
            self.neutrino_models.append(p_cluster)

        elif name=='biehl':
            energy, flux, band_min, band_max = self.get_data('models/biehl_tde.txt')
            self.ax.fill_between(energy, band_min, band_max,
                                 color='thistle', alpha=0.5)
            p_tde, = self.ax.plot(energy, flux,
                                  color='darkmagenta', linestyle=':',zorder=1,
                                  label="TDE, Biehl et al.") # (1711.03555)
            self.neutrino_models.append(p_tde)

        elif name=='boncioli':
            energy, flux, band_min, band_max = self.get_data('models/boncioli_llgrb.txt')
            self.ax.fill_between(energy, band_min, band_max,
                                 color='0.8')
            p_ll_grb, = self.ax.plot(energy, flux,
                                     linestyle='-.', c='k', zorder=1,
                                     label="LLGRB, Boncioli et al.") # (1808.07481)
            self.neutrino_models.append(p_ll_grb)

        elif name=='murase_agn':
            energy, flux, _, _ = self.get_data('models/murase_agn.txt')
            agn, = self.ax.plot(energy, flux,
                                color="red", linestyle='--',
                                label="AGN, Murase") # (1511.01590)
            self.neutrino_models.append(agn)

        elif name=='murase_grb':
            energy, flux, _, _ = self.get_data('models/murase_grb_late_prompt.txt')
            late, = self.ax.plot(energy, flux,
                                 color="saddlebrown", linestyle='-.',
                                 label="GRB afterglow-late prompt, Murase") # (0707.1140)
            energy, flux, _, _ = self.get_data('models/murase_grb_wind.txt')
            wind, = self.ax.plot(energy, flux,
                                 color="goldenrod", linestyle='-.',
                                 label="GRB afterglow-wind, Murase") # (0707.1140)
            energy, flux, _, _ = self.get_data('models/murase_grb_ism.txt')
            ism, = self.ax.plot(energy, flux,
                                color="gold", linestyle='-.',
                                label="GRB afterglow-ISM, Murase") # (0707.1140)
            self.neutrino_models.extend([late, wind, ism])

        else:
            raise ValueError("Unrecognized data set '"+str(name)+"'")


    def add_experiment(self, name):
        if 'ice_cube' in name:
            if self.e_power==2:
                self.ax.annotate('IceCube',
                                 xy=(3e6, 5e-8), xycoords='data',
                                 horizontalalignment='center', color='dodgerblue', rotation=0)
            if self.e_power==1:
                self.ax.annotate("IceCube",
                                 xy=(1.3e7, 2.5e-15), xycoords='data',
                                 horizontalalignment='center', color='dodgerblue', rotation=0,fontsize=12)

        if name=='grand_10k':
            energy, flux, _, _ = self.get_data('experiments/grand_10k.txt')
            self.ax.plot(energy, flux,
                         color='saddlebrown', linestyle="--")
            if self.e_power==2:
                self.ax.annotate('GRAND 10k',
                                 xy=(1e10, 5e-8*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='saddlebrown', rotation=40)
            if self.e_power==1:
                self.ax.annotate('GRAND 10k',
                                 xy=(2e9, 5e-18*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='saddlebrown', rotation=-10)

        elif name=='grand_200k':
            energy, flux, _, _ = self.get_data('experiments/grand_200k.txt')
            self.ax.plot(energy, flux,
                         color='saddlebrown', linestyle="--")
            if self.e_power==2:
                self.ax.annotate('GRAND 200k',
                                 xy=(1e10, 3e-9*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='saddlebrown', rotation=40)

        elif name=='radar':
            energy, _, band_min, band_max = self.get_data('experiments/radar.txt')
            self.ax.fill_between(energy, band_min, band_max,
                                 facecolor='None', edgecolor='0.8', hatch='x')
            if self.e_power==2:
                self.ax.annotate('Radar',
                                 xy=(1e9, 3e-8*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='0.7', rotation=45)

        elif name=='ice_cube_ehe':
            energy, flux, _, _ = self.get_data('experiments/ice_cube_ehe.txt')
            self.ax.plot(energy, flux,
                         color='grey')
            self.ax.annotate('IceCube',
                                xy=(1e7, 0.95e-8), xycoords='data',
                                horizontalalignment='center', color='gray', rotation=17)


        elif name=='ice_cube_hese_data':
            energy, flux, err_min, err_max = self.get_data('experiments/ice_cube_hese.txt')
            uplimit = err_max-flux
            uplimit[np.where(err_max-flux == 0)] = 1
            uplimit[np.where(err_max-flux != 0)] = 0

            self.ax.errorbar(energy, flux*3,
                             yerr=np.asarray([flux-err_min, err_max-flux])*3, uplims=uplimit,
                             color='dodgerblue', marker='o', ecolor='dodgerblue', linestyle='None')

        elif name=='ice_cube_hese_fit':
            ice_cube_hese_range = self._get_i3_hese_range()
            energy = ice_cube_hese_range[0] / self.e_unit
            band_min = ice_cube_hese_range[1] * energy**self.e_power / self.f_unit
            band_max = ice_cube_hese_range[2] * energy**self.e_power / self.f_unit
            self.ax.fill_between(energy, band_min, band_max,
                                 hatch='\\', edgecolor='dodgerblue', facecolor='azure')
            flux = self._i3_nu_fit(ice_cube_hese_range[0], offset=2.46, slope=-2.92) * energy**self.e_power / self.f_unit
            self.ax.plot(energy, flux,
                         color='dodgerblue')

        elif name=='ice_cube_mu_fit':
            ice_cube_mu_range = self._get_i3_mu_range()
            energy = ice_cube_mu_range[0] / self.e_unit
            band_min = ice_cube_mu_range[1] * energy**self.e_power / self.f_unit
            band_max = ice_cube_mu_range[2] * energy**self.e_power / self.f_unit
            self.ax.fill_between(energy, band_min, band_max,
                                 edgecolor='dodgerblue', facecolor='azure')
            flux = self._i3_nu_fit(ice_cube_mu_range[0], offset=1.01, slope=-2.19) * energy**self.e_power / self.f_unit
            self.ax.plot(energy, flux,
                         color='dodgerblue')

        elif name=='anita':
            energy, flux, _, _ = self.get_data('experiments/anita.txt')
            self.ax.plot(energy, flux,
                         color='darkorange')
            if self.e_power==2:
                self.ax.annotate('ANITA I - III',
                                 xy=(2e9, 5e-6*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='darkorange')
            if self.e_power==1:
                self.ax.annotate('ANITA I - III',
                                 xy=(3e9, 1e-15*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='darkorange')

        elif name=='anitaiv':
            energy, flux, _, _ = self.get_data('experiments/anita_iv.txt')
            self.ax.plot(energy, flux,
                         color='grey')
            if self.e_power==2:
                self.ax.annotate('ANITA I - IV',
                                 xy=(4e9, 5e-6*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey')
            if self.e_power==1:
                self.ax.annotate('ANITA I - IV',
                                 xy=(2e9, 1e-14*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', fontsize=12)

        elif name=='auger':
            energy, flux, _, _ = self.get_data('experiments/auger.txt')
            self.ax.plot(energy, flux,
                         color='grey')
            if self.e_power==2:
                self.ax.annotate('Auger',
                                 xy=(1.2e8, 1.1e-7*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-40)
            if self.e_power==1:
                self.ax.annotate('Auger',
                                 xy=(3e10, 9.5e-18*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-8, fontsize=12)
        elif name=='auger_2019':
            energy, flux, _, _ = self.get_data('experiments/auger_2019.txt')
            self.ax.plot(energy, flux,
                         color='grey')
            if self.e_power==2:
                self.ax.annotate('Auger',
                                 xy=(4e7, 5e-8*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-40)
            if self.e_power==1:
                self.ax.annotate("Auger",
                                 xy=(5e7, 2e-15*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=0, fontsize=12)
        elif name=='arianna':
            energy, flux, _, _ = self.get_data('experiments/arianna.txt')
            self.ax.plot(energy, flux*2.,
                         color='grey')
            if self.e_power==2:
                self.ax.annotate('ARIANNA (7x3yr)',
                                 xy=(1.2e8, 1.1e-7*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-40)
            if self.e_power==1:
                self.ax.annotate('ARIANNA (7x3yr)',
                                 xy=(5e9, 8.7e-17*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-25, fontsize=12)
        elif name=='arianna_2019':
            energy, flux, _, _ = self.get_data('experiments/arianna_2019.txt')
            self.ax.plot(energy, flux*2.,
                         color='grey')
            if self.e_power==2:
                self.ax.annotate('ARIANNA (7x4.5yr)',
                                 xy=(6.8e9, 1.9e-6*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=20)
            if self.e_power==1:
                self.ax.annotate('ARIANNA (7x4.5yr)',
                                 xy=(3.6e9, 9.6e-17*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', rotation=-26, fontsize=12)
        elif name=='ara_a23':
            energy, flux, _, _ = self.get_data('experiments/ara_a23.txt')
            self.ax.plot(energy, flux,
                         color='grey', linewidth=1.0)
            if self.e_power==2:
                self.ax.annotate('ARA2 (2x4yr)',
                                 xy=(1.4e10, 5.1e-7*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='grey', 
                                 rotation=15)
            if self.e_power==1:
                self.ax.annotate('ARA (2x4yr)',
                                 xy=(3e8, 15.5e-17*self.e_bins), xycoords='data',
                                 horizontalalignment='left', color='purple', 
                                 rotation=-41)
        else:
            raise ValueError("Unrecognized data set '"+str(name)+"'")


    def build_base_plot(self, group='clean', experiments=None, models=None):
        if group=='rnog_proposal':
            if experiments is None:
                # experiments = ['anitaiv', 'auger_2019', 'ara_a23', 'arianna_2019',
                #                'ice_cube_ehe', 'ice_cube_hese_data', 'ice_cube_mu_fit']
                experiments = ['anitaiv', 'auger_2019', 'ara_a23', 'arianna_2019', 'ice_cube_ehe']
            if models is None:
                models = ['kotera', 'ahlers']
        else:
            if experiments is None:
                experiments = []
            if models is None:
                models = []
        for name in models:
            self.add_model(name)
        for name in experiments:
            self.add_experiment(name)


    def add_limit(self, name, energies, veffs, stations=1, years=1, color=None, linestyle=None, label=None, sup=2.44):
        limits = calculate_flux(energies, veffs, stations, years, sup=sup)
        limits *= energies**self.e_power # convert to GeV m^-2 s^-1 sr^-1 (if this is an E^2 plot)
        limits *= 1e-4 # convert to GeV cm^-2 s^-1 sr^-1

        # Scale by energy bin size
        log_energy = np.log10(energies)
        d_log_energy = np.diff(log_energy)
        bins_per_decade = 1/d_log_energy[0]
        limits *= self.e_bins / bins_per_decade

        if label is None:
            label = "{2}: {0} stations, {1} years".format(stations, years, name)

        # Plot limit
        _plt, = self.ax.plot(energies / self.e_unit,
                             limits / self.f_unit,
                             color=color, linestyle=linestyle,
                             label=label,
                             linewidth=5,
                             zorder=100+len(self.custom_limits))
        self.custom_limits.append(_plt)
        return energies/self.e_unit, limits/self.f_unit


    def title(self, title, size=None):
        self.ax.set_title(title)
        if size is None:
            size = self.font_size
        self.ax.title.set_fontsize(size)

    def show(self, legend_size=12, save_name=None, *args, **kwargs):
        if self.e_power==2:
            self.ax.add_artist(plt.legend(handles=self.neutrino_models, loc=4, fontsize=legend_size))
            # self.ax.add_artist(plt.legend(handles=self.custom_limits, loc=2, fontsize=legend_size))
        elif self.e_power==1:
            self.ax.add_artist(plt.legend(handles=self.neutrino_models, loc=3, fontsize=legend_size))
            # self.ax.add_artist(plt.legend(handles=self.custom_limits, loc=1, fontsize=legend_size))
        plt.tight_layout()
        if save_name is not None:
            plt.savefig(save_name, *args, **kwargs)
        # plt.show()

# this part of the code is borrowed from PyREx
# but replicated here to avoid having PyREx as a dependency
# See: https://github.com/bhokansonfasig/pyrex/blob/master/pyrex/particle.py#L866

def get_total_cross_section(energy, particle_type):
    """
    A function to get the total cross-section of a neutrino.
    Based on CTW 2011

    Parameters
    ----------
    energy: double or float
        neutrino energy in eV

    particle_type: str
        whether particle is 'neutrino' or 'antineutrino'

    Returns
    -------
    sigma: double or float
        the cross section
    """

    if particle_type == 'neutrino':
        c_0_cc = -1.826
        c_0_nc = -1.826
        c_1_cc = -17.31
        c_1_nc = -17.31
        c_2_cc = -6.406
        c_2_nc = -6.448
        c_3_cc = 1.431
        c_3_nc = 1.431
        c_4_cc = -17.91
        c_4_nc = -18.61
    elif particle_type == 'antineutrino':
        c_0_cc = -1.033
        c_0_nc = -1.033
        c_1_cc = -15.95
        c_1_nc = -15.95
        c_2_cc = -7.247
        c_2_nc = -7.296
        c_3_cc = 1.569
        c_3_nc = 1.569
        c_4_cc = -17.72
        c_4_nc = -18.30
    else:
        raise TypeError('particle_type is {}, which is not supported'.format(particle_type))

    eps = np.log10(energy)
    log_term_cc = np.log(eps - c_0_cc)
    power_cc = (c_1_cc + c_2_cc*log_term_cc + c_3_cc*log_term_cc**2
                + c_4_cc/log_term_cc)
    log_term_nc = np.log(eps - c_0_nc)
    power_nc = (c_1_nc + c_2_nc*log_term_nc + c_3_nc*log_term_nc**2
                + c_4_nc/log_term_nc)
    return 10**power_cc + 10**power_nc


def get_lint(energy, particle_type):
    """
    A function to get the interaction length of a neutrino
    Parameters
    ----------
    energy: double or float
        neutrino energy in eV

    particle_type: str
        whether particle is 'neutrino' or 'antineutrino'

    Returns
    -------
    lint: double or float
        the interaction length
    """

    sigma = get_total_cross_section(energy, particle_type)
    lint = 1 / (scipy.constants.N_A * sigma)
    return lint

def get_average_lint(energy):
    """
    A function to get the average interaction length for neutrino and anti-neutrino
    Calculated as the harmonic mean, since the average should be in *cross section*

    ----------
    energy: double or float
        neutrino energy in eV

    Returns
    -------
    lint: double or float
        the average interaction length
    """
    lint_nu = get_lint(energy, 'neutrino')
    lint_nubar = get_lint(energy, 'antineutrino')
    lint_avg = 2/((1/lint_nu)+(1/lint_nubar))
    return lint_avg


def calculate_flux(energies, veffs, stations=1, years=1, sup=2.44):
    """Calculate flux (m^-2 s^-1 sr^-1 GeV^-1) for energies in GeV and veffs in km3sr and livetime in years"""
    energies = np.asarray(energies)
    veffs = np.asarray(veffs)

    # Get number of energy bins per decade
    log_energy = np.log10(energies)
    d_log_energy = np.diff(log_energy)
    for d_log in d_log_energy:
        if not np.isclose(d_log, d_log_energy[0]):
            raise ValueError("Energies should be evenly spaced in log-10-space")
    bins_per_decade = 1/d_log_energy[0]

    # Get average interaction lengths (harmonic mean, since average should be in cross section)
    int_len = np.zeros(len(energies))
    for i, e in enumerate(energies):
        int_len[i] = get_average_lint(e)

    # Get effective area
    ice_density = 0.92 # g/cm^3
    ice_density *= 1e15 # convert to g/km^3 = nucleons/km^3
    aeffs = veffs * ice_density / int_len # cm^2 sr
    aeffs *= 1e-4 # convert to m^2 sr

    aeff_tots = aeffs * stations * (years * 365.25 * 24 * 60 * 60)

    # Upper limit on events
    # 2.3 for Neyman UL w/ 0 background,
    # 2.44 for F-C UL w/ 0 background, etc
    upper_limit = sup

    return upper_limit / aeff_tots * bins_per_decade / np.log(10) / energies


def count_neutrinos(flux, energies, veffs, stations=1, years=1, sup=2.44):
    """Count the number of neutrinos observed for a given flux at each energy"""
    log_energy = np.log10(energies)
    step = np.diff(log_energy)[0]
    mean_fluxes = np.zeros(len(energies))
    for i, (e, log_e) in enumerate(zip(energies, log_energy)):
        e_range = np.logspace(log_e-step/2, log_e+step/2, 101)
        log_e_range = np.linspace(log_e-step/2, log_e+step/2, 101)
        mean_fluxes[i] = np.trapz(flux(e_range), x=log_e_range) / step
    return mean_fluxes / calculate_flux(energies, veffs, stations, years) * sup



