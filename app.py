import sys
import os
from pathlib import Path
from typing import Any, Dict, Optional
import streamlit as st

# Ensure src is in sys.path
repo_root = Path(__file__).resolve().parent
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.router import Router
from slm_router.cloud import CloudHandler


@st.cache_resource
def get_router() -> Router:
    """Load SLM and Router once in memory."""
    return Router()


def inject_custom_css():
    """Inject modern, dark, distraction-free product styling."""
    st.markdown("""
        <style>
        /* Modern font and dark palette */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Clean app header */
        .app-header {
            margin-bottom: 2rem;
            padding-bottom: 1.2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .app-title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.3rem;
        }

        .app-subtitle {
            font-size: 0.95rem;
            color: #8b949e;
            margin-bottom: 0.8rem;
        }

        .status-indicators {
            display: flex;
            gap: 14px;
            align-items: center;
            font-size: 0.78rem;
            color: #8b949e;
            font-family: 'JetBrains Mono', monospace;
        }

        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            margin-right: 5px;
        }

        .status-dot.green { background-color: #22c55e; box-shadow: 0 0 6px #22c55e; }
        .status-dot.blue { background-color: #38bdf8; box-shadow: 0 0 6px #38bdf8; }
        .status-dot.purple { background-color: #a855f7; box-shadow: 0 0 6px #a855f7; }

        /* Routing Decision Card */
        .route-card {
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.02);
        }

        .route-card.local {
            border-left: 5px solid #22c55e;
            background: rgba(34, 197, 94, 0.04);
        }

        .route-card.command {
            border-left: 5px solid #f59e0b;
            background: rgba(245, 158, 11, 0.04);
        }

        .route-card.cloud {
            border-left: 5px solid #8b5cf6;
            background: rgba(139, 92, 246, 0.04);
        }

        .route-card-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .route-badge {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.01em;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .route-badge.local { color: #4ade80; }
        .route-badge.command { color: #fbbf24; }
        .route-badge.cloud { color: #a78bfa; }

        .route-status {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            letter-spacing: 0.05em;
        }

        .route-status.success {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
        }

        .route-status.error {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
        }

        .route-explanation {
            font-size: 0.92rem;
            color: #94a3b8;
            margin-bottom: 0.9rem;
        }

        .route-meta-row {
            display: flex;
            gap: 2rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 0.82rem;
        }

        .route-meta-item {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .route-meta-label {
            color: #64748b;
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .route-meta-val {
            color: #e2e8f0;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(cloud_status: str):
    """Render clean, minimalist app header."""
    st.markdown(f"""
        <div class='app-header'>
            <div class='app-title'>⚡ SLM ROUTER</div>
            <div class='app-subtitle'>Local AI Request Classification & Intelligent Dispatch</div>
            <div class='status-indicators'>
                <span><span class='status-dot green'></span>Local SLM Online</span>
                <span><span class='status-dot blue'></span>Router Ready</span>
                <span><span class='status-dot purple'></span>Cloud API: {cloud_status}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_prompt_section(router: Router):
    """Render the central prompt input section with sample pills."""
    st.markdown("### What would you like to do?")

    # Compact sample pills
    p1, p2, p3 = st.columns(3)
    if p1.button("🌱 Turn on sprinkler", use_container_width=True):
        st.session_state.query_input = "Turn the garden sprinkler on for 15 minutes."
        st.rerun()
    if p2.button("🌊 Explain ocean tides", use_container_width=True):
        st.session_state.query_input = "What causes tides in the ocean?"
        st.rerun()
    if p3.button("📊 Semiconductor analysis", use_container_width=True):
        st.session_state.query_input = "Give me a detailed analysis of why semiconductor manufacturing is difficult."
        st.rerun()

    query = st.text_area(
        label="Prompt",
        value=st.session_state.get("query_input", ""),
        height=110,
        placeholder="Enter any request... (e.g. 'What is photosynthesis?', 'Turn on the sprinkler', 'Analyze market trends')",
        label_visibility="collapsed",
        key="prompt_text_area",
    )

    st.session_state.query_input = query

    if st.button("⚡ Route Request", type="primary", use_container_width=True):
        cleaned = query.strip()
        if not cleaned:
            st.warning("Please enter a request before routing.")
        else:
            with st.spinner("Analyzing and routing request..."):
                result = router.route(cleaned)
                st.session_state.result = result
            st.rerun()


def render_routing_decision(result: Dict[str, Any]):
    """Render ONE clean routing decision card."""
    route = result.get("route", "UNKNOWN").upper()
    success = result.get("success", True)
    status_label = "SUCCESS" if success else "ERROR"
    status_class = "success" if success else "error"

    if route == "LOCAL":
        route_class = "local"
        icon = "◉"
        explanation = "Handled by the on-device SLM"
        handler_name = "Qwen2.5-1.5B-Instruct"
    elif route == "COMMAND":
        route_class = "command"
        icon = "⚙"
        explanation = "Safe device/action request detected"
        handler_name = "Safe Action Engine"
    elif route == "CLOUD":
        route_class = "cloud"
        icon = "☁"
        explanation = "Complex workload detected"
        raw_model = result.get("model", "Gemini 3.6 Flash")
        if "gemini" in raw_model.lower():
            parts = raw_model.split("-")
            if len(parts) >= 3:
                handler_name = f"Gemini {' '.join(p.capitalize() for p in parts[1:])}"
            else:
                handler_name = raw_model
        else:
            handler_name = raw_model
    else:
        route_class = "local"
        icon = "●"
        explanation = "Standard routing dispatch"
        handler_name = result.get("handler", "Router Engine")

    st.markdown(f"""
        <div class='route-card {route_class}'>
            <div class='route-card-top'>
                <div class='route-badge {route_class}'>
                    <span>{icon}</span> {route} ROUTE
                </div>
                <div class='route-status {status_class}'>{status_label}</div>
            </div>
            <div class='route-explanation'>{explanation}</div>
            <div class='route-meta-row'>
                <div class='route-meta-item'>
                    <span class='route-meta-label'>Selected Handler / Model</span>
                    <span class='route-meta-val'>{handler_name}</span>
                </div>
                <div class='route-meta-item'>
                    <span class='route-meta-label'>Execution Status</span>
                    <span class='route-meta-val'>{status_label}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_answer_section(result: Dict[str, Any]):
    """Render prominent, clean Answer section."""
    route = result.get("route", "UNKNOWN").upper()
    success = result.get("success", True)
    response_text = result.get("response", "")

    st.markdown("### Answer")

    if not success:
        st.error(response_text)
        return

    if route == "COMMAND":
        action = result.get("action", "Action Executed")
        details = result.get("details", {})
        exec_details = details.get("execution_details", "")

        with st.container(border=True):
            st.markdown(f"**Action:** `{action}`")
            if exec_details:
                st.caption(f"Details: {exec_details}")
            st.markdown(response_text)
    else:
        # LOCAL or CLOUD output
        with st.container(border=True):
            st.markdown(response_text)


def main():
    st.set_page_config(
        page_title="SLM Router",
        page_icon="⚡",
        layout="centered",
    )

    inject_custom_css()
    router = get_router()

    # Determine Cloud API status safely
    cloud_status = router.cloud.get_api_status()

    # State initialization
    if "result" not in st.session_state:
        st.session_state.result = None
    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    # 1. Header
    render_header(cloud_status)

    # 2. Prompt Section
    render_prompt_section(router)

    # 3. Routing Decision & Answer
    if st.session_state.result:
        st.divider()
        render_routing_decision(st.session_state.result)
        render_answer_section(st.session_state.result)


if __name__ == "__main__":
    main()
