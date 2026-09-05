import sys
import unittest
from unittest.mock import MagicMock
from pathlib import Path

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.router import Router
from slm_router.commands import CommandExecutor
from slm_router.cloud import CloudHandler


class TestRouterUnit(unittest.TestCase):

    def setUp(self):
        self.mock_slm = MagicMock()
        self.mock_classifier = MagicMock()
        self.command_executor = CommandExecutor()
        self.cloud_handler = CloudHandler()

        self.router = Router(
            slm=self.mock_slm,
            classifier=self.mock_classifier,
            command_executor=self.command_executor,
            cloud_handler=self.cloud_handler
        )

    def test_local_query_reaches_local_handler(self):
        """1. LOCAL query reaches local handler and generates an answer via SLM."""
        query = "Why is the ocean blue?"
        self.mock_classifier.classify_with_raw.return_value = ("LOCAL", "LOCAL")
        self.mock_slm.generate.return_value = "The ocean appears blue due to the absorption and scattering of light."

        result = self.router.route(query)

        self.assertEqual(result["route"], "LOCAL")
        self.assertEqual(result["handler"], "Local SLM")
        self.assertEqual(result["processing_type"], "local")
        self.assertIn("absorption and scattering", result["response"])
        self.mock_slm.generate.assert_called_once()

    def test_command_query_reaches_command_handler(self):
        """2. COMMAND query reaches command handler and does not invoke SLM generation."""
        query = "Turn the garden sprinkler on for 15 minutes."
        self.mock_classifier.classify_with_raw.return_value = ("COMMAND", "COMMAND")

        result = self.router.route(query)

        self.assertEqual(result["route"], "COMMAND")
        self.assertEqual(result["handler"], "Command Executor")
        self.assertEqual(result["processing_type"], "device")
        self.assertEqual(result["action"], "Turn on garden sprinkler")
        self.assertEqual(result["status"], "SIMULATED EXECUTION SUCCESS")
        self.assertIn("Duration: 15 minutes", result["details"]["execution_details"])
        # SLM generation should NOT be called for commands
        self.mock_slm.generate.assert_not_called()

    def test_cloud_query_reaches_cloud_handler(self):
        """3. CLOUD query reaches cloud handler and does not invoke SLM generation."""
        query = "Create a detailed 3000-word research report on AI employment."
        self.mock_classifier.classify_with_raw.return_value = ("CLOUD", "CLOUD")

        result = self.router.route(query)

        self.assertEqual(result["route"], "CLOUD")
        self.assertEqual(result["handler"], "Cloud LLM")
        self.assertEqual(result["processing_type"], "cloud")
        self.assertIn("Cloud LLM routing selected", result["response"])
        # SLM generation should NOT be called for cloud tasks
        self.mock_slm.generate.assert_not_called()

    def test_router_preserves_original_query(self):
        """4. Router preserves original query accurately."""
        query = "   What is the speed of light?   "
        self.mock_classifier.classify_with_raw.return_value = ("LOCAL", "LOCAL")
        self.mock_slm.generate.return_value = "299,792,458 m/s"

        result = self.router.route(query)

        self.assertEqual(result["query"], "What is the speed of light?")

    def test_router_returns_valid_structured_result(self):
        """5. Router returns valid structured result for all paths."""
        self.mock_classifier.classify_with_raw.return_value = ("LOCAL", "LOCAL")
        self.mock_slm.generate.return_value = "Test response"
        res = self.router.route("Test query")

        required_keys = {"query", "route", "handler", "response", "processing_type", "details"}
        self.assertTrue(required_keys.issubset(res.keys()))

    def test_unsupported_command_handled_safely(self):
        """6. Unsupported/unrecognized command is handled safely without error."""
        cmd_exec = CommandExecutor()
        res = cmd_exec.execute("Launch alien spacecraft into orbit.")

        self.assertFalse(res["success"])
        self.assertEqual(res["status"], "SIMULATED REJECTION (UNREGISTERED)")
        self.assertIn("not in demonstration registry", res["response"])

    def test_no_arbitrary_shell_execution_possible(self):
        """7. Verify no dangerous system execution modules or calls are used in commands.py."""
        commands_code = Path(__file__).resolve().parent.parent / "commands.py"
        with open(commands_code, "r", encoding="utf-8") as f:
            content = f.read()

        dangerous_patterns = [
            "import subprocess",
            "from subprocess",
            "os.system",
            "os.popen",
            "shell=True",
            "exec(",
            "eval("
        ]
        for pattern in dangerous_patterns:
            self.assertNotIn(pattern, content, f"Security violation: dangerous pattern '{pattern}' found in commands.py")


if __name__ == "__main__":
    unittest.main()
