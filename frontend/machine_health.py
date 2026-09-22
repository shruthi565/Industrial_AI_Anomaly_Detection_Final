import tkinter as tk
import json
import os


class MachineHealth:

    def __init__(self, parent):

        self.parent = parent
        self.refresh_id = None

        self.create_ui()

        # Start reading live sensor data
        self.update_status()

        # Refresh every 1 second
        self.refresh_id = self.parent.after(
            1000,
            self.refresh_status
        )

    # ==================================================
    # CREATE UI
    # ==================================================

    def create_ui(self):

        self.page = tk.Frame(
            self.parent,
            bg="#EEF2F7"
        )

        self.page.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # TOP SUMMARY CARDS
        # ==================================================

        summary = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        # Machine status
        self.machine_status_label = self.create_card(
            summary,
            "MACHINE STATUS",
            "HEALTHY",
            "#16A34A"
        )

        # Temperature status
        self.temperature_summary_label = self.create_card(
            summary,
            "TEMPERATURE",
            "NORMAL",
            "#16A34A"
        )

        # Vibration status
        self.vibration_summary_label = self.create_card(
            summary,
            "VIBRATION",
            "NORMAL",
            "#16A34A"
        )

        # Anomaly status
        self.anomaly_summary_label = self.create_card(
            summary,
            "ANOMALY",
            "NOT DETECTED",
            "#64748B"
        )

        # ==================================================
        # MAIN AREA
        # ==================================================

        main_area = tk.Frame(
            self.page,
            bg="#EEF2F7"
        )

        main_area.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # MACHINE OVERVIEW
        # ==================================================

        overview = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid"
        )

        overview.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            overview,
            text="MACHINE OVERVIEW",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # Machine icon

        tk.Label(
            overview,
            text="⚙",
            font=("Segoe UI Symbol", 65),
            bg="white",
            fg="#2563EB"
        ).pack(
            pady=5
        )

        tk.Label(
            overview,
            text="MACHINE 01",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            pady=5
        )

        tk.Label(
            overview,
            text="Industrial Machine Monitoring",
            font=("Arial", 10),
            bg="white",
            fg="#64748B"
        ).pack(
            pady=(0, 20)
        )

        # Machine information

        self.machine_running_label = self.info_row(
            overview,
            "Machine Status",
            "RUNNING",
            "#16A34A"
        )

        self.health_condition_label = self.info_row(
            overview,
            "Health Condition",
            "HEALTHY",
            "#16A34A"
        )

        self.anomaly_status_label = self.info_row(
            overview,
            "Anomaly Status",
            "NORMAL",
            "#16A34A"
        )

        self.monitoring_label = self.info_row(
            overview,
            "Monitoring",
            "ACTIVE",
            "#2563EB"
        )

        # ==================================================
        # SENSOR / AI ANALYSIS
        # ==================================================

        analysis = tk.Frame(
            main_area,
            bg="white",
            bd=1,
            relief="solid",
            width=380
        )

        analysis.pack(
            side="right",
            fill="y"
        )

        analysis.pack_propagate(False)

        tk.Label(
            analysis,
            text="HEALTH ANALYSIS",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        # ==================================================
        # TEMPERATURE
        # ==================================================

        (
            self.temperature_value_label,
            self.temperature_status_label
        ) = self.sensor_box(
            analysis,
            "TEMPERATURE",
            "-- °C",
            "WAITING",
            "#64748B"
        )

        # ==================================================
        # VIBRATION
        # ==================================================

        (
            self.vibration_value_label,
            self.vibration_status_label
        ) = self.sensor_box(
            analysis,
            "VIBRATION",
            "-- mm/s",
            "WAITING",
            "#64748B"
        )

        # ==================================================
        # ISOLATION FOREST
        # ==================================================

        self.sensor_box(
            analysis,
            "ISOLATION FOREST",
            "ACTIVE",
            "MONITORING",
            "#2563EB"
        )

        # ==================================================
        # ALGORITHM INFORMATION
        # ==================================================

        tk.Frame(
            analysis,
            bg="#E2E8F0",
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            analysis,
            text="ANOMALY DETECTION",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#172033"
        ).pack(
            anchor="w",
            padx=25
        )

        algorithm_text = (
            "Isolation Forest\n\n"
            "• Temperature monitoring\n"
            "• Vibration monitoring\n"
            "• Unlabelled sensor data\n"
            "• Normal / anomaly classification\n"
            "• Real-time machine health analysis"
        )

        tk.Label(
            analysis,
            text=algorithm_text,
            font=("Arial", 9),
            bg="white",
            fg="#64748B",
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=12
        )

        # ==================================================
        # FOOTER
        # ==================================================

        tk.Label(
            self.page,
            text=(
                "Machine health is determined using sensor "
                "data and anomaly detection algorithms."
            ),
            font=("Arial", 8),
            bg="#EEF2F7",
            fg="#94A3B8"
        ).pack(
            pady=8
        )

    # ==================================================
    # SUMMARY CARD
    # ==================================================

    def create_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            height=100
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 16, "bold"),
            bg="white",
            fg=color
        )

        value_label.pack(
            anchor="w",
            padx=15
        )

        return value_label

    # ==================================================
    # INFORMATION ROW
    # ==================================================

    def info_row(
        self,
        parent,
        label,
        value,
        color
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=30,
            pady=8
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            side="left"
        )

        value_label = tk.Label(
            row,
            text=value,
            font=("Arial", 9, "bold"),
            bg="white",
            fg=color
        )

        value_label.pack(
            side="right"
        )

        return value_label

    # ==================================================
    # SENSOR BOX
    # ==================================================

    def sensor_box(
        self,
        parent,
        sensor,
        value,
        status,
        color
    ):

        box = tk.Frame(
            parent,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )

        box.pack(
            fill="x",
            padx=20,
            pady=6
        )

        tk.Label(
            box,
            text=sensor,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        value_label = tk.Label(
            box,
            text=value,
            font=("Arial", 16, "bold"),
            bg="#F8FAFC",
            fg="#172033"
        )

        value_label.pack(
            anchor="w",
            padx=15
        )

        status_label = tk.Label(
            box,
            text=status,
            font=("Arial", 9, "bold"),
            bg="#F8FAFC",
            fg=color
        )

        status_label.pack(
            anchor="w",
            padx=15,
            pady=(2, 12)
        )

        return value_label, status_label

    # ==================================================
    # READ LIVE STATUS
    # ==================================================

    def update_status(self):

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        status_file = os.path.join(
            project_root,
            "data",
            "latest_status.json"
        )

        try:

            if not os.path.exists(status_file):
                return

            with open(
                status_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            # ==================================================
            # SENSOR VALUES
            # ==================================================

            temperature = float(
                data.get(
                    "temperature",
                    0
                )
            )

            vibration = float(
                data.get(
                    "vibration",
                    0
                )
            )

            temperature_threshold = float(
                data.get(
                    "temperature_threshold",
                    70.0
                )
            )

            vibration_threshold = float(
                data.get(
                    "vibration_threshold",
                    7.0
                )
            )

            # ==================================================
            # ANOMALY FLAGS
            # ==================================================

            temperature_danger = bool(
                data.get(
                    "temperature_danger",
                    temperature >= temperature_threshold
                )
            )

            vibration_danger = bool(
                data.get(
                    "vibration_danger",
                    vibration >= vibration_threshold
                )
            )

            anomaly = bool(
                data.get(
                    "anomaly",
                    False
                )
            )

            danger = bool(
                data.get(
                    "danger",
                    False
                )
            )

            fall = bool(
                data.get(
                    "fall",
                    False
                )
            )

            hand_danger = bool(
                data.get(
                    "hand_danger",
                    False
                )
            )

            body_danger = bool(
                data.get(
                    "body_danger",
                    False
                )
            )

            # ==================================================
            # OVERALL MACHINE ANOMALY
            # ==================================================

            machine_anomaly = (
                temperature_danger
                or vibration_danger
                or anomaly
                or danger
                or fall
                or hand_danger
                or body_danger
            )

            # ==================================================
            # TEMPERATURE VALUE
            # ==================================================

            self.temperature_value_label.config(
                text=f"{temperature:.2f} °C",
                fg=(
                    "#DC2626"
                    if temperature_danger
                    else "#16A34A"
                )
            )

            # Temperature status
            self.temperature_status_label.config(
                text=(
                    "HIGH"
                    if temperature_danger
                    else "NORMAL"
                ),
                fg=(
                    "#DC2626"
                    if temperature_danger
                    else "#16A34A"
                )
            )

            # ==================================================
            # VIBRATION VALUE
            # ==================================================

            self.vibration_value_label.config(
                text=f"{vibration:.2f} mm/s",
                fg=(
                    "#DC2626"
                    if vibration_danger
                    else "#16A34A"
                )
            )

            # Vibration status
            self.vibration_status_label.config(
                text=(
                    "HIGH"
                    if vibration_danger
                    else "NORMAL"
                ),
                fg=(
                    "#DC2626"
                    if vibration_danger
                    else "#16A34A"
                )
            )

            # ==================================================
            # TOP SUMMARY
            # ==================================================

            if machine_anomaly:

                self.machine_status_label.config(
                    text="ANOMALY",
                    fg="#DC2626"
                )

            else:

                self.machine_status_label.config(
                    text="HEALTHY",
                    fg="#16A34A"
                )

            # Temperature summary

            if temperature_danger:

                self.temperature_summary_label.config(
                    text="HIGH",
                    fg="#DC2626"
                )

            else:

                self.temperature_summary_label.config(
                    text="NORMAL",
                    fg="#16A34A"
                )

            # Vibration summary

            if vibration_danger:

                self.vibration_summary_label.config(
                    text="HIGH",
                    fg="#DC2626"
                )

            else:

                self.vibration_summary_label.config(
                    text="NORMAL",
                    fg="#16A34A"
                )

            # Anomaly summary

            if machine_anomaly:

                self.anomaly_summary_label.config(
                    text="DETECTED",
                    fg="#DC2626"
                )

            else:

                self.anomaly_summary_label.config(
                    text="NOT DETECTED",
                    fg="#64748B"
                )

            # ==================================================
            # MACHINE OVERVIEW
            # ==================================================

            self.machine_running_label.config(
                text=(
                    "RUNNING"
                    if data.get("system") == "ONLINE"
                    else "OFFLINE"
                ),
                fg=(
                    "#16A34A"
                    if data.get("system") == "ONLINE"
                    else "#64748B"
                )
            )

            # Health condition

            if machine_anomaly:

                self.health_condition_label.config(
                    text="ANOMALY",
                    fg="#DC2626"
                )

            else:

                self.health_condition_label.config(
                    text="HEALTHY",
                    fg="#16A34A"
                )

            # Anomaly status

            if machine_anomaly:

                self.anomaly_status_label.config(
                    text="DETECTED",
                    fg="#DC2626"
                )

            else:

                self.anomaly_status_label.config(
                    text="NORMAL",
                    fg="#16A34A"
                )

        except Exception as e:

            print(
                "Machine Health update error:",
                e
            )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh_status(self):

        try:

            if self.page.winfo_exists():

                self.update_status()

                self.refresh_id = self.parent.after(
                    1000,
                    self.refresh_status
                )

        except Exception:

            pass

    # ==================================================
    # CLEANUP
    # ==================================================

    def destroy(self):

        try:

            if self.refresh_id is not None:

                self.parent.after_cancel(
                    self.refresh_id
                )

                self.refresh_id = None

        except Exception:

            pass

        try:

            if self.page.winfo_exists():

                self.page.destroy()

        except Exception:

            pass