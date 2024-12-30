import csv
import random
import datetime

# Configuration parameters
NUM_WELLS = 5  # number of wells to simulate
NUM_RECORDS_PER_WELL = 1000  # number of records per well per dataset
ERROR_PROB_MISSING = 0.05  # 5% chance to produce a missing value (None)
ERROR_PROB_WRONG_TYPE = 0.05  # 5% chance to produce a wrong data type/string error
ERROR_PROB_OUTLIER = 0.05  # 5% chance to produce an outlier

# Generate a list of wells with some basic attributes
wells = []
for i in range(NUM_WELLS):
    well_id = f"WELL-{1000 + i}"
    lat = 29.0 + random.uniform(-1, 1)
    lon = -95.0 + random.uniform(-1, 1)
    depth = random.randint(1500, 8000)  # approximate total well depth in meters
    wells.append((well_id, lat, lon, depth))


def generate_timestamp_records(num_records, start_date=datetime.date(2010, 1, 1)):
    return [start_date + datetime.timedelta(days=d) for d in range(num_records)]


def random_corrupt_value(value, is_numeric=True):
    """Randomly introduce data quality issues."""
    # Chance to become missing
    if random.random() < ERROR_PROB_MISSING:
        return None

    # Chance to become wrong type (e.g., string where a number is expected)
    if is_numeric and random.random() < ERROR_PROB_WRONG_TYPE:
        return random.choice(["ERROR", "N/A", "NULL", "XYZ"])

    # Chance to become an outlier
    if is_numeric and random.random() < ERROR_PROB_OUTLIER:
        # Multiply by a large factor or add a large offset
        if isinstance(value, (int, float)):
            return value * random.uniform(10, 1000)

    return value


def random_str_choice(choices):
    return random.choice(choices)


# 1. Wellbore Data (20 columns)
# Columns: well_id, date, measured_depth_m, mud_weight_ppg, rop_m_per_hr, borehole_diameter_in,
# fluid_loss_rate_ml_per_min, pump_pressure_psi, bit_type, operator_name, rig_id,
# drilling_fluid_type, wellhead_pressure_psi, formation_pressure_psi, wob_kN, rpm, torque_ft_lbs,
# standpipe_pressure_psi, direction_azimuth_deg, inclination_deg
def generate_wellbore_data():
    bit_types = ["PDC", "Roller Cone", "Diamond Impregnated"]
    operators = ["Schlumberger", "Halliburton", "Baker Hughes", "Nabors", "Weatherford"]
    rig_ids = ["RIG-1", "RIG-2", "RIG-3", "RIG-4", "RIG-5"]
    fluid_types = ["OBM", "WBM", "SOBM"]

    with open("wellbore_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "well_id", "date", "measured_depth_m", "mud_weight_ppg", "rop_m_per_hr", "borehole_diameter_in",
            "fluid_loss_rate_ml_per_min", "pump_pressure_psi", "bit_type", "operator_name", "rig_id",
            "drilling_fluid_type", "wellhead_pressure_psi", "formation_pressure_psi", "wob_kN", "rpm", "torque_ft_lbs",
            "standpipe_pressure_psi", "direction_azimuth_deg", "inclination_deg"
        ])

        for well_id, lat, lon, total_depth in wells:
            dates = generate_timestamp_records(NUM_RECORDS_PER_WELL)
            current_depth = 0
            for dt in dates:
                current_depth += random.randint(5, 20)
                if current_depth > total_depth:
                    current_depth = total_depth
                row = [
                    well_id,
                    dt.isoformat(),
                    random_corrupt_value(current_depth),
                    random_corrupt_value(round(random.uniform(8.5, 12.0), 2)),
                    random_corrupt_value(round(random.uniform(5, 30), 2)),
                    random_corrupt_value(round(random.uniform(8.5, 12.25), 2)),
                    random_corrupt_value(round(random.uniform(0, 50), 2)),
                    random_corrupt_value(round(random.uniform(500, 5000), 2)),
                    random_corrupt_value(random_str_choice(bit_types), is_numeric=False),
                    random_corrupt_value(random_str_choice(operators), is_numeric=False),
                    random_corrupt_value(random_str_choice(rig_ids), is_numeric=False),
                    random_corrupt_value(random_str_choice(fluid_types), is_numeric=False),
                    random_corrupt_value(round(random.uniform(1000, 3000), 2)),
                    random_corrupt_value(round(random.uniform(2000, 6000), 2)),
                    random_corrupt_value(round(random.uniform(10, 200), 2)),
                    random_corrupt_value(round(random.uniform(50, 200), 2)),
                    random_corrupt_value(round(random.uniform(100, 10000), 2)),
                    random_corrupt_value(round(random.uniform(500, 5000), 2)),
                    random_corrupt_value(round(random.uniform(0, 360), 2)),
                    random_corrupt_value(round(random.uniform(0, 90), 2))
                ]
                writer.writerow(row)


# 2. Geophysical Data (20 columns)
# well_id, measured_depth_m, gamma_ray_api, resistivity_ohm_m, sonic_dt_us_ft,
# density_g_cc, neutron_porosity, caliper_in, photoelectric_factor, shale_volume,
# clay_content, water_saturation, hydrocarbon_saturation, permeability_md, velocity_m_s,
# acoustic_impedance, formation_factor, bulk_modulus_GPa, shear_modulus_GPa, poisson_ratio
def generate_geophysical_logs():
    with open("geophysical_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "well_id", "measured_depth_m", "gamma_ray_api", "resistivity_ohm_m", "sonic_dt_us_ft",
            "density_g_cc", "neutron_porosity", "caliper_in", "photoelectric_factor", "shale_volume",
            "clay_content", "water_saturation", "hydrocarbon_saturation", "permeability_md", "velocity_m_s",
            "acoustic_impedance", "formation_factor", "bulk_modulus_GPa", "shear_modulus_GPa", "poisson_ratio"
        ])

        for well_id, lat, lon, total_depth in wells:
            depth_interval = total_depth / NUM_RECORDS_PER_WELL
            for i in range(NUM_RECORDS_PER_WELL):
                depth = i * depth_interval + random.uniform(0, depth_interval)
                row = [
                    well_id,
                    random_corrupt_value(round(depth, 2)),
                    random_corrupt_value(round(random.uniform(20, 150), 2)),
                    random_corrupt_value(round(random.uniform(0.5, 200), 2)),
                    random_corrupt_value(round(random.uniform(50, 120), 2)),
                    random_corrupt_value(round(random.uniform(1.9, 2.7), 3)),
                    random_corrupt_value(round(random.uniform(0.05, 0.35), 3)),
                    random_corrupt_value(round(random.uniform(8.5, 16), 2)),
                    random_corrupt_value(round(random.uniform(1, 5), 2)),
                    random_corrupt_value(round(random.uniform(0.1, 0.8), 3)),
                    random_corrupt_value(round(random.uniform(0.1, 0.5), 3)),
                    random_corrupt_value(round(random.uniform(0.2, 1.0), 3)),
                    random_corrupt_value(round(random.uniform(0.2, 0.8), 3)),
                    random_corrupt_value(round(random.uniform(0.1, 1000), 2)),
                    random_corrupt_value(round(random.uniform(2000, 5000), 2)),
                    random_corrupt_value(round(random.uniform(5e6, 25e6), 2)),  # acoustic impedance
                    random_corrupt_value(round(random.uniform(1, 5), 2)),
                    random_corrupt_value(round(random.uniform(10, 50), 2)),
                    random_corrupt_value(round(random.uniform(5, 30), 2)),
                    random_corrupt_value(round(random.uniform(0.1, 0.4), 3))
                ]
                writer.writerow(row)


# 3. Well Characterization (20 columns)
# well_id, formation_name, porosity_frac, permeability_md, lithology, grain_density_g_cc, clay_volume_frac,
# quartz_volume_frac, calcite_volume_frac, dolomite_volume_frac, formation_thickness_m, net_pay_m,
# capillary_pressure_psi, fluid_contact_depth_m, reservoir_temperature_C, reservoir_pressure_psi,
# oil_saturation_frac, gas_saturation_frac, water_saturation_frac, fracture_density
def generate_well_characterization():
    formations = ["Sandstone_A", "Shale_B", "Limestone_C", "Dolomite_D"]
    lithologies = ["Sandstone", "Shale", "Limestone", "Dolomite"]

    with open("well_characterization.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "well_id", "formation_name", "porosity_frac", "permeability_md", "lithology",
            "grain_density_g_cc", "clay_volume_frac", "quartz_volume_frac", "calcite_volume_frac",
            "dolomite_volume_frac", "formation_thickness_m", "net_pay_m", "capillary_pressure_psi",
            "fluid_contact_depth_m", "reservoir_temperature_C", "reservoir_pressure_psi",
            "oil_saturation_frac", "gas_saturation_frac", "water_saturation_frac", "fracture_density"
        ])

        for well_id, lat, lon, total_depth in wells:
            for i in range(NUM_RECORDS_PER_WELL):
                formation = random.choice(formations)
                lith = lithologies[formations.index(formation)]
                row = [
                    well_id,
                    random_corrupt_value(formation, is_numeric=False),
                    random_corrupt_value(round(random.uniform(0.05, 0.25), 3)),
                    random_corrupt_value(round(random.uniform(0.1, 1000), 2)),
                    random_corrupt_value(lith, is_numeric=False),
                    random_corrupt_value(round(random.uniform(2.0, 2.7), 3)),
                    random_corrupt_value(round(random.uniform(0.1, 0.5), 3)),
                    random_corrupt_value(round(random.uniform(0.2, 0.8), 3)),
                    random_corrupt_value(round(random.uniform(0.0, 0.6), 3)),
                    random_corrupt_value(round(random.uniform(0.0, 0.4), 3)),
                    random_corrupt_value(round(random.uniform(10, 100), 2)),
                    random_corrupt_value(round(random.uniform(5, 50), 2)),
                    random_corrupt_value(round(random.uniform(100, 3000), 2)),
                    random_corrupt_value(round(random.uniform(1500, 3500), 2)),
                    random_corrupt_value(round(random.uniform(50, 150), 2)),
                    random_corrupt_value(round(random.uniform(2000, 6000), 2)),
                    random_corrupt_value(round(random.uniform(0.2, 0.8), 3)),
                    random_corrupt_value(round(random.uniform(0.0, 0.5), 3)),
                    random_corrupt_value(round(random.uniform(0.2, 1.0), 3)),
                    random_corrupt_value(round(random.uniform(0, 10), 2))
                ]
                writer.writerow(row)


# 4. Seismic Data (20 columns)
# seismic_line_id, shot_point, twt_ms, amplitude, frequency_hz, reflection_coefficient,
# acoustic_impedance, velocity_m_s, quality_factor, offset_m, azimuth_deg, inclination_deg,
# wavelet_type, gain_db, noise_level_db, processing_version, survey_name, inline_number, crossline_number, pol_frequency_hz
def generate_seismic_data():
    line_ids = [f"LINE-{i}" for i in range(1, NUM_WELLS + 1)]
    wavelet_types = ["Ricker", "Ormsby", "Klauder"]
    surveys = ["Survey_A", "Survey_B", "Survey_C"]

    with open("seismic_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "seismic_line_id", "shot_point", "twt_ms", "amplitude", "frequency_hz", "reflection_coefficient",
            "acoustic_impedance", "velocity_m_s", "quality_factor", "offset_m", "azimuth_deg", "inclination_deg",
            "wavelet_type", "gain_db", "noise_level_db", "processing_version", "survey_name", "inline_number",
            "crossline_number", "pol_frequency_hz"
        ])

        for line_id in line_ids:
            for i in range(NUM_RECORDS_PER_WELL):
                row = [
                    random_corrupt_value(line_id, is_numeric=False),
                    random_corrupt_value(i + 1),
                    random_corrupt_value(round(random.uniform(1000, 5000), 2)),
                    random_corrupt_value(round(random.uniform(-1000, 1000), 2)),
                    random_corrupt_value(round(random.uniform(10, 60), 2)),
                    random_corrupt_value(round(random.uniform(-1, 1), 4)),
                    random_corrupt_value(round(random.uniform(5e6, 25e6), 2)),
                    random_corrupt_value(round(random.uniform(1500, 5000), 2)),
                    random_corrupt_value(round(random.uniform(10, 100), 2)),
                    random_corrupt_value(round(random.uniform(100, 10000), 2)),
                    random_corrupt_value(round(random.uniform(0, 360), 2)),
                    random_corrupt_value(round(random.uniform(0, 30), 2)),
                    random_corrupt_value(random_str_choice(wavelet_types), is_numeric=False),
                    random_corrupt_value(round(random.uniform(-10, 10), 2)),
                    random_corrupt_value(round(random.uniform(-20, 20), 2)),
                    random_corrupt_value(f"v{random.randint(1, 3)}", is_numeric=False),
                    random_corrupt_value(random_str_choice(surveys), is_numeric=False),
                    random_corrupt_value(random.randint(1000, 2000)),
                    random_corrupt_value(random.randint(2000, 3000)),
                    random_corrupt_value(round(random.uniform(10, 50), 2))
                ]
                writer.writerow(row)


# 5. Production Data (20 columns)
# well_id, date, oil_rate_bopd, gas_rate_mscfd, water_cut_frac, tubing_pressure_psi, casing_pressure_psi,
# choke_size_64ths, gorp_factor, oil_gravity_api, produced_water_salinity_ppm, downhole_temperature_C,
# downhole_pressure_psi, CO2_fraction, H2S_fraction, sand_production_rate_lbs_day,
# ESP_current_amp, ESP_voltage_volts, pump_efficiency_frac, downtime_hours
def generate_production_data():
    with open("production_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "well_id", "date", "oil_rate_bopd", "gas_rate_mscfd", "water_cut_frac", "tubing_pressure_psi",
            "casing_pressure_psi",
            "choke_size_64ths", "gorp_factor", "oil_gravity_api", "produced_water_salinity_ppm",
            "downhole_temperature_C",
            "downhole_pressure_psi", "CO2_fraction", "H2S_fraction", "sand_production_rate_lbs_day",
            "ESP_current_amp", "ESP_voltage_volts", "pump_efficiency_frac", "downtime_hours"
        ])

        for well_id, lat, lon, total_depth in wells:
            dates = generate_timestamp_records(NUM_RECORDS_PER_WELL, start_date=datetime.date(2021, 1, 1))
            for dt in dates:
                row = [
                    well_id,
                    random_corrupt_value(dt.isoformat(), is_numeric=False),
                    random_corrupt_value(round(random.uniform(500, 3000), 1)),
                    random_corrupt_value(round(random.uniform(1000, 10000), 1)),
                    random_corrupt_value(round(random.uniform(0.1, 0.5), 2)),
                    random_corrupt_value(round(random.uniform(1000, 5000), 2)),
                    random_corrupt_value(round(random.uniform(500, 3000), 2)),
                    random_corrupt_value(round(random.uniform(8, 64), 1)),
                    random_corrupt_value(round(random.uniform(0.5, 2.0), 3)),  # gorp_factor is fictional
                    random_corrupt_value(round(random.uniform(20, 40), 1)),
                    random_corrupt_value(round(random.uniform(10000, 50000), 1)),
                    random_corrupt_value(round(random.uniform(50, 120), 2)),
                    random_corrupt_value(round(random.uniform(2000, 6000), 2)),
                    random_corrupt_value(round(random.uniform(0.0, 0.05), 3)),
                    random_corrupt_value(round(random.uniform(0.0, 0.01), 3)),
                    random_corrupt_value(round(random.uniform(0, 100), 2)),
                    random_corrupt_value(round(random.uniform(5, 100), 2)),
                    random_corrupt_value(round(random.uniform(100, 600), 2)),
                    random_corrupt_value(round(random.uniform(0.5, 1.0), 3)),
                    random_corrupt_value(round(random.uniform(0, 24), 2))
                ]
                writer.writerow(row)


# Generate all datasets
generate_wellbore_data()
generate_geophysical_logs()
generate_well_characterization()
generate_seismic_data()
generate_production_data()

print("Data generation complete! Check the CSV files in the current directory.")
