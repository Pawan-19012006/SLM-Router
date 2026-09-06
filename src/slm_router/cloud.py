"""Cloud LLM routing handler for SLM Router.

Integrates with external Cloud LLM endpoints via the official Google Gemini
Python SDK (`google-genai`), with resilient error handling and local mock fallback.
"""

import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class CloudHandler:
    """Handles dispatching heavy or complex requests to Cloud LLM providers

    using the Google Gemini Python SDK, or safe mock fallback.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        mode: Optional[str] = None,
        api_key: Optional[str] = None,
        provider: str = "Google Gemini",
    ):
        # Reload env in case it changed at runtime
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY", "") if api_key is None else api_key
        self.model_name = model_name or os.getenv("CLOUD_MODEL", "gemini-2.5-flash")
        self.provider = provider

        # Resolve mode: live vs mock
        env_mode = (mode or os.getenv("CLOUD_MODE", "")).strip().lower()
        if not self.api_key or not self.api_key.strip():
            # If GEMINI_API_KEY is missing, default to mock mode
            self.mode = "mock"
        elif env_mode == "mock":
            self.mode = "mock"
        else:
            self.mode = "live"

    @property
    def is_configured(self) -> bool:
        """Check if a non-empty API key is present."""
        return bool(self.api_key and self.api_key.strip())

    def get_api_status(self) -> str:
        """Return human-readable API status for UI display without exposing keys."""
        if not self.is_configured:
            return "Not Configured"
        if self.mode == "mock":
            return "Mock Mode"
        return "Connected"

    def _sanitize_error_message(self, err: Exception) -> str:
        """Strip any accidental API key leakage from error text."""
        msg = getattr(err, "message", None) or str(err)
        if self.api_key and self.api_key in msg:
            msg = msg.replace(self.api_key, "[REDACTED_API_KEY]")
        return msg

    def handle(self, query: str) -> Dict[str, Any]:
        """Dispatch query to Cloud LLM or local mock fallback based on configuration."""
        if self.mode == "mock":
            return self._handle_mock(query)
        return self._handle_live(query)

    def _handle_mock(self, query: str) -> Dict[str, Any]:
        """Provide simulated cloud response without network/API calls."""
        word_count = len(query.strip().split())
        estimated_complexity = (
            "High (Production Scale / Deep Research)"
            if word_count > 10
            else "Moderate / High"
        )

        mock_response = (
            "Cloud LLM routing selected.\n"
            "This request has been identified as exceeding local SLM resource budget.\n"
            f"Prepared payload for target endpoint: {self.model_name} via {self.provider}.\n"
            "(Mock mode active — no external API calls made)."
        )

        return {
            "handler": "Cloud LLM",
            "mode": "MOCK",
            "model": self.model_name,
            "response": mock_response,
            "success": True,
            "provider": f"Cloud LLM ({self.provider} Provider)",
            "target_model": self.model_name,
            "status": "READY FOR CLOUD LLM (MOCK MODE)",
            "complexity_assessment": estimated_complexity,
        }

    def _handle_live(self, query: str) -> Dict[str, Any]:
        """Dispatch query via official Google Gemini Python SDK."""
        if not self.is_configured:
            return {
                "handler": "Cloud LLM",
                "mode": "ERROR",
                "model": self.model_name,
                "success": False,
                "response": "Gemini API key missing. Please set GEMINI_API_KEY in .env or switch CLOUD_MODE to mock.",
            }

        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)

            response = client.models.generate_content(
                model=self.model_name,
                contents=query,
            )

            # Extract generated text from response
            output_text = getattr(response, "text", None)
            if output_text is None:
                output_text = str(response)

            return {
                "handler": "Cloud LLM",
                "mode": "LIVE",
                "model": self.model_name,
                "response": output_text,
                "success": True,
                "provider": f"Cloud LLM ({self.provider} Provider)",
                "target_model": self.model_name,
                "status": "LIVE INFERENCE SUCCESS",
            }

        except Exception as e:
            from google.genai import errors

            err_msg = self._sanitize_error_message(e)

            if isinstance(e, errors.ClientError):
                code = getattr(e, "code", None)
                if code in (400, 401, 403) or "API key not valid" in err_msg:
                    return {
                        "handler": "Cloud LLM",
                        "mode": "ERROR",
                        "model": self.model_name,
                        "success": False,
                        "response": f"Authentication Error: Invalid or unauthorized Gemini API key. ({err_msg})",
                    }
                elif code == 429 or "RESOURCE_EXHAUSTED" in err_msg:
                    return {
                        "handler": "Cloud LLM",
                        "mode": "ERROR",
                        "model": self.model_name,
                        "success": False,
                        "response": f"Rate Limit / Quota Exceeded: Your Gemini API quota has been exceeded. ({err_msg})",
                    }
                else:
                    return {
                        "handler": "Cloud LLM",
                        "mode": "ERROR",
                        "model": self.model_name,
                        "success": False,
                        "response": f"Gemini Client Error: {err_msg}",
                    }
            elif isinstance(e, errors.ServerError):
                return {
                    "handler": "Cloud LLM",
                    "mode": "ERROR",
                    "model": self.model_name,
                    "success": False,
                    "response": f"Gemini Server Error ({getattr(e, 'code', '5xx')}): {err_msg}",
                }
            elif isinstance(e, errors.APIError):
                return {
                    "handler": "Cloud LLM",
                    "mode": "ERROR",
                    "model": self.model_name,
                    "success": False,
                    "response": f"Gemini API Error: {err_msg}",
                }
            else:
                return {
                    "handler": "Cloud LLM",
                    "mode": "ERROR",
                    "model": self.model_name,
                    "success": False,
                    "response": f"Unexpected Cloud Handler Error: {err_msg}",
                }
