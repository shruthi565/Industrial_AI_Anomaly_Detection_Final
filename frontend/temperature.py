import tkinter as tk
import os
import sys
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
STATUS_FILE = os.path.join(PROJECT_ROOT, "data", "latest_status.json")

class Temperature:
    THRESHOLD = 70.0

    def __init__(self, parent):
        self.parent = parent
        self.temperature = None
        self.after_id = None
        self.create_page()
        self.refresh_temperature()

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", height=90)
        card.pack(side="left", fill="both", expand=True, padx=5)
        card.pack_propagate(False)
        tk.Label(card, text=title, font=("Arial", 8, "bold"), bg="white", fg="#64748B").pack(anchor="w", padx=15, pady=(14,5))
        label = tk.Label(card, text=value, font=("Arial", 16, "bold"), bg="white", fg=color)
        label.pack(anchor="w", padx=15)
        return label

    def create_page(self):
        cards = tk.Frame(self.parent, bg="#EEF2F7")
        cards.pack(fill="x", pady=(0,15))
        self.current_card = self.create_card(cards, "CURRENT TEMPERATURE", "-- °C", "#64748B")
        self.status_card = self.create_card(cards, "TEMPERATURE STATUS", "WAITING", "#64748B")
        self.create_card(cards, "ANOMALY THRESHOLD", "70 °C", "#2563EB")
        self.create_card(cards, "SENSOR", "SIMULATED", "#2563EB")

        main = tk.Frame(self.parent, bg="#EEF2F7")
        main.pack(fill="both", expand=True)

        left = tk.Frame(main, bg="white", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=(0,10))
        tk.Label(left, text="TEMPERATURE MONITORING", font=("Arial",18,"bold"), bg="white", fg="#172033").pack(anchor="w", padx=30, pady=(30,25))
        tk.Label(left, text="🌡", font=("Arial",52), bg="white", fg="#2563EB").pack(pady=(25,5))
        self.big_value = tk.Label(left, text="-- °C", font=("Arial",40,"bold"), bg="white", fg="#172033")
        self.big_value.pack(pady=5)
        self.big_status = tk.Label(left, text="WAITING FOR SENSOR DATA", font=("Arial",16,"bold"), bg="white", fg="#64748B")
        self.big_status.pack(pady=5)
        tk.Label(left, text="Real-time simulated temperature monitoring", font=("Arial",10), bg="white", fg="#64748B").pack(pady=(0,25))
        info = tk.Frame(left, bg="#F8FAFC", bd=1, relief="solid")
        info.pack(fill="x", padx=30, pady=15)
        self.value_info = tk.Label(info, text="Current Value                         -- °C", font=("Arial",10), bg="#F8FAFC", fg="#64748B", anchor="w")
        self.value_info.pack(fill="x", padx=15, pady=10)
        for text in ["Normal Range                         20–70 °C", "Detection Method                    Threshold Monitoring", "Data Type                              Simulated / Arduino Ready"]:
            tk.Label(info, text=text, font=("Arial",10), bg="#F8FAFC", fg="#64748B", anchor="w").pack(fill="x", padx=15, pady=5)

        right = tk.Frame(main, bg="white", bd=1, relief="solid", width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        tk.Label(right, text="TEMPERATURE ANALYSIS", font=("Arial",18,"bold"), bg="white", fg="#172033").pack(anchor="w", padx=25, pady=(30,25))
        self.condition_box = tk.Frame(right, bg="#F0FDF4", bd=1, relief="solid")
        self.condition_box.pack(fill="x", padx=20)
        self.condition_title = tk.Label(self.condition_box, text="WAITING FOR DATA", font=("Arial",10,"bold"), bg="#F0FDF4", fg="#64748B")
        self.condition_title.pack(anchor="w", padx=15, pady=(15,5))
        self.condition_text = tk.Label(self.condition_box, text="Start Live Monitoring to receive simulated temperature values.", font=("Arial",9), bg="#F0FDF4", fg="#64748B", wraplength=250, justify="left")
        self.condition_text.pack(anchor="w", padx=15, pady=(0,15))
        tk.Label(right, text="ANOMALY DETECTION", font=("Arial",10,"bold"), bg="white", fg="#2563EB").pack(anchor="w", padx=25, pady=(25,5))
        self.detection = tk.Label(right, text="Monitoring active.", font=("Arial",9), bg="white", fg="#64748B", wraplength=250, justify="left")
        self.detection.pack(anchor="w", padx=25)
        tk.Frame(right, bg="#E2E8F0", height=1).pack(fill="x", padx=25, pady=20)
        tk.Label(right, text="DETECTION", font=("Arial",10,"bold"), bg="white", fg="#172033").pack(anchor="w", padx=25)
        tk.Label(right, text="Temperature Threshold\n\n• Normal below 70 °C\n• Anomaly at or above 70 °C\n• Real-time monitoring\n• Simulated sensor data\n• Ready for Arduino sensor", font=("Arial",9), bg="white", fg="#64748B", justify="left").pack(anchor="w", padx=25, pady=10)
        tk.Label(right, text="SIMULATED SENSOR", font=("Arial",10,"bold"), bg="white", fg="#2563EB").pack(anchor="w", padx=25, pady=(10,0))
        self.time_label = tk.Label(right, text="Last update: --", font=("Arial",8), bg="white", fg="#94A3B8")
        self.time_label.pack(anchor="w", padx=25, pady=8)

    def read_data(self):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            value = data.get("temperature")
            if value is None:
                return None
            value = float(value)
            danger = bool(data.get("temperature_danger", value >= self.THRESHOLD))
            return value, danger, data.get("time", "--")
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    def refresh_temperature(self):
        # Stop safely if Dashboard destroyed this page.
        try:
            if not self.parent.winfo_exists():
                return
            if not self.current_card.winfo_exists():
                return
        except tk.TclError:
            return

        result = self.read_data()
        if result is None:
            self.current_card.config(text="-- °C", fg="#64748B")
            self.status_card.config(text="WAITING", fg="#64748B")
            self.big_value.config(text="-- °C", fg="#172033")
            self.big_status.config(text="WAITING FOR SENSOR DATA", fg="#64748B")
        else:
            value, danger, update_time = result
            color = "#DC2626" if danger else "#16A34A"
            self.current_card.config(text=f"{value:.1f} °C", fg=color)
            self.status_card.config(text="HIGH" if danger else "NORMAL", fg=color)
            self.big_value.config(text=f"{value:.1f} °C", fg=color if danger else "#172033")
            self.big_status.config(text="HIGH TEMPERATURE" if danger else "NORMAL", fg=color)
            self.value_info.config(text=f"Current Value                         {value:.1f} °C")
            self.time_label.config(text=f"Last update: {update_time}")
            if danger:
                self.condition_box.config(bg="#FEF2F2")
                self.condition_title.config(text="HIGH TEMPERATURE", bg="#FEF2F2", fg="#DC2626")
                self.condition_text.config(text="Temperature has reached or exceeded the anomaly threshold.", bg="#FEF2F2")
                self.detection.config(text="⚠ Temperature anomaly detected.", fg="#DC2626")
            else:
                self.condition_box.config(bg="#F0FDF4")
                self.condition_title.config(text="NORMAL CONDITION", bg="#F0FDF4", fg="#16A34A")
                self.condition_text.config(text="Temperature is within the expected range.", bg="#F0FDF4")
                self.detection.config(text="Monitoring active. No temperature anomaly detected.", fg="#64748B")
        self.after_id = self.parent.after(1000, self.refresh_temperature)


    def destroy(self):
        if self.after_id is not None:
            try:
                self.parent.after_cancel(self.after_id)
            except (tk.TclError, ValueError):
                pass
            self.after_id = None
