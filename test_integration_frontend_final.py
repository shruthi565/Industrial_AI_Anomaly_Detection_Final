import os
import tempfile
import unittest

from backend.incident_manager import IncidentManager


class FrontendFinalIntegrationSmokeTest(unittest.TestCase):
    """Smoke test for the frontend-final integration surface: incident history and alert workflow."""

    def test_incident_history_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            manager = IncidentManager()
            manager.incident_file = os.path.join(tmp_dir, "incident_history.json")
            manager.create_file_if_needed()

            manager.save_incident(
                "FALL",
                "Worker fall detected",
                "Fall Detection",
                "CRITICAL"
            )

            incidents = manager.get_incidents()
            self.assertIsInstance(incidents, list)
            self.assertGreaterEqual(len(incidents), 1)
            self.assertEqual(incidents[0]["type"], "FALL")
            self.assertEqual(incidents[0]["source"], "Fall Detection")
            self.assertEqual(incidents[0]["status"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
