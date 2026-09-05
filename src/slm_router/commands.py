"""Safe simulated command executor for SLM Router.

Provides a safe in-memory command registry for demonstration purposes.
DOES NOT execute arbitrary OS actions or system binaries.
"""

import re
from typing import Any, Dict


class CommandExecutor:
    """Safe, sandboxed demonstration command executor."""

    def __init__(self):
        # In-memory simulated device/system states
        self.state: Dict[str, Any] = {
            "light": "OFF",
            "sprinkler": "OFF",
            "music": "PAUSED",
            "browser": "CLOSED",
            "screen": "UNLOCKED",
            "brightness": 50,
            "volume": 50,
        }

    def execute(self, query: str) -> Dict[str, Any]:
        """Parse query against the safe simulated command catalog and update simulated state."""
        q = query.lower().strip()

        # 1. Garden Sprinkler
        if "sprinkler" in q:
            duration_match = re.search(r"(\d+)\s*(minutes|minute|hours|hour|seconds|sec|min)\b", q)
            duration_str = duration_match.group(0) if duration_match else None
            is_turn_off = any(w in q for w in ["off", "stop", "disable", "shut"])
            target_state = "OFF" if is_turn_off else "ON"
            self.state["sprinkler"] = target_state

            details = f"Duration: {duration_str}" if duration_str else "Duration: Standard cycle"
            action_desc = f"Turn {'off' if is_turn_off else 'on'} garden sprinkler"
            return {
                "success": True,
                "action": action_desc,
                "target": "Garden Sprinkler",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": target_state,
                "details": details,
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: {target_state}\n{details}"
            }

        # 2. Lighting
        if "light" in q or "lamp" in q:
            is_turn_off = any(w in q for w in ["off", "dim down", "extinguish"])
            target_state = "OFF" if is_turn_off else "ON"
            self.state["light"] = target_state
            action_desc = f"Turn {'off' if is_turn_off else 'on'} light"
            return {
                "success": True,
                "action": action_desc,
                "target": "Lighting System",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": target_state,
                "details": "Location: Default Zone",
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: {target_state}"
            }

        # 3. Music / Audio Playback
        if any(w in q for w in ["music", "song", "track", "sonata", "play", "pause", "mute", "unmute"]):
            if "pause" in q or "stop" in q:
                self.state["music"] = "PAUSED"
                action_desc = "Pause audio playback"
            elif "mute" in q and "unmute" not in q:
                self.state["music"] = "MUTED"
                action_desc = "Mute audio output"
            elif "unmute" in q:
                self.state["music"] = "ACTIVE"
                action_desc = "Unmute audio output"
            else:
                self.state["music"] = "PLAYING"
                action_desc = "Play audio track"

            return {
                "success": True,
                "action": action_desc,
                "target": "Audio Player",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": self.state["music"],
                "details": f"Track/Command: {query.strip()}",
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: {self.state['music']}"
            }

        # 4. Web Browser
        if "browser" in q or "chrome" in q or "safari" in q:
            is_close = any(w in q for w in ["close", "quit", "exit", "shut"])
            target_state = "CLOSED" if is_close else "OPENED"
            self.state["browser"] = target_state
            action_desc = f"{'Close' if is_close else 'Launch'} web browser"
            return {
                "success": True,
                "action": action_desc,
                "target": "Web Browser Application",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": target_state,
                "details": "Environment: Local Desktop",
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: {target_state}"
            }

        # 5. Screen Lock / Brightness / Display
        if "lock" in q and "screen" in q:
            self.state["screen"] = "LOCKED"
            action_desc = "Lock system workstation"
            return {
                "success": True,
                "action": action_desc,
                "target": "OS Session Lock",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": "LOCKED",
                "details": "Security: Workstation locked immediately",
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: LOCKED"
            }

        if "brightness" in q:
            pct_match = re.search(r"(\d+)\s*%", q)
            pct = int(pct_match.group(1)) if pct_match else 70
            self.state["brightness"] = pct
            action_desc = f"Set display brightness to {pct}%"
            return {
                "success": True,
                "action": action_desc,
                "target": "Display Hardware",
                "status": "SIMULATED EXECUTION SUCCESS",
                "state": f"{pct}%",
                "details": f"Brightness Level: {pct}%",
                "response": f"Command executed successfully.\nAction: {action_desc}\nStatus: {pct}%"
            }

        # 6. Safe generic fallback for unregistered / unsupported commands
        return {
            "success": False,
            "action": "Unregistered Device/System Action",
            "target": "Unknown / External Device",
            "status": "SIMULATED REJECTION (UNREGISTERED)",
            "state": "NO_ACTION",
            "details": "Action recognized as a command intent, but safe sandbox policy permits only registered simulated actions.",
            "response": "Command recognized by router.\nStatus: Rejected by safe execution policy (action not in demonstration registry)."
        }
