import unittest
from veil.common.service_health_enums import ComponentDegradationLevel
from veil.common.service_state import ServiceState


class TestServiceState(unittest.TestCase):
    """Unit tests for ServiceState."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_default_initialization(self) -> None:
        """Test default ServiceState initialization."""

        state = ServiceState()

        self.assertEqual(
            state.service_health,
            ComponentDegradationLevel.NONE
        )

        self.assertEqual(state.service_health_state_str, "")
        self.assertTrue(state.database_enabled)

        self.assertEqual(
            state.database_health,
            ComponentDegradationLevel.NONE
        )

        self.assertEqual(state.database_health_state_str, "")
        self.assertEqual(state.version, "")
        self.assertFalse(state.in_maintenance)

        self.assertIsInstance(state.startup_time, int)

    # ------------------------------------------------------------------
    # mark_database_failed
    # ------------------------------------------------------------------

    def test_mark_database_failed(self) -> None:
        """Test marking the database as failed."""

        state = ServiceState()

        state.mark_database_failed("SQL corruption")

        self.assertEqual(
            state.database_health,
            ComponentDegradationLevel.FULLY_DEGRADED
        )

        self.assertEqual(
            state.database_health_state_str,
            "SQL corruption"
        )

        self.assertTrue(state.in_maintenance)

        self.assertEqual(
            state.service_health,
            ComponentDegradationLevel.FULLY_DEGRADED
        )

        self.assertEqual(
            state.service_health_state_str,
            "Database failure: SQL corruption"
        )

    def test_mark_database_failed_when_database_disabled(self) -> None:
        """Test database failure handling when DB monitoring is disabled."""

        state = ServiceState(database_enabled=False)

        state.mark_database_failed("SQL corruption")

        self.assertEqual(
            state.database_health,
            ComponentDegradationLevel.NONE
        )

        self.assertEqual(state.database_health_state_str, "")
        self.assertFalse(state.in_maintenance)

    def test_mark_database_failed_default_reason(self) -> None:
        """Test database failure with default reason."""

        state = ServiceState()

        state.mark_database_failed()

        self.assertEqual(
            state.database_health_state_str,
            "Fatal SQL failure"
        )

        self.assertEqual(
            state.service_health_state_str,
            "Database failure: Fatal SQL failure"
        )

    # ------------------------------------------------------------------
    # mark_service_failed
    # ------------------------------------------------------------------

    def test_mark_service_failed(self) -> None:
        """Test marking the service as failed."""

        state = ServiceState()

        state.mark_service_failed("Fatal service error")

        self.assertEqual(
            state.service_health,
            ComponentDegradationLevel.FULLY_DEGRADED
        )

        self.assertEqual(
            state.service_health_state_str,
            "Fatal service error"
        )

        self.assertTrue(state.in_maintenance)

    # ------------------------------------------------------------------
    # enter_maintenance
    # ------------------------------------------------------------------

    def test_enter_maintenance(self) -> None:
        """Test entering maintenance mode."""

        state = ServiceState()

        state.enter_maintenance("Maintenance scheduled")

        self.assertTrue(state.in_maintenance)

        self.assertEqual(
            state.service_health,
            ComponentDegradationLevel.FULLY_DEGRADED
        )

        self.assertEqual(
            state.service_health_state_str,
            "Maintenance scheduled"
        )

    def test_enter_maintenance_default_reason(self) -> None:
        """Test entering maintenance mode with default reason."""

        state = ServiceState()

        state.enter_maintenance()

        self.assertEqual(
            state.service_health_state_str,
            "Entering maintenance mode"
        )

    # ------------------------------------------------------------------
    # exit_maintenance
    # ------------------------------------------------------------------

    def test_exit_maintenance(self) -> None:
        """Test exiting maintenance mode."""

        state = ServiceState()

        state.enter_maintenance("Failure")
        state.exit_maintenance()

        self.assertFalse(state.in_maintenance)

        self.assertEqual(
            state.service_health,
            ComponentDegradationLevel.NONE
        )

        self.assertEqual(
            state.service_health_state_str,
            "Normal operation"
        )

    # ------------------------------------------------------------------
    # is_operational
    # ------------------------------------------------------------------

    def test_is_operational_when_operational(self) -> None:
        """Test operational state when healthy."""

        state = ServiceState()

        self.assertTrue(state.is_operational())

    def test_is_operational_when_in_maintenance(self) -> None:
        """Test operational state when in maintenance mode."""

        state = ServiceState()

        state.enter_maintenance()

        self.assertFalse(state.is_operational())

    # ------------------------------------------------------------------
    # to_dict
    # ------------------------------------------------------------------

    def test_to_dict_with_database_enabled(self) -> None:
        """Test dictionary serialization with database enabled."""

        state = ServiceState(
            service_health=ComponentDegradationLevel.NONE,
            service_health_state_str="Healthy",
            database_enabled=True,
            database_health=ComponentDegradationLevel.NONE,
            database_health_state_str="Healthy DB",
            version="1.0.0",
            startup_time=123456789,
            in_maintenance=False
        )

        result = state.to_dict()

        expected = {
            "service_health": "NONE",
            "service_health_state_str": "Healthy",
            "database_health": "NONE",
            "database_health_state_str": "Healthy DB",
            "version": "1.0.0",
            "startup_time": 123456789,
            "in_maintenance": False
        }

        self.assertEqual(result, expected)

    def test_to_dict_with_database_disabled(self) -> None:
        """Test dictionary serialization with database disabled."""

        state = ServiceState(
            database_enabled=False
        )

        result = state.to_dict()

        self.assertNotIn("database_health", result)
        self.assertNotIn("database_health_state_str", result)

        self.assertIn("service_health", result)
        self.assertIn("version", result)
        self.assertIn("startup_time", result)
        self.assertIn("in_maintenance", result)
