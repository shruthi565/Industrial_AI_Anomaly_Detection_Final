import os
import json
import tkinter as tk
from datetime import datetime


# ============================================================
# PROJECT ROOT
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STATUS_FILE = os.path.join(DATA_DIR, "latest_status.json")
INCIDENT_FILE = os.path.join(DATA_DIR, "incident_history.json")

try:
    from backend.incident_manager import IncidentManager
except ImportError:
    IncidentManager = None


# ============================================================
# FRONTEND FINAL INTEGRATION
# ============================================================

class FrontendFinalIntegration:
    """A compact frontend integration layer for the alert display,
    incident history display, and final dashboard summary flow.

    This file intentionally does not edit the existing UI files.
    It provides a reusable integration widget that can be imported
    by the dashboard and connected to the current project data files.
    """

    def __init__(self, parent):
        self.parent = parent

        self.alerts = []
        self.logs = []
        self.alert_signatures = set()

        self.manager = None
        if IncidentManager is not None:
            try:
                self.manager = IncidentManager()
            except Exception as error:
                print("Incident manager init error:", error)
                self.manager = None

        # Keep one alert per normalized event signature so the
        # final integration screen does not reinsert the same status
        # message at every auto-refresh pass.
        self.alert_signatures = set()

        self.page = None
        self.total_card = None
        self.critical_card = None
        self.warning_card = None
        self.status_card = None
        self.alert_list = None
        self.logs_frame = None
        self.refresh_id = None

        self.create_ui()
        self.load_status()
        self.load_incidents()
        self.auto_refresh()

    # =======================================================
    # CREATE UI
    # =======================================================

    def create_ui(self):
        self.page = tk.Frame(self.parent, bg="#EEF2F7")
        self.page.pack(fill="both", expand=True)

        # Summary cards
        summary = tk.Frame(self.page, bg="#EEF2F7")
        summary.pack(fill="x", pady=(0, 15))

        self.total_card = self.create_card(summary, "TOTAL ALERTS", "0", "#2563EB")
        self.critical_card = self.create_card(summary, "CRITICAL", "0", "#DC2626")
        self.warning_card = self.create_card(summary, "WARNING", "0", "#F59E0B")
        self.status_card = self.create_card(summary, "SYSTEM STATUS", "SAFE", "#16A34A")

        # Main panel
        main = tk.Frame(self.page, bg="#EEF2F7")
        main.pack(fill="both", expand=True)

        # Left alert list area
        alert_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        alert_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        header = tk.Frame(alert_frame, bg="white")
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(header, text="SAFETY ALERTS", font=("Arial", 15, "bold"),
                 bg="white", fg="#172033").pack(side="left")

        tk.Button(header, text="CLEAR ALERTS", font=("Arial", 9, "bold"),
                  bg="#F1F5F9", fg="#475569", relief="flat",
                  cursor="hand2", command=self.clear_alerts).pack(side="right")

        list_container = tk.Frame(alert_frame, bg="#F8FAFC")
        list_container.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self.canvas = tk.Canvas(list_container, bg="#F8FAFC", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)

        self.alert_list = tk.Frame(self.canvas, bg="#F8FAFC")
        self.alert_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.alert_list, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right incident history area
        incident_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        incident_frame.pack(side="right", fill="y")

        tk.Label(incident_frame, text="INCIDENT HISTORY", font=("Arial", 15, "bold"),
                 bg="white", fg="#172033").pack(anchor="w", padx=20, pady=(20, 10))

        self.logs_frame = tk.Frame(incident_frame, bg="#F8FAFC")
        self.logs_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    # =======================================================
    # SUMMARY CARD
    # =======================================================

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", height=100)
        card.pack(side="left", fill="both", expand=True, padx=5)
        card.pack_propagate(False)

        tk.Label(card, text=title, font=("Arial", 9, "bold"), bg="white", fg="#64748B").pack(
            anchor="w", padx=15, pady=(15, 5)
        )

        label = tk.Label(card, text=value, font=("Arial", 16, "bold"), bg="white", fg=color)
        label.pack(anchor="w", padx=15)

        return label

    # =======================================================
    # LOAD STATUS
    # =======================================================

    def load_status(self):
        if not os.path.exists(STATUS_FILE):
            return

        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Read all relevant booleans from the same file source.
            worker = bool(data.get("worker", False))
            danger = bool(data.get("danger", False))
            hand_danger = bool(data.get("hand_danger", False))
            body_danger = bool(data.get("body_danger", False))
            fall = bool(data.get("fall", False))
            anomaly = bool(data.get("anomaly", False))
            temperature_danger = bool(data.get("temperature_danger", False))
            vibration_danger = bool(data.get("vibration_danger", False))
            hazard_detected = bool(data.get("hazard_detected", False))
            timestamp = data.get("time", datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"))

            # Only emit alert cards for actual abnormal states. The former
            # worker-safe branch inserted a synthetic SAFE alert from the
            # same file every refresh cycle, which made the UI feel random.
            if fall:
                alert_type = "CRITICAL"
                alert_message = "Worker fall detected"
            elif danger or body_danger or hand_danger:
                alert_type = "HIGH RISK"
                alert_message = "Worker entered danger zone"
            elif anomaly:
                alert_type = "WARNING"
                alert_message = "Industrial anomaly detected"
            elif temperature_danger:
                alert_type = "HIGH RISK"
                alert_message = "High temperature detected"
            elif vibration_danger:
                alert_type = "WARNING"
                alert_message = "Vibration anomaly detected"
            elif hazard_detected and worker:
                alert_type = "WARNING"
                alert_message = str(data.get("message", "Industrial hazard detected"))
            else:
                # No active abnormal state, so there is no event to append.
                return

            self.add_alert(alert_type, alert_message, "System", timestamp)

        except Exception as error:
            print("Status integration error:", error)

    # =======================================================
    # ADD ALERT
    # =======================================================

    def add_alert(self, alert_type, message, source="System", timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        # The test path and the live UI path both hit this method.
        # Keep the guard robust when alert_signatures is absent.
        if not hasattr(self, "alert_signatures"):
            self.alert_signatures = set()

        # Normalize repeated data from the same status file into a single
        # event key. This prevents auto-refresh loops from re-rendering the
        # same incident as a new card every 2 seconds.
        key = f"{str(alert_type).upper()}|{str(message).strip().lower()}|{str(source).strip().lower()}"
        if key in self.alert_signatures:
            return

        self.alert_signatures.add(key)

        alert = {
            "type": alert_type,
            "message": message,
            "source": source,
            "time": timestamp,
        }
        self.alerts.insert(0, alert)
        self.alerts = self.alerts[:50]

        # Only refresh widgets if the frame exists; allows test and import
        # scenarios to call the method without a live Tk canvas.
        if hasattr(self, "alert_list") and self.alert_list is not None:
            self.refresh_alerts()

    # =======================================================
    # REFRESH ALERTS
    # =======================================================

    def refresh_alerts(self):
        for widget in self.alert_list.winfo_children():
            widget.destroy()

        if not self.alerts:
            tk.Label(self.alert_list, text="No safety alerts detected",
                     font=("Arial", 11), bg="#F8FAFC", fg="#94A3B8").pack(pady=60)
            self.update_alert_summary()
            return

        for alert in self.alerts:
            self.create_alert_item(alert)

        self.update_alert_summary()

    # =======================================================
    # CREATE ALERT ITEM
    # =======================================================

    def create_alert_item(self, alert):
        alert_type = alert.get("type", "INFO")
        color = {
            "CRITICAL": "#DC2626",
            "HIGH RISK": "#EA580C",
            "WARNING": "#F59E0B",
        }.get(alert_type, "#2563EB")

        item = tk.Frame(self.alert_list, bg="white", bd=1, relief="solid")
        item.pack(fill="x", padx=10, pady=5)

        tk.Frame(item, bg=color, width=5).pack(side="left", fill="y")

        content = tk.Frame(item, bg="white")
        content.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        top = tk.Frame(content, bg="white")
        top.pack(fill="x")

        tk.Label(top, text=alert_type, font=("Arial", 9, "bold"), bg="white", fg=color).pack(side="left")
        tk.Label(top, text=alert.get("time", "--"), font=("Arial", 8), bg="white", fg="#94A3B8").pack(side="right")

        tk.Label(content, text=alert.get("message", ""), font=("Arial", 10, "bold"),
                 bg="white", fg="#172033", anchor="w", wraplength=600).pack(fill="x", pady=(5, 2))

        tk.Label(content, text=f"Source: {alert.get('source', 'System')}", font=("Arial", 8),
                 bg="white", fg="#64748B", anchor="w").pack(fill="x")

    # =======================================================
    # UPDATE ALERT SUMMARY
    # =======================================================

    def update_alert_summary(self):
        total = len(self.alerts)
        critical = sum(1 for a in self.alerts if a.get("type") == "CRITICAL")
        warning = sum(1 for a in self.alerts if a.get("type") in ["WARNING", "HIGH RISK"])

        self.total_card.config(text=str(total))
        self.critical_card.config(text=str(critical))
        self.warning_card.config(text=str(warning))

        if critical > 0:
            self.status_card.config(text="CRITICAL", fg="#DC2626")
        elif warning > 0:
            self.status_card.config(text="WARNING", fg="#F59E0B")
        else:
            self.status_card.config(text="SAFE", fg="#16A34A")

    # =======================================================
    # LOAD INCIDENTS
    # =======================================================

    def load_incidents(self):
        if self.manager is None:
            self.logs = []
            self.refresh_incidents()
            return

        try:
            self.logs = self.manager.get_incidents()
            if self.logs is None:
                self.logs = []
        except Exception as error:
            print("Incident history load error:", error)
            self.logs = []

        self.refresh_incidents()

    # =======================================================
    # REFRESH INCIDENTS
    # =======================================================

    def refresh_incidents(self):
        for widget in self.logs_frame.winfo_children():
            widget.destroy()

        if not self.logs:
            tk.Label(self.logs_frame, text="No incidents recorded",
                     font=("Arial", 10), bg="#F8FAFC", fg="#94A3B8").pack(pady=60)
            return

        for incident in self.logs[:20]:
            if isinstance(incident, dict):
                self.create_incident_row(incident)

    # =======================================================
    # CREATE INCIDENT ROW
    # =======================================================

    def create_incident_row(self, incident):
        row = tk.Frame(self.logs_frame, bg="white", bd=1, relief="solid")
        row.pack(fill="x", pady=3)

        incident_type = str(incident.get("type", "UNKNOWN"))
        color = {
            "FALL": "#DC2626",
            "DANGER ZONE": "#EA580C",
            "TEMPERATURE": "#F59E0B",
            "VIBRATION": "#F59E0B",
            "ANOMALY": "#F59E0B",
        }.get(incident_type, "#2563EB")

        fields = [
            incident.get("date", "--"),
            incident.get("time", "--"),
            incident_type,
            incident.get("description", ""),
            incident.get("source", "System"),
            incident.get("status", "OPEN"),
        ]

        for index, value in enumerate(fields):
            fg = color if index == 2 else "#475569"
            font_style = "bold" if index == 2 else "normal"
            tk.Label(row, text=str(value), font=("Arial", 8, font_style), bg="white", fg=fg,
                     width=[14, 10, 20, 40, 25, 15][index], anchor="w").pack(side="left", padx=5, pady=10)

    # =======================================================
    # CLEAR ALERTS
    # =======================================================

    def clear_alerts(self):
        self.alerts = []
        self.refresh_alerts()

    # =======================================================
    # AUTO REFRESH
    # =======================================================

    def auto_refresh(self):
        try:
            if self.page.winfo_exists():
                self.load_status()
                self.load_incidents()
                self.refresh_id = self.page.after(2000, self.auto_refresh)
        except Exception:
            pass

    # =======================================================
    # DESTROY
    # =======================================================

    def destroy(self):
        try:
            if self.refresh_id is not None:
                self.page.after_cancel(self.refresh_id)
        except Exception:
            pass

        try:
            if self.page.winfo_exists():
                self.page.destroy()
        except Exception:
            pass
