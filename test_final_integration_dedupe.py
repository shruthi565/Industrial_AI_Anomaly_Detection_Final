import os
import sys

sys.path.insert(0, os.getcwd())

from frontend.final_integration import FrontendFinalIntegration


def test_add_alert_skips_duplicate_event():
    widget = object.__new__(FrontendFinalIntegration)
    widget.alerts = []
    widget.alert_signatures = set()
    widget.alert_list = None
    widget.total_card = None
    widget.critical_card = None
    widget.warning_card = None
    widget.status_card = None

    event = {
        "type": "WARNING",
        "message": "Industrial anomaly detected",
        "source": "System",
        "time": "08-09-2026 01:38:54 PM",
    }

    widget.add_alert(event["type"], event["message"], event["source"], event["time"])
    widget.add_alert(event["type"], event["message"], event["source"], event["time"])

    assert len(widget.alerts) == 1
