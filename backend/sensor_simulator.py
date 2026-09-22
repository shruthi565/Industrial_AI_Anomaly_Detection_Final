import random
import time


class SensorSimulator:

    def __init__(self):
        self.temperature = 30.0
        self.vibration = 1.0

        # Thresholds
        self.temperature_threshold = 70.0
        self.vibration_threshold = 7.0

        # Current simulation mode
        self.mode = "normal"

    def set_mode(self, mode):
        """
        Modes:
        normal
        high_temperature
        high_vibration
        both
        """

        self.mode = mode

    def generate_data(self):

        # -----------------------------
        # NORMAL CONDITION
        # -----------------------------

        if self.mode == "normal":

            temperature = random.uniform(28, 35)
            vibration = random.uniform(0.5, 2.0)

        # -----------------------------
        # HIGH TEMPERATURE
        # -----------------------------

        elif self.mode == "high_temperature":

            temperature = random.uniform(72, 90)
            vibration = random.uniform(0.5, 2.0)

        # -----------------------------
        # HIGH VIBRATION
        # -----------------------------

        elif self.mode == "high_vibration":

            temperature = random.uniform(28, 35)
            vibration = random.uniform(8, 12)

        # -----------------------------
        # BOTH ABNORMAL
        # -----------------------------

        elif self.mode == "both":

            temperature = random.uniform(75, 95)
            vibration = random.uniform(8, 12)

        else:

            temperature = 30
            vibration = 1

        return {
            "temperature": round(temperature, 2),
            "vibration": round(vibration, 2)
        }

    def check_anomaly(self, data):

        temperature_anomaly = (
            data["temperature"] >= self.temperature_threshold
        )

        vibration_anomaly = (
            data["vibration"] >= self.vibration_threshold
        )

        return {
            "temperature_anomaly": temperature_anomaly,
            "vibration_anomaly": vibration_anomaly
        }


if __name__ == "__main__":

    sensor = SensorSimulator()

    # Change this to test different conditions
    sensor.set_mode("both")

    while True:

        data = sensor.generate_data()

        result = sensor.check_anomaly(data)

        print("--------------------------------")
        print("Temperature:", data["temperature"], "°C")
        print("Vibration:", data["vibration"], "mm/s")

        if result["temperature_anomaly"]:
            print("⚠ HIGH TEMPERATURE")

        else:
            print("✓ Temperature NORMAL")

        if result["vibration_anomaly"]:
            print("⚠ HIGH VIBRATION")

        else:
            print("✓ Vibration NORMAL")

        time.sleep(2)