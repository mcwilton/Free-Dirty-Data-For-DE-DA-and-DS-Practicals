import os
import random
import datetime

# Directory to store generated SQL files
output_dir = "generated_big_data_sql_files"
os.makedirs(output_dir, exist_ok=True)

# Configuration
NUM_WELLS = 10000  # Number of wells to simulate
NUM_RECORDS_PER_WELL = 100  # Number of records per dataset
well_ids = [f"WELL {i}" for i in range(1, NUM_WELLS)]
ERROR_RATE = 0.40  # Probability of introducing errors


def random_date_range(start_date, end_date):
    """Generate random date range."""
    delta = end_date - start_date
    return start_date + datetime.timedelta(
        days=random.randint(0, delta.days)
    )


def wrong_date_format(date):
    """Change date format to 'dd/mm/yyyy' or 'yyyy-mm-dd'."""
    if "/" in date:
        return date.replace("/", "-")
    else:
        return date.replace("-", "/")


def wrong_date_format_numbers(date):
    """ change date format to "dd/mm/yyyy" or "yyyy/mm/dd" or "mm/dd/yyyy ."""
    if "/" in date:
        part1, part2, part3 = date.split("/")
        return f"{part2}/{part1}/{part3}"
    else:
        part1_dash, part2_dash, part3_dash = date.split("-")
        return f"{part3_dash}-{part2_dash}-{part1_dash}"


years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
days = random.randint(1, 28)
month = random.randint(1, 12)
date_format1 = str(years[random.randint(0, len(years) - 1)]) + "-" + str(days) + "-" + str(month)
date_format2 = f"{str(month)}{"/"}{str(days)}{"/"}{str(years[random.randint(0, len(years) - 1)])} "


# Helper Functions
def random_value(val_range, is_float=False):
    """Generate random value with a chance of NULL or error."""
    if random.random() < ERROR_RATE:
        return random.choice(
            ["NULL", "N/A", random.randint(9999999, 99999999)])  # Wrong data type or missing
    return round(random.uniform(*val_range), 2) if is_float else random.randint(*val_range)


def random_date(start_date, days_range=365):
    """Generate random dates with chance of errors."""
    if random.random() < ERROR_RATE:
        return random.choice(["NULL", "INVALID_DATE", date_format1, date_format2])  # Messed-up dates
    random_days = random.randint(0, days_range)
    return (start_date + datetime.timedelta(days=random_days)).isoformat()


def format_sql_value(value):
    """Format value for SQL (e.g., wrap strings in quotes)."""
    if value in ["NULL", "INVALID_DATE", "N/A"]:
        return value
    return f"'{value}'" if isinstance(value, str) else value


# Dataset Generators
def generate_wellbore_data():
    table_name = "wellbore_data"
    columns = [
        "well_id TEXT", "date DATE", "measured_depth_m FLOAT", "mud_weight_ppg FLOAT",
        "rop_m_per_hr FLOAT", "borehole_diameter_in FLOAT", "bit_type TEXT",
        "pump_pressure_psi FLOAT", "rpm INT", "torque_ft_lbs FLOAT", "standpipe_pressure FLOAT",
        "fluid_loss_rate FLOAT", "direction_azimuth_deg FLOAT", "inclination_deg FLOAT",
        "formation_pressure_psi FLOAT", "wellhead_temperature FLOAT", "bit_wear_index FLOAT",
        "drill_time_hours FLOAT", "block_height_m FLOAT", "well_status TEXT", "well_location TEXT"
    ]
    file_path = os.path.join(output_dir, f"{table_name}.sql")
    with open(file_path, "w") as f:
        f.write(f"CREATE TABLE {table_name} (\n    {', '.join(columns)}\n)\n\n")
        start_date = datetime.date(2010, 1, 1)
        for well_id in well_ids:
            for _ in range(NUM_RECORDS_PER_WELL):
                row = [
                    format_sql_value(well_id),
                    format_sql_value(random_date(start_date)),
                    random_value((100, 5000), True),
                    random_value((8.5, 12.0), True),
                    random_value((5, 30), True),
                    random_value((8.5, 12.25), True),
                    random.choice(["PDC", "Roller Cone", "Diamond", "ERROR"]),
                    random_value((500, 5000), True),
                    random_value((50, 200)),
                    random_value((100, 10000), True),
                    random_value((500, 5000), True),
                    random_value((0, 50), True),
                    random_value((0, 360), True),
                    random_value((0, 90), True),
                    random_value((1000, 5000), True),
                    random_value((20, 120), True),
                    random_value((0, 1), True),
                    random_value((0, 100), True),
                    random_value((0, 50), True),
                    random.choice(["Active", "Inactive", "Under Maintenance", "NULL"]),
                    random.choice(["Dubai", "Texas", "Nigeria", "Calgary", "Mzarabani", "NULL"]),
                ]
                f.write(f"INSERT INTO {table_name} VALUES ({', '.join(map(str, row))});\n")


def generate_geophysical_logs():
    table_name = "geophysical_logs"
    columns = [
        "well_id TEXT", "depth_m FLOAT", "gamma_ray_api FLOAT", "resistivity_ohm_m FLOAT",
        "sonic_dt_us_ft FLOAT", "density_g_cc FLOAT", "caliper_in FLOAT",
        "neutron_porosity FLOAT", "bulk_modulus_gpa FLOAT", "shear_modulus_gpa FLOAT",
        "poisson_ratio FLOAT", "velocity_m_s FLOAT", "shale_volume FLOAT",
        "clay_content FLOAT", "water_saturation FLOAT", "hydrocarbon_saturation FLOAT",
        "permeability_md FLOAT", "lithology TEXT", "wavelet_type TEXT", "survey_name TEXT"
    ]
    file_path = os.path.join(output_dir, f"{table_name}.sql")
    with open(file_path, "w") as f:
        f.write(f"CREATE TABLE {table_name} (\n    {', '.join(columns)}\n)\n\n")
        for well_id in well_ids:
            for _ in range(NUM_RECORDS_PER_WELL):
                row = [
                    format_sql_value(well_id),
                    random_value((0, 5000), True),
                    random_value((20, 150), True),
                    random_value((0.5, 200), True),
                    random_value((50, 120), True),
                    random_value((1.9, 2.7), True),
                    random_value((8.5, 16), True),
                    random_value((0.05, 0.35), True),
                    random_value((10, 50), True),
                    random_value((5, 30), True),
                    random_value((0.1, 0.4), True),
                    random_value((1000, 5000), True),
                    random_value((0.1, 0.8), True),
                    random_value((0.1, 0.5), True),
                    random_value((0.2, 1.0), True),
                    random_value((0.2, 0.8), True),
                    random_value((0.1, 1000), True),
                    random.choice(["Sandstone", "Shale", "Limestone", "Dolomite", "INVALID"]),
                    random.choice(["Ricker", "Ormsby", "Klauder", "INVALID"]),
                    random.choice(["SurveyA", "SurveyB", "SurveyC", "ERROR"])
                ]
                f.write(f"INSERT INTO {table_name} VALUES ({', '.join(map(str, row))});\n")


# Add more datasets with similar structure
datasets = [
    generate_wellbore_data,
    generate_geophysical_logs,
]

# Generate SQL Files
for dataset_generator in datasets:
    dataset_generator()

print(f"SQL files for big data datasets with quality issues have been generated in the '{output_dir}' directory.")
