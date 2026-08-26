import unittest
from unittest.mock import patch
from tools.powerbi_tools import (
    DASHBOARD_REGISTRY,
    get_dashboard_health,
    trigger_dataset_refresh,
    get_all_dashboard_statuses,
    HEALTH_WEIGHTS,
    FAILURE_REASONS
)

class TestPowerBITools(unittest.TestCase):

    def test_registry_length(self):
        """Test that the dashboard registry contains exactly 3 dashboards."""
        self.assertEqual(len(DASHBOARD_REGISTRY), 3)

    def test_registry_contains_dashboard_001(self):
        """Test that dashboard_001 is in the registry."""
        dashboard_ids = [d["dashboard_id"] for d in DASHBOARD_REGISTRY]
        self.assertIn("dashboard_001", dashboard_ids)

    def test_get_dashboard_health_valid(self):
        """Test getting health for a valid dashboard returns a valid status."""
        health = get_dashboard_health("dashboard_001")
        self.assertEqual(health["dashboard_id"], "dashboard_001")
        self.assertIn(health["status"], HEALTH_WEIGHTS.keys())
        self.assertIn("checked_at", health)

    def test_get_dashboard_health_invalid(self):
        """Test getting health for an invalid dashboard returns failed status."""
        health = get_dashboard_health("invalid_dashboard")
        self.assertEqual(health["dashboard_id"], "invalid_dashboard")
        self.assertEqual(health["status"], "failed")
        self.assertIn("not found in registry", health["failure_reason"])

    def test_trigger_dataset_refresh(self):
        """Test triggering a dataset refresh returns expected triggered status."""
        response = trigger_dataset_refresh("dataset_001")
        self.assertEqual(response["dataset_id"], "dataset_001")
        self.assertEqual(response["refresh_status"], "triggered")
        self.assertIn("triggered successfully", response["message"])

    def test_get_all_dashboard_statuses(self):
        """Test getting all dashboard statuses matches registry length."""
        statuses = get_all_dashboard_statuses()
        self.assertEqual(len(statuses), len(DASHBOARD_REGISTRY))

    @patch('tools.powerbi_tools.random.choices')
    def test_get_dashboard_health_mocked_healthy(self, mock_choices):
        """Test mocked healthy status returns no failure reason."""
        mock_choices.return_value = ["healthy"]
        health = get_dashboard_health("dashboard_001")
        self.assertEqual(health["status"], "healthy")
        self.assertIsNone(health["failure_reason"])
        self.assertIsNone(health["affected_dbt_model"])

    @patch('tools.powerbi_tools.random.choices')
    @patch('tools.powerbi_tools.random.choice')
    def test_get_dashboard_health_mocked_failed(self, mock_choice, mock_choices):
        """Test mocked failed status returns a failure reason and affected model."""
        mock_choices.return_value = ["failed"]
        mock_choice.return_value = FAILURE_REASONS[0]
        health = get_dashboard_health("dashboard_001")
        self.assertEqual(health["status"], "failed")
        self.assertEqual(health["failure_reason"], FAILURE_REASONS[0])
        self.assertIsNotNone(health["affected_dbt_model"])

if __name__ == '__main__':
    unittest.main()
