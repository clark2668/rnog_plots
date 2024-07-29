from limits import LimitFigure
import rnog as rnog


if __name__=="__main__":

    rnog_energies, rnog_projected_exposure = rnog.compute_exposure(
        additional_years=0,
        uptime_fraction=0.45
    )

    # figure = LimitFigure(e_power=1, xlims=(1e6, 1e11), ylims=(1e-19, 1e-13), font_size=16, tick_size=14)    
    figure = LimitFigure(e_power=2, xlims=(1e6, 1e11), ylims=(1e-10, 1e-5), font_size=16, tick_size=14)    
    figure.build_base_plot('ara_a23')
    # energies, limits = figure.add_limit(name='RNOG', energies=rnog_energies,
    #     veffs=rnog_projected_exposure, stations=1, years=1, sup=2.44,
    #     color='black',linestyle='--', label='RNO-G 8')
    figure.show(legend_size=10, save_name='limit_E2FE.png',dpi=300)

    # print('Energies {} in GeV'.format(energies))
    # print('Limit {} in GeV/cm2/s/sr'.format(limits))
