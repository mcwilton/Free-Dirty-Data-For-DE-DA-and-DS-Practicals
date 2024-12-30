"""
Note that the data generated is full of errors, and should not be used for any serious data analysis. It's meant
 for practical use.
"""
import csv
import random
import datetime

# Configuration
output_file = "wellbore_data_with_places.csv"
cities = [
    {"city": "Houston", "country": "USA"},
    {"city": "Calgary", "country": "Canada"},
    {"city": "Aberdeen", "country": "UK"},
    {"city": "Dubai", "country": "UAE"},
    {"city": "Luanda", "country": "Angola"},
    {"city": "Perth", "country": "Australia"},
    {"city": "Stavanger", "country": "Norway"},
    {"city": "Rio de Janeiro", "country": "Brazil"},
    {"city": "Doha", "country": "Qatar"},
    {"city": "Jakarta", "country": "Indonesia"},
]
min_wells_per_place = 2200
max_wells_per_place = 2500
wrong_date_formats = ["MM/DD/YYYY", "DD-MM-YYYY", "INVALID_DATE", " "]


# Helper Functions
def random_date(start_year, end_year, include_wrong_format=False):
    """Generate a random date within the specified range, with optional wrong formats."""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    date = start_date + datetime.timedelta(days=random_days)

    if include_wrong_format and random.random() < 0.25:  # 15% chance for a wrong date format
        return random.choice([
            date.strftime("%m/%d/%Y"),  # MM/DD/YYYY
            date.strftime("%d-%m-%Y"),  # DD-MM-YYYY
            "31/02/2023",  # Invalid date
            "NULL",  # Missing date
        ])
    return date.strftime("%Y-%m-%d")  # Default correct format


def random_status():
    return random.choice(["Active", "Inactive", "Maintenance", "Abandoned", "NULL", "ERROR"])


def random_operator():
    return random.choice(["Schlumberger", "Halliburton", "Baker Hughes", "Weatherford", "UNKNOWN", "ERROR"])


def random_formation():
    return random.choice(["Sandstone", "Shale", "Limestone", "Dolomite", "Granite", "UNKNOWN"])


def random_pressure():
    if random.random() < 0.1:  # 10% chance of an error
        return random.choice(["NULL", "ERROR", "N/A", random.randint(99999, 9999999)])
    return f"{random.randint(1000, 15000)} PSI"


# Generate the CSV data
header = [
    "CITY", "COUNTRY", "WELL_ID", "DEPTH_FT", "PRESSURE_PSI", "TEMPERATURE_F", "DATE_LOGGED",
    "STATUS", "LATITUDE", "LONGITUDE", "OPERATOR", "FORMATION", "POROSITY", "PERMEABILITY",
    "MUD_WEIGHT_PPG", "CASING_SIZE_IN", "CEMENT_TYPE", "SPUD_DATE", "COMPLETION_DATE",
    "LAST_INSPECTION", "PRODUCTION_RATE_BBL", "WATER_CUT_PERCENT"
]

rows = []

for place in cities:
    city, country = place["city"], place["country"]
    num_wells = random.randint(min_wells_per_place, max_wells_per_place)
    for i in range(num_wells):
        well_id = f"WELL-{random.randint(1000, 9999)}-{city[:3].upper()}"
        depth_ft = random.randint(100, 15000)
        pressure_psi = random_pressure()
        temperature_f = random.randint(50, 350)
        date_logged = random_date(2015, 2023, include_wrong_format=True)
        status = random_status()
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        operator = random_operator()
        formation = random_formation()
        porosity = round(random.uniform(0.05, 0.3), 5)
        permeability = round(random.uniform(0.01, 1000), 6)
        mud_weight_ppg = random.choice(["8.5", "9.0", "10.0", "ERROR", "N/A", "NULL"])
        casing_size_in = round(random.uniform(4.5, 20.0), 2)
        cement_type = random.choice(["Type I", "Type II", "Type III", "Type IV", "UNKNOWN"])
        spud_date = random_date(2000, 2015, include_wrong_format=True)
        completion_date = random_date(2015, 2023, include_wrong_format=True)
        last_inspection = random_date(2020, 2023, include_wrong_format=True)
        production_rate_bbl = random.randint(0, 5000)
        water_cut_percent = random.randint(0, 100)

        rows.append([
            city, country, well_id, depth_ft, pressure_psi, temperature_f, date_logged, status,
            latitude, longitude, operator, formation, porosity, permeability, mud_weight_ppg,
            casing_size_in, cement_type, spud_date, completion_date, last_inspection,
            production_rate_bbl, water_cut_percent
        ])

# Write to CSV
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print(f"CSV file '{output_file}' with data for 10 cities and their wells has been generated.")
