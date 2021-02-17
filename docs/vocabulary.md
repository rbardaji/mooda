# Vocabulary

We recommended to use the CF vocabulary. For parameters that are not yet in the CF, we recommend using the [IMOS vocabulary](https://github.com/aodn/imos-toolbox/blob/master/IMOS/imosParameters.txt). Below is the recommended vocabulary:

## CF parameters

ID | units | valid min | valid max | standard / long name | direction positive | reference datum 
--- | --- | --- | --- | --- | --- | --- |
AIRT | degrees_Celsius | -50.0 | 50.0 | air_temperature | |
ATMP | pascal | 90000.0 | 110000.0 | air_pressure | |
ATMP | pascal | 90000.0 | 110000.0 | air_pressure | |
ATMS | pascal | 90000.0 | 110000.0 | air_pressure_at_mean_sea_level | |
BAT | m-1 | | | volume_beam_attenuation_coefficient_of_radiative_flux_in_sea_water | |
BOT_DEPTH | m | 0.0 | 12000.0 | sea_floor_depth_below_sea_surface | down | sea surface
CDIR | degree | 0.0 | 360.0 | direction_of_sea_water_velocity | clockwise | true north
CDIR_MAG | degree | 0.0 | 360.0 | direction_of_sea_water_velocity | clockwise | magnetic north
CDOM | 1e-9 | 0.0 | 375.0 | concentration_of_colored_dissolved_organic_matter_in_sea_water _expressed_as_equivalent_mass_fraction _of_quinine_sulfate_dihydrate | clockwise | magnetic north
CHC | ug l-1 | | | mass_concentration_of_petroleum_hydrocarbons_in_sea_water | |
CNDC | S m-1 | 0.0 | 50000.0 | sea_water_electrical_conductivity | |
CSPD | m s-1 | 0.0 | 10.0 | sea_water_speed | |
DENS | kg m-3 | | | sea_water_density | |
DEPTH | m | -5.0 | 12000.0 | depth | down | sea surface
DEWT | degrees_Celsius | -50.0 | 50.0 | dew_point_temperature | depth | sea surface
DOX1 | umol l-1 | 0.0 | 1000.0 | mole_concentration_of_dissolved_molecular_oxygen_in_sea_water | |
DOX2 | umol kg-1 | 0.0 | 1000.0 | moles_of_oxygen_per_unit_mass_in_sea_water | |
DOXS | % | 0.0 | 100.0 | fractional_saturation_of_oxygen_in_sea_water | |
DOXY | mg l-1 | 0.0 | 29.0 | mass_concentration_of_oxygen_in_sea_water | |
DOXY_TEMP | degrees_Celsius | 0.0 | 0.0 | temperature_of_sensor_for_oxygen_in_sea_water | |
HEADING | degree | 0.0 | 360.0 | platform_yaw_angle | clockwise | true north
HEADING_MAG | degree | 0.0 | 360.0 | platform_yaw_angle | clockwise | magnetic north
HEAT_NET | W m-2 | | | surface_upward_heat_flux_in_air | |
HEIGHT_ABOVE_SENSOR | m | -12000.0 | 12000.0 | height | up | sea surface
HL | W m-2 | | | surface_upward_latent_heat_flux | |
HS | W m-2 | | | surface_upward_sensible_heat_flux | |
ISO17 | m | | | depth_of_isosurface_of_sea_water_potential_temperature | down | sea surface
LATITUDE | degrees_north | -90.0 | 90.0 | latitude | WGS84 geographic coordinate system |
LONGITUDE | degrees_east | -180.0 | 180.0 | longitude | WGS84 geographic coordinate system |
LW | W m-2 | | | surface_downwelling_longwave_flux_in_air | |
LW_NET | W m-2 | | | surface_net_upward_longwave_flux | |
MASS_NET | kg m-2 s-1 | | | upward_mass_flux_of_air | |
NOBS | 1 | | | number_of_observations | |
NOMINAL_DEPTH | m | -5.0 | 12000.0 | depth | down | sea surface
NTRA | umole l-1 | | | mole_concentration_of_nitrate_in_sea_water | |
NTR2 | umole kg-1 | | | moles_of_nitrate_per_unit_mass_in_sea_water | |
PAR | umole m-2 s-1 | | | downwelling_photosynthetic_photon_flux_in_sea_water | |
PCO2 | pascal | | | surface_partial_pressure_of_carbon_dioxide_in_air | |
PHOS | umole kg-1 | | | moles_of_phosphate_per_unit_mass_in_sea_water | |
PHO2 | umole l-1 | | | mole_concentration_of_phosphate_in_sea_water | |
PITCH | degree | -180.0 | 180.0 | platform_pitch_angle | |
PRES | dbar | -5.0 | 12000.0 | sea_water_pressure | |
PRES_REL | dbar | -15.0 | 12000.0 | sea_water_pressure_due_to_sea_water | |
PSAL | 1 | 2.0 |  41.0 | sea_water_practical_salinity | |
Q | 1 | 0.0 | 150.0 | surface_specific_humidity | |
RRATE | mm s-1 | | | rainfall_rate | |
RAIN_AMOUNT | mm | | | thickness_of_rainfall_amount | |
RELH | % | 0.0 | 150.0 | relative_humidity | |
ROLL | degree | -180.0 | 180.0 | platform_roll_angle | |
SLCA | umole l-1 | | | mole_concentration_of_silicate_in_sea_water | |
SLC2 | umole kg-1 | | | moles_of_silicate_per_unit_mass_in_sea_water | |
SRAD | W m-1 sr-1 | | | isotropic_shortwave_radiance_in_air | |
SSPD | m s-1 | 1400.0 | 1600.0 | speed_of_sound_in_sea_water | |
SSS | 1e-3 | 2.0 |41.0 | sea_surface_salinity | |
SST | degrees_Celsius | 2.0 | 41.0 | sea_surface_skin_temperature | |
SSTI | degrees_Celsius | -2.5 | 40.0 | sea_surface_temperature | |
SSWV | m2 s degree-1 | | | sea_surface_wave_directional_variance_spectral_density | |
SSWV_MAG | m2 s degree-1 | | | sea_surface_wave_directional_variance_spectral_density | |
SW | W m-2 | | | surface_downwelling_shortwave_flux_in_air | |
SWSH | m | 0.0 | 100.0 | sea_surface_swell_wave_significant_height | |
SW_NET | W m-2 | | | surface_net_upward_shortwave_flux | |
TAU | pascal | | | magnitude_of_surface_downward_stress | |
TEMP | degrees_Celsius | -2.5 | 40.0 | sea_water_temperature | |
TIME | time | 0.0 | 90000.0 | days since 1950-01-01 00:00:00 UTC | |
TURB | 1 | 0.0 | 4.0 | sea_water_turbidity | |
UCUR | m s-1 | -10.0 | 10.0 | eastward_sea_water_velocity | | true north
UCUR_MAG | m s-1 | -10.0 | 10.0 | eastward_sea_water_velocity | | magnetic north
UWND | m s-1 | | | eastward_wind | |
VAVH | m | 0.0 | 100.0 | sea_surface_wave_significant_height | |
VCUR | m s-1 | -10.0 | 10.0 | northward_sea_water_velocity | | true north
VCUR_MAG | m s-1 | -10.0 | 10.0 | northward_sea_water_velocity | | magnetic north
VDEN | m2 s | | | sea_surface_wave_variance_spectral_density | |
VDIR | degree | 0.0 | 360.0 | sea_surface_wave_from_direction | clockwise | true north
VDIR_MAG | degree | 0.0 | 360.0 | sea_surface_wave_from_direction | clockwise | magnetic north
VDIRT | degree | 0.0 | 360.0 | sea_surface_wave_to_direction | clockwise | true north
VWND | m s-1 | | | northward_wind | clockwise | true north
WCUR | m s-1 | -5.0 | 5.0 | upward_sea_water_velocity | |
WDIR | degree | 0.0 | 360.0 | wind_to_direction | clockwise | true north
WDIRF_AVG | degree | 0.0 | 360.0 | wind_from_direction | clockwise | true north
WHTE | m | 0.0 | 100.0 | sea_surface_wave_mean_height_of_highest_tenth | |
WHTH | m | 0.0 | 100.0 | sea_surface_wave_significant_height | |
WPFM | second | 0.0 | 100.0 | sea_surface_wave_mean_period | |
WPMH | second | 0.0 | 100.0 | sea_surface_wave_mean_period | |
WPSM | second | 0.0 | 100.0 | sea_surface_wave_mean_period_ from_variance_spectral_density_second_ frequency_moment | |
WPTE | second | 0.0 | 100.0 | sea_surface_wave_mean_period_of_highest_tenth | |
WPTH | second | 0.0 | 100.0 | sea_surface_wave_significant_period | |
WMPP | second | 0.0 | 100.0 | sea_surface_wave_maximum_period | |
WMSH | m | 0.0 | 100.0 | sea_surface_wave_mean_height | |
WMXH | m | 0.0 | 100.0 | sea_surface_wave_maximum_height | |
WPDI | degree | 0.0 | 360.0 | sea_surface_wave_from_direction_ at_variance_spectral_density_maximum | clockwise | true north
WPDI_MAG | degree | 0.0 | 360.0 | sea_surface_wave_from_direction_ at_variance_spectral_density_maximum | clockwise | magnetic north
WPPE | second | 0.0 | 100.0 | sea_surface_wave_period_ at_variance_spectral_density_maximum | clockwise | magnetic north
WSPD | m s-1 | | | wind_speed | |
WSPD_AVG | m s-1 | | | wind_speed | |
WSPD_MIN | m s-1 | | | wind_speed | |
WSPD_MAX | m s-1 | | | wind_speed | |
WWAV | degree | 0.0 | 360.0 | sea_surface_wind_wave_to_direction | clockwise | true north
WWSH | m | 0.0 | 100.0 | sea_surface_wind_wave_significant_height | clockwise | true north
XCO2_AIR | 1e-6 | 0.0 | 360.0 | mole_fraction_of_carbon_dioxide_in_air | clockwise | true north

## Other parameters

ID | units | valid min | valid max | standard / long name | direction positive | reference datum 
--- | --- | --- | --- | --- | --- | --- |
ABSI | decibel | 0.0 | 150.0 | backscatter_intensity_from_acoustic_beam | | 
ABSI1 | decibel | 0.0 | 150.0 | backscatter_intensity_from_acoustic_beam_1 | | 
ABSI2 | decibel | 0.0 | 150.0 | backscatter_intensity_from_acoustic_beam_2 | |
ABSI3 | decibel | 0.0 | 150.0 | backscatter_intensity_from_acoustic_beam_3 | |
ABSI4 | decibel | 0.0 | 150.0 | backscatter_intensity_from_acoustic_beam_4 | |
ABSIC1 | count | 0.0 | 255.0 | backscatter_intensity_from_acoustic_beam_1 | |
ABSIC2 | count | 0.0 | 255.0 | backscatter_intensity_from_acoustic_beam_2 | |
ABSIC3 | count | 0.0 | 255.0 | backscatter_intensity_from_acoustic_beam_3 | |
ABSIC4 | count | 0.0 | 255.0 | backscatter_intensity_from_acoustic_beam_4 | |
CMAG1 | count | 0.0 | 255.0 | particle_distribution_correlation_magnitude_from_acoustic_beam_1 | |
CMAG2 | count | 0.0 | 255.0 | particle_distribution_correlation_magnitude_from_acoustic_beam_2 | |
CMAG3 | count | 0.0 | 255.0 | particle_distribution_correlation_magnitude_from_acoustic_beam_3 | |
CMAG4 | count | 0.0 | 255.0 | particle_distribution_correlation_magnitude_from_acoustic_beam_4 | |
PERG1 | % | 0.0 | 100.0 | percentage_of_good_three_beam_solutions | |
PERG2 | % | 0.0 | 100.0 | percentage_of_transformations_rejected | |
PERG3 | % | 0.0 | 100.0 | percentage_of_measurements_with_more_than_one_beam_bad | |
PERG4 | % | 0.0 | 100.0 | percentage_of_good_four_beam_solutions | |
CHR | ug l-1 | | | mass_concentration_of_refined_hydrocarbons_in_sea_water | |
CPHL | mg m-3 | 0.0 | 5.0 | mass_concentration_of_inferred_chlorophyll_ from_relative_fluorescence_units_in_sea_water | |
CSPD_STD | m s-1 | 0.0 | 10.0 | sea_water_speed_standard_deviation | |
DESC | m s-1 | 0.0 | 5.0 | profiling_descent_rate_of_instrument | |
DIR | degree | 0.0 | 360.0 | from_direction | clockwise | true north
DIR_MAG | degree | 0.0 | 360.0 | from_direction | clockwise | magnetic north
DIRECTION | | | | direction_of_the_profile | |
DIRT | degree | 0.0 | 360.0 | to_direction | clockwise | true north
DIST_ALONG_BEAMS | m | -12000.0 | 12000.0 | distance_from_sensor_along_beams | |
DOX | ml l-1 | 0.0 | 200.0 | volume_concentration_of_dissolved_molecular_oxygen_in_sea_water | |
DRYT | degrees_Celsius | | | dry_bulb_temperature | |
DYNHT | m | | | dynamic_height | |
ECUR | m s-1 | -5.0 | 5.0 | error_sea_water_velocity | |
FLU2 | count | -5.0 | 5.0 | fluorescence_in_sea_water | |
FREQUENCY | Hz | 0.0 | 900000.0 | frequency | |
GDOP | degree | 0.0 | 180.0 | radar_beam_intersection_angle | |
HEAT | 10^10 J m-2 | | | heat_content | |
MAXZ | 1 | | | maximum_number_of_samples_in_vertical_profile | |
MEAN_DEPTH | m | 0.0 | 10000.0 | mean_cell_depth | |
MEAN_HEIGHT | m | 0.0 | 100.0 | mean_cell_height | |
OPBS | 1 | | | optical_backscattering_coefficient | |
CPAR | % | 0.0 | 100.0 | downwelling_corrected_photosynthetic_photon_flux_in_sea_water | |
PROFILE | | | | unique_identifier_for_each_profile_feature_instance_in_this_file | |
SNR1 | decibel | 0.0 | 150.0 | signal_noise_ratio_from_acoustic_beam_1 | |
SNR2 | decibel | 0.0 | 150.0 | signal_noise_ratio_from_acoustic_beam_2 | |
SNR3 | decibel | 0.0 | 150.0 | signal_noise_ratio_from_acoustic_beam_3 | |
SPCT | decibel | 0.0 | 3.0 | awac_spectra_calculation_method | |
SPEC_CNDC | S m-1 | 0.0 | 50000.0 | sea_water_specific_electrical_conductivity_corrected_at_25degC | |
SSDS | degree | 0.0 | 360.0 | sea_surface_wave_directional_spread | clockwise | true north
SSDS_MAG | degree | 0.0 | 360.0 | sea_surface_wave_directional_spread | clockwise | magnetic north
SSWD | degree | 0.0 | 360.0 | sea_surface_wave_from_direction_by_frequency | clockwise | true north
SSSSWD_MAGWD | degree | 0.0 | 360.0 | sea_surface_wave_from_direction_by_frequency | clockwise | magnetic north
SSWDT | degree | 0.0 | 360.0 | sea_surface_wave_to_direction_by_frequency | clockwise | true north
SSWST | m2 degree-1 | | | sea_surface_wave_to_directional_variance | |
SSWVT | m2 s degree-1 | | | sea_surface_wave_to_directional_variance_spectral_density | |
SV | m-1 | 0.0 | 1.0 | mean_volume_backscatter_coefficient | |
SV_MEAN | decibel | -128.0 | 0.0 | mean_volume_backscatter | |
SV_KURT | m-1 | 0.0 | 1.0 | kurtosis_volume_backscatter | |
SV_PCNT_GOOD | % | 0.0 | 100.0 | percent_Sv_samples_included | |
SV_SD | m-1 | 0.0 | 1.0 | standard_deviation_volume_backscatter | |
SV_SKEW | m-1 | 0.0 | 1.0 | skewness_volume_backscatter | |
SV_UNFILT | m-1 | 0.0 | 1.0 | mean_volume_backscatter_including_bad_data | |
SV_UNFILT_KURT | m-1 | 0.0 | 1.0 | kurtosis_volume_backscatter_including_bad_data | |
SV_UNFILT_SD | m-1 | 0.0 | 1.0 | standard_deviation_volume_backscatter_including_bad_data | |
SV_UNFILT_SKEW | m-1 | 0.0 | 1.0 | skewness_volume_backscatter_including_bad_data | |
SWPD | degree | 0.0 | 360.0 | sea_surface_swell_wave_ from_direction_at_ variance_spectral_density_maximum | clockwise | true north
SWPD_MAG | degree | 0.0 | 360.0 | sea_surface_swell_wave_from_direction_ at_variance_spectral_density_maximum | clockwise | magnetic north
SWPP | second | 0.0 | 100.0 | sea_surface_swell_wave_period_ at_variance_spectral_density_maximum | clockwise | magnetic north
TIMESERIES | 1 | | | unique_identifier_for_each_timeseries_feature_instance_in_this_file | |
TURBF | 1 | 0.0 | 4.0 | sea_water_turbidity_in_FTU | |
TRAJECTORY | | | | unique_identifier_for_each_trajectory_feature_instance_in_this_file | |
VBSC | m-1 sr-1 | | | volumetric_backscatter_coefficient | |
VDEV | m2 s | | | sea_surface_wave_variance_spectral_density_from_velocity | |
VDEP | m2 s | | | sea_surface_wave_variance_spectral_density_from_pressure | |
VDES | m2 s | | | sea_surface_wave_variance_spectral_density_from_range_to_surface | |
VEL1 | m s-1 | -10.0 | 10.0 | sea_water_velocity_from_acoustic_beam_1 | |
VEL2 | m s-1 | -10.0 | 10.0 | sea_water_velocity_from_acoustic_beam_1 | |
VEL3 | m s-1 | -10.0 | 10.0 | sea_water_velocity_from_acoustic_beam_1 | |
VEL4 | m s-1 | -10.0 | 10.0 | sea_water_velocity_from_acoustic_beam_1 | |
VOLT | V | -100.0 | 100.0 | voltage | |
VSF412 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_412nm | |
VSF440 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_440nm | |
VSF470 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_470nm | |
VSF488 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_488nm | |
VSF510 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_510nm | |
VSF532 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_532nm | |
VSF595 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_595nm | |
VSF650 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_650nm | |
VSF660 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_660nm | |
VSF676 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_676nm | |
VSF715 | m-1 sr-1 | | | volume_scattering_function_ of_radiative_flux_in_sea_water_ for_wavelength_715nm | |
WPDIT | degree | 0.0 | 360.0 | sea_surface_wave_to_direction_at_variance_spectral_density_maximum | clockwise | true north
WSMP | second | 0.0 | 100.0 | sea_surface_wave_spectral_mean_period | |
WSSH | m | 0.0 | 100.0 | sea_surface_wave_spectral_significant_height | |
WWDS | degree | 0.0 | 360.0 | sea_surface_wind_wave_directional_spread | clockwise | true north
WWPD | degree | 0.0 | 360.0 | sea_surface_wind_wave_from_direction_ at_variance_spectral_density_maximum | clockwise | true north
WWPD_MAG | degree | 0.0 | 360.0 | sea_surface_wind_wave_ from_direction_at_variance_spectral_density_maximum | clockwise | magnetic north
WWPP | second | 0.0 | 100.0 | sea_surface_wind_wave_period_at_variance_spectral_density_maximum | |
XCO2_WATER | 1e-6 | | | mole_fraction_of_carbon_dioxide_in_sea_water | |

Return to [index](index_docs.md).
