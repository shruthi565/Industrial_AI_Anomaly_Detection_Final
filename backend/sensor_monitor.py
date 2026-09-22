import time

from backend.sensor_simulator import SensorSimulator
from backend.decision_logic import DecisionLogic
from backend.monitor_state import monitor_state


# Create objects
sensor = SensorSimulator()
decision = DecisionLogic()

# Start in normal mode
sensor.set_mode("both")

# Used to prevent repeated alerts
previous_temp_anomaly = False
previous_vibration_anomaly = False


print("======================================")
print("   INDUSTRIAL SENSOR MONITOR")
print("======================================")
print("Sensor monitoring started...")
print()


while True:

    # ----------------------------------
    # Generate sensor values
    # ----------------------------------
    data = sensor.generate_data()

    temperature = data["temperature"]
    vibration = data["vibration"]

    # ----------------------------------
    # Check sensor anomalies
    # ----------------------------------
    anomalies = sensor.check_anomaly(data)

    temperature_anomaly = anomalies["temperature_anomaly"]
    vibration_anomaly = anomalies["vibration_anomaly"]

    # ----------------------------------
    # Update monitor state
    # ----------------------------------
    monitor_state.update_sensors(
        temperature,
        vibration
    )

    # ----------------------------------
    # Get final system status
    # ----------------------------------
    status = decision.get_status(
        temp_anomaly=temperature_anomaly,
        vibration_anomaly=vibration_anomaly
    )

    # ----------------------------------
    # Display sensor information
    # ----------------------------------
    print("--------------------------------------")
    print(f"Temperature : {temperature} °C")
    print(f"Vibration   : {vibration} mm/s")

    print(
        f"Temperature Status : "
        f"{monitor_state.temperature_status}"
    )

    print(
        f"Vibration Status   : "
        f"{monitor_state.vibration_status}"
    )

    print(
        f"Machine Status     : "
        f"{monitor_state.machine_status}"
    )

    print(f"FINAL STATUS       : {status}")

    # ----------------------------------
    # Temperature alert
    # ----------------------------------
    if temperature_anomaly:

        print("⚠ HIGH TEMPERATURE DETECTED!")

        # Create alert only when anomaly starts
        if not previous_temp_anomaly:

            monitor_state.add_incident(
                incident_type="HIGH TEMPERATURE",
                location="Machine 1",
                priority="HIGH"
            )

    # ----------------------------------
    # Vibration alert
    # ----------------------------------
    if vibration_anomaly:

        print("⚠ HIGH VIBRATION DETECTED!")

        # Create alert only when anomaly starts
        if not previous_vibration_anomaly:

            monitor_state.add_incident(
                incident_type="HIGH VIBRATION",
                location="Machine 1",
                priority="HIGH"
            )

    # ----------------------------------
    # Normal condition
    # ----------------------------------
    if not temperature_anomaly and not vibration_anomaly:

        print("✓ All sensor values are NORMAL")

    # ----------------------------------
    # Remember previous state
    # ----------------------------------
    previous_temp_anomaly = temperature_anomaly
    previous_vibration_anomaly = vibration_anomaly

    # Wait before next reading
    time.sleep(2)