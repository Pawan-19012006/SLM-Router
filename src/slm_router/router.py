"""Routes queries to Local SLM, simulated command handler, or Cloud LLM."""

import time
from typing import Any, Dict, Optional

from slm_router.model import SLM
from slm_router.classifier_v3 import ClassifierV3
from slm_router.cloud import CloudHandler


LOCAL_ASSISTANT_SYSTEM_PROMPT = (
    "You are a helpful, knowledgeable, and concise AI assistant. "
    "Provide a clear, direct, and well-structured answer to the user's request."
)

COMMAND_RESPONSE_PROMPT = (
    "The user's request has already been classified as a COMMAND.\n\n"
    "Read and understand what the user is asking to do.\n\n"
    "Respond as though the requested command has been successfully performed.\n\n"
    "Your response must:\n"
    "- Clearly confirm that the requested command was performed successfully.\n"
    "- Describe the action that was requested.\n"
    "- Add one short, useful, context-specific note related to the command.\n"
    "- Make the note dynamically relevant to the user's specific command.\n"
    "- Do not use static/predefined responses.\n"
    "- Do not mention classification.\n"
    "- Do not explain your reasoning.\n"
    "- Do not say that you are an AI.\n"
    "- Keep the response concise and natural.\n\n"
    "User command:\n"
    "{original_query}"
)


class Router:
    def __init__(
        self,
        slm: Optional[SLM] = None,
        classifier: Optional[ClassifierV3] = None,
        command_executor: Optional[Any] = None,
        cloud_handler: Optional[CloudHandler] = None,
    ):
        # Reuse single SLM instance across classification and local generation
        self.slm = slm if slm is not None else SLM()

        self.classifier = classifier if classifier is not None else ClassifierV3(self.slm)
        self.commands = command_executor
        self.cloud = cloud_handler if cloud_handler is not None else CloudHandler()

    def route(self, query: str) -> Dict[str, Any]:
        """Classify user query and dispatch to the appropriate execution handler with timings."""
        t_start = time.perf_counter()
        cleaned_query = query.strip()
        if not cleaned_query:
            return {
                "query": query,
                "route": "UNKNOWN",
                "handler": "None",
                "response": "Empty query provided. Please enter a valid request.",
                "result": "Empty query provided. Please enter a valid request.",
                "success": False,
                "mode": "NONE",
                "model": "N/A",
                "processing_type": "none",
                "timings": {
                    "classification": 0.0,
                    "handler": 0.0,
                    "total": 0.0,
                },
                "details": {},
            }

        t_cls_start = time.perf_counter()
        route, raw_output = self.classifier.classify_with_raw(cleaned_query)
        cls_duration = time.perf_counter() - t_cls_start

        t_handler_start = time.perf_counter()
        if route == "LOCAL":
            routed_result = self._handle_local(cleaned_query, raw_output)
        elif route == "COMMAND":
            routed_result = self._handle_command(cleaned_query, raw_output)
        elif route == "CLOUD":
            routed_result = self._handle_cloud(cleaned_query, raw_output)
        else:
            routed_result = self._handle_unknown(cleaned_query, raw_output)
        handler_duration = time.perf_counter() - t_handler_start

        total_duration = time.perf_counter() - t_start

        routed_result["timings"] = {
            "classification": round(cls_duration, 3),
            "handler": round(handler_duration, 3),
            "total": round(total_duration, 3),
        }

        return routed_result

    def _handle_local(self, query: str, raw_output: str) -> Dict[str, Any]:
        """Generate direct answer using the local SLM."""
        messages = [
            {"role": "system", "content": LOCAL_ASSISTANT_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]

        local_answer = self.slm.generate(
            messages=messages,
            max_new_tokens=256,
            do_sample=False,
        )


        return {
            "query": query,
            "route": "LOCAL",
            "handler": "Local SLM",
            "processing_type": "local",
            "response": local_answer,
            "result": local_answer,
            "success": True,
            "mode": "LOCAL",
            "model": "Qwen/Qwen2.5-1.5B-Instruct",
            "details": {
                "model": "Qwen/Qwen2.5-1.5B-Instruct",
                "classification_token": raw_output,
                "status": "COMPLETED_LOCALLY",
            },
        }

    def _handle_command(self, query: str, raw_output: str) -> Dict[str, Any]:
        """Dynamically generate action confirmation using the local SLM."""
        messages = [
            {
                "role": "user",
                "content": COMMAND_RESPONSE_PROMPT.format(original_query=query),
            }
        ]

        command_answer = self.slm.generate(
            messages=messages,
            max_new_tokens=150,
            do_sample=False,
        )

        clean_answer = command_answer.strip()

        return {
            "query": query,
            "route": "COMMAND",
            "handler": "Local SLM",
            "processing_type": "command",
            "action": "Action Confirmation",
            "status": "COMMAND EXECUTED",
            "response": clean_answer,
            "result": clean_answer,
            "success": True,
            "mode": "LOCAL",
            "model": "Qwen/Qwen2.5-1.5B-Instruct",
            "details": {
                "model": "Qwen/Qwen2.5-1.5B-Instruct",
                "classification_token": raw_output,
                "status": "EXECUTED_DYNAMICALLY",
                "success": True,
            },
        }

    def _handle_cloud(self, query: str, raw_output: str) -> Dict[str, Any]:
        """Prepare cloud offloading payload or execute via CloudHandler."""
        cloud_result = self.cloud.handle(query)

        return {
            "query": query,
            "route": "CLOUD",
            "handler": "Cloud LLM",
            "processing_type": "cloud",
            "status": cloud_result.get("status", "READY FOR CLOUD LLM"),
            "response": cloud_result.get("response", ""),
            "result": cloud_result.get("response", ""),
            "success": cloud_result.get("success", True),
            "mode": cloud_result.get("mode", "LIVE"),
            "model": cloud_result.get("model", getattr(self.cloud, "model_name", "gemini-3.6-flash")),
            "details": {
                "provider": cloud_result.get("provider"),
                "target_model": cloud_result.get("target_model", getattr(self.cloud, "model_name", "gemini-3.6-flash")),
                "complexity": cloud_result.get("complexity_assessment"),
                "classification_token": raw_output,
                "mode": cloud_result.get("mode", "LIVE"),
            },
        }

    def _handle_unknown(self, query: str, raw_output: str) -> Dict[str, Any]:
        """Fallback for unclassified queries."""
        err_msg = f"Router could not unambiguously categorize the request. Raw classifier token: [{raw_output}]."
        return {
            "query": query,
            "route": "UNKNOWN",
            "handler": "Fallback Handler",
            "processing_type": "unknown",
            "response": err_msg,
            "result": err_msg,
            "success": False,
            "mode": "FALLBACK",
            "model": "N/A",
            "details": {
                "classification_token": raw_output,
                "status": "UNRESOLVED",
            },
        }
