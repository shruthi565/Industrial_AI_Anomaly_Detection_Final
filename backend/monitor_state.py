import os
import cv2
from datetime import datetime


class MonitorState:

    def __init__(self):
        # ==============================
        # SYSTEM STATUS
        # ==============================
        self.system_status = "ONLINE"

        # ==============================
        # WORKER STATUS
        # ==============================
        self.worker_status = "NOT DETECTED"

        # ==============================
        # MACHINE STATUS
        # ==============================
        self.machine_status = "NORMAL"

        # ==============================
        # SAFETY STATUS
        # ==============================
        self.danger_status = "SAFE"
        self.fall_status = "NOT DETECTED"

        # ==============================
        # TEMPERATURE SENSOR
        # ==============================
        self.temperature = 30.0
        self.temperature_status = "NORMAL"

        # ==============================
        # VIBRATION SENSOR
        # ==============================
        self.vibration = 1.0
        self.vibration_status = "NORMAL"

        # ==============================
        # SENSOR THRESHOLDS
        # ==============================
        self.temperature_threshold = 70.0
        self.vibration_threshold = 7.0

        # ==============================
        # ALERT INFORMATION
        # ==============================
        self.active_alerts = 0

        self.latest_incident = {
            "status": "NO INCIDENT",
            "type": "No incident recorded",
            "time": "--",
            "location": "--",
            "priority": "--"
        }

        # Store recent alerts
        self.recent_alerts = []

        # Latest incident image
        self.latest_image = None

        # Create data folder if it doesn't exist
        os.makedirs("data", exist_ok=True)

    # ==========================================================
    # UPDATE TEMPERATURE AND VIBRATION
    # ==========================================================
    def update_sensors(self, temperature, vibration):

        # Store sensor values
        self.temperature = temperature
        self.vibration = vibration

        # Check temperature
        if temperature >= self.temperature_threshold:
            self.temperature_status = "HIGH"
        else:
            self.temperature_status = "NORMAL"

        # Check vibration
        if vibration >= self.vibration_threshold:
            self.vibration_status = "HIGH"
        else:
            self.vibration_status = "NORMAL"

        # Update overall machine status
        if (
            self.temperature_status == "HIGH"
            or self.vibration_status == "HIGH"
        ):
            self.machine_status = "ANOMALY"
        else:
            self.machine_status = "NORMAL"

    # ==========================================================
    # ADD INCIDENT / ALERT
    # ==========================================================
    def add_incident(
        self,
        incident_type,
        location="Zone A",
        priority="HIGH",
        frame=None
    ):

        now = datetime.now()

        # Update latest incident
        self.latest_incident = {
            "status": "ACTIVE",
            "type": incident_type,
            "time": now.strftime("%I:%M:%S %p"),
            "location": location,
            "priority": priority
        }

        # Increase active alert count
        self.active_alerts += 1

        # Save incident image if available
        if frame is not None:

            image_path = os.path.join(
                "data",
                "latest_incident.jpg"
            )

            cv2.imwrite(image_path, frame)

            self.latest_image = image_path

        # Add alert to recent alerts
        self.recent_alerts.insert(
            0,
            {
                "time": now.strftime("%I:%M:%S %p"),
                "type": incident_type,
                "location": location,
                "priority": priority,
                "status": "ACTIVE"
            }
        )

        # Keep only latest 5 alerts
        self.recent_alerts = self.recent_alerts[:5]

    # ==========================================================
    # CLEAR ALL ALERTS
    # ==========================================================
    def clear_alerts(self):

        self.active_alerts = 0

        self.latest_incident = {
            "status": "NO INCIDENT",
            "type": "No incident recorded",
            "time": "--",
            "location": "--",
            "priority": "--"
        }

        # Mark recent alerts as cleared
        for alert in self.recent_alerts:
            alert["status"] = "CLEARED"


# ==============================================================
# GLOBAL MONITOR STATE OBJECT
# ==============================================================

monitor_state = MonitorState()