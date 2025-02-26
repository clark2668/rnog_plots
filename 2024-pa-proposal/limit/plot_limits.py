from limits import LimitFigure
import rnog as rnog


if __name__=="__main__":

    # July 2024-2025: 8 years
    # July 2025-2026: 9 years (add 1 station)
    # July 2026-2027: 14 years (add 5 stations)
    # July 2027-2028: 22 years (add 8 stations)
    # July 2028-2029: 30 yaers (add 8 stations) -- not included, cuz we can't analysze it in time
    additional_years = 8 + 9 + 14 + 22
    print(additional_years)

    rnog_energies, rnog_today = rnog.compute_exposure(
        additional_years=0,
    )

    rnog_energies, rnog_moreSMT = rnog.compute_exposure(
        additional_years=additional_years,
        additional_uptime_fraction=2./3.,
        additional_veff_assume='smt'
    )


    rnog_energies, rnog_morePA = rnog.compute_exposure(
        additional_years=additional_years,
        additional_uptime_fraction=2./3.,
        additional_veff_assume='pa'
    )

    figure = LimitFigure(e_power=2, xlims=(1e6, 1e11), ylims=(1e-10, 1e-5), font_size=16, tick_size=14)    
    figure.build_base_plot('rnog_proposal')
    
    
    energies, limits = figure.add_limit(name='RNOG', energies=rnog_energies,
        veffs=rnog_today, stations=1, years=1, sup=2.44,
        color='black',linestyle='--', label='RNO-G on-disk')

    energies, limits = figure.add_limit(name='RNOG', energies=rnog_energies,
        veffs=rnog_moreSMT, stations=1, years=1, sup=2.44,
        color='red',linestyle='-.', label='RNO-G 2028 (more Hi/Lo)')
    
    energies, limits = figure.add_limit(name='RNOG', energies=rnog_energies,
        veffs=rnog_morePA, stations=1, years=1, sup=2.44,
        color='blue',linestyle=':', label='RNO-G 2028 (more PA)')
    figure.show(legend_size=10, save_name='limit_E2FE.png',dpi=300)

    print('Energies {} in GeV'.format(energies))
    print('Limit {} in GeV/cm2/s/sr'.format(limits))
