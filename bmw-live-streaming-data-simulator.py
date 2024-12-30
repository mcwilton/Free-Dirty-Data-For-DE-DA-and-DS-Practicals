"""
Generate a live stream of BMW telemetric data with random (but somewhat realistic) values
and with a 3% chance of producing an erroneous reading in certain fields.
You can use this data to simulate real-time data ingestion into your BMW telemetric data pipeline.
You can edit the error injection functions to simulate different types of errors.
You can change the 3% chance of error.
Note: This is a very simplified simulation, and the actual BMW telemetric data
"""

import random
import time
import json
from datetime import datetime


def generate_bmw_telemetry_data():

    def maybe_inject_error(value, error_range):
        """
        With 3% probability, create an artificial error by adding an offset
        or completely throwing the value out of normal range.
        """
        if random.random() < 0.03:  # 3% probability
            # For simplicity, let's assume error_range is a function that returns the erroneous value
            return error_range(value)
        return value

    # Example error injection functions
    def large_offset_error(val):
        # Add a large offset (positive or negative) to simulate an obvious outlier
        offset = random.uniform(-val * 2, val * 2)  # up to ±200% of the original
        return round(val + offset, 2)

    def completely_out_of_range_error(val):
        # Generate a new random number that’s far outside normal operating range
        return round(random.uniform(9999, 19999), 2)

    # We can define different error behaviors for different metrics
    def speed_error(val):
        return large_offset_error(val)

    def rpm_error(val):
        # Maybe RPM error is entirely out of range
        return completely_out_of_range_error(val)

    def throttle_error(val):
        # Throttle error might just invert or drastically offset
        return large_offset_error(val)

    # Simulate driver behavior metrics
    speed = random.randint(0, 250)  # Speed in km/h
    rpm = random.randint(600, 8000)  # Engine RPM
    throttle_position = round(random.uniform(0, 100), 2)  # Throttle position (%)
    brake_pedal_pressure = round(random.uniform(0, 100), 2)  # Brake pedal pressure (%)
    steering_angle = round(random.uniform(-90, 90), 2)  # Steering angle in degrees
    seatbelt_fastened = bool(random.getrandbits(1))  # True/False for seatbelt usage

    # Predictive maintenance metrics
    engine_temperature = round(random.uniform(70, 120), 2)  # Engine temperature (°C)
    oil_level = round(random.uniform(2.5, 5.0), 2)  # Liters of engine oil
    tire_pressure_fl = round(random.uniform(28, 35), 2)  # Front-left tire pressure (PSI)
    tire_pressure_fr = round(random.uniform(28, 35), 2)  # Front-right tire pressure (PSI)
    tire_pressure_rl = round(random.uniform(28, 35), 2)  # Rear-left tire pressure (PSI)
    tire_pressure_rr = round(random.uniform(28, 35), 2)  # Rear-right tire pressure (PSI)
    battery_voltage = round(random.uniform(12, 14.5), 2)  # Battery voltage (V)

    # Other telemetry data
    fuel_level = round(random.uniform(0, 100), 2)  # Fuel level (%)
    latitude = round(random.uniform(-90, 90), 6)  # Simulated GPS latitude
    longitude = round(random.uniform(-180, 180), 6)  # Simulated GPS longitude
    gear_position = random.choice(['P', 'R', 'N', 'D', 'S'])  # Gear position
    ambient_temperature = round(random.uniform(-10, 40), 2)  # Outside temperature (°C)
    odometer = random.randint(0, 300000)  # Odometer reading (km)

    # Error injection on key metrics
    speed = maybe_inject_error(speed, speed_error)
    rpm = maybe_inject_error(rpm, rpm_error)
    throttle_position = maybe_inject_error(throttle_position, throttle_error)

    # Timestamp for data record
    timestamp = datetime.utcnow().isoformat()

    data = {
        "timestamp": timestamp,
        "vehicle_model": "BMW",
        "speed_kmh": speed,
        "rpm": rpm,
        "throttle_position_percent": throttle_position,
        "brake_pedal_pressure_percent": brake_pedal_pressure,
        "steering_angle_degrees": steering_angle,
        "seatbelt_fastened": seatbelt_fastened,
        "engine_temperature_celsius": engine_temperature,
        "oil_level_liters": oil_level,
        "tire_pressure_psi": {
            "front_left": tire_pressure_fl,
            "front_right": tire_pressure_fr,
            "rear_left": tire_pressure_rl,
            "rear_right": tire_pressure_rr
        },
        "battery_voltage": battery_voltage,
        "fuel_level_percent": fuel_level,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "gear_position": gear_position,
        "ambient_temperature_celsius": ambient_temperature,
        "odometer_km": odometer
    }

    return data


def main():
    """
    Continuously generates telemetric data for a BMW car, printing to stdout.
    In practice, you can also send this to a file, message queue, or REST endpoint.
    """
    while True:

        telemetry_data = generate_bmw_telemetry_data()
        telemetry_json = json.dumps(telemetry_data)
        print(telemetry_json)
        time.sleep(1)  # Generate new data every second


if __name__ == "__main__":
    main()
