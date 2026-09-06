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
def get_router():
    """Load SLM and Router once in memory."""
    return Router()


def inject_custom_css():
    """Inject modern, high-tech dashboard styling."""
    st.markdown("""
        <style>
        /* Base typography and background hints */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .mono {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Top Header */
        .dash-title {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 0.15rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .dash-subtitle {
            font-size: 0.98rem;
            color: #64748b;
            margin-bottom: 1.2rem;
            font-weight: 400;
        }

        /* Status Pills Header */
        .status-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 1.6rem;
            padding: 10px 14px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            align-items: center;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.5px;
        }

        .status-pill.online {
            background: #dcfce7;
            color: #15803d;
            border: 1px solid #bbf7d0;
        }

        .status-pill.ready {
            background: #e0f2fe;
            color: #0369a1;
            border: 1px solid #bae6fd;
        }

        .status-pill.cloud-live {
            background: #ede9fe;
            color: #6d28d9;
            border: 1px solid #ddd6fe;
        }

        .status-pill.cloud-mock {
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #cbd5e1;
        }

        /* Pipeline visualization */
        .pipeline-container {
            background: #0f172a;
            color: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 1.8rem;
            border: 1px solid #1e293b;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        .pipeline-header {
            font-size: 0.78rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #94a3b8;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 14px;
        }

        .pipeline-flow {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .pipeline-node {
            background: #1e293b;
            border: 1px solid #334155;
            padding: 8px 18px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 600;
            color: #e2e8f0;
            text-align: center;
        }

        .pipeline-router-box {
            background: #1e293b;
            border: 2px solid #38bdf8;
            padding: 10px 22px;
            border-radius: 10px;
            text-align: center;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
        }

        .pipeline-branches {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            width: 100%;
        }

        .branch-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            transition: all 0.2s ease;
        }

        .branch-card.active-local {
            border: 2px solid #22c55e;
            background: #14532d25;
            box-shadow: 0 0 18px rgba(34, 197, 94, 0.35);
        }

        .branch-card.active-command {
            border: 2px solid #f97316;
            background: #7c2d1225;
            box-shadow: 0 0 18px rgba(249, 115, 22, 0.35);
        }

        .branch-card.active-cloud {
            border: 2px solid #a855f7;
            background: #581c8725;
            box-shadow: 0 0 18px rgba(168, 85, 247, 0.35);
        }

        .branch-label {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }

        .branch-sub {
            font-size: 0.72rem;
            color: #94a3b8;
        }

        .active-badge {
            display: inline-block;
            margin-top: 6px;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            font-family: 'JetBrains Mono', monospace;
        }

        /* Decision card */
        .decision-card {
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 1.4rem;
            border: 1px solid #e2e8f0;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .decision-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .decision-route-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.3px;
        }

        .decision-intent {
            color: #64748b;
            font-size: 0.9rem;
            margin-bottom: 14px;
        }

        .decision-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            padding-top: 10px;
            border-top: 1px solid #f1f5f9;
        }

        .decision-cell-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #94a3b8;
            font-family: 'JetBrains Mono', monospace;
        }

        .decision-cell-val {
            font-size: 0.88rem;
            font-weight: 700;
            color: #1e293b;
            margin-top: 2px;
        }

        /* Prominent Result Boxes */
        .result-box {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 1.5rem;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }

        .result-box-title {
            font-size: 0.95rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .result-content {
            font-size: 0.96rem;
            line-height: 1.65;
            color: #1e293b;
        }

        /* Telemetry card */
        .telemetry-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            font-family: 'JetBrains Mono', monospace;
        }

        .telemetry-table td {
            padding: 6px 8px;
            border-bottom: 1px solid #f1f5f9;
        }

        .telemetry-table td.label {
            color: #64748b;
            width: 45%;
        }

        .telemetry-table td.val {
            font-weight: 600;
            color: #0f172a;
        }

        .benchmark-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-top: 10px;
        }

        .benchmark-metric {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 10px;
            text-align: center;
        }

        .benchmark-metric-val {
            font-size: 1.15rem;
            font-weight: 800;
            color: #0f172a;
            font-family: 'JetBrains Mono', monospace;
        }

        .benchmark-metric-lbl {
            font-size: 0.68rem;
            color: #64748b;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(cloud_status: str):
    """Render the dashboard header and live connectivity pills."""
    st.markdown("""
        <div class='dash-title'>⚡ SLM ROUTER</div>
        <div class='dash-subtitle'>Local AI Request Classification & Intelligent Dispatch</div>
    """, unsafe_allow_html=True)

    cloud_pill_class = "cloud-live" if "Connected" in cloud_status else "cloud-mock"
    st.markdown(f"""
        <div class='status-bar'>
            <span class='status-pill online'>● LOCAL MODEL ONLINE</span>
            <span class='status-pill ready'>● ROUTER READY</span>
            <span class='status-pill {cloud_pill_class}'>● CLOUD API: {cloud_status.upper()}</span>
        </div>
    """, unsafe_allow_html=True)


def render_pipeline(active_route: Optional[str] = None):
    """Render high-tech visual pipeline highlighting the active branch."""
    is_local = (active_route == "LOCAL")
    is_cmd = (active_route == "COMMAND")
    is_cloud = (active_route == "CLOUD")

    local_class = "active-local" if is_local else ""
    cmd_class = "active-command" if is_cmd else ""
    cloud_class = "active-cloud" if is_cloud else ""

    local_badge = "<div class='active-badge' style='background:#22c55e; color:#000;'>ACTIVE</div>" if is_local else ""
    cmd_badge = "<div class='active-badge' style='background:#f97316; color:#000;'>ACTIVE</div>" if is_cmd else ""
    cloud_badge = "<div class='active-badge' style='background:#a855f7; color:#fff;'>ACTIVE</div>" if is_cloud else ""

    st.markdown(f"""
        <div class='pipeline-container'>
            <div class='pipeline-header'>⚡ LIVE ROUTING PIPELINE</div>
            <div class='pipeline-flow'>
                <div class='pipeline-node'>USER QUERY</div>
                <div style='color:#64748b; font-size:1.1rem; line-height:1;'>↓</div>
                <div class='pipeline-router-box'>
                    QWEN2.5-1.5B ROUTER
                </div>
                <div style='color:#64748b; font-size:1.1rem; line-height:1;'>↓</div>
                <div class='pipeline-branches'>
                    <div class='branch-card {local_class}'>
                        <div class='branch-label' style='color: {"#22c55e" if is_local else "#94a3b8"};'>◉ LOCAL</div>
                        <div class='branch-sub'>On-Device SLM</div>
                        {local_badge}
                    </div>
                    <div class='branch-card {cmd_class}'>
                        <div class='branch-label' style='color: {"#f97316" if is_cmd else "#94a3b8"};'>⚙ COMMAND</div>
                        <div class='branch-sub'>Action Engine</div>
                        {cmd_badge}
                    </div>
                    <div class='branch-card {cloud_class}'>
                        <div class='branch-label' style='color: {"#a855f7" if is_cloud else "#94a3b8"};'>☁ CLOUD</div>
                        <div class='branch-sub'>Cloud LLM</div>
                        {cloud_badge}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_query_input(router: Router):
    """Render the main input area with example pills and dispatch button."""
    st.markdown("### What would you like to do?")

    # Example query quick pills
    st.caption("Try an example:")
    col_e1, col_e2, col_e3 = st.columns(3)

    if col_e1.button("🌱 Turn on sprinkler", use_container_width=True):
        st.session_state.query_text = "Turn the garden sprinkler on for 15 minutes."
        st.rerun()

    if col_e2.button("🌊 Explain ocean tides", use_container_width=True):
        st.session_state.query_text = "What causes tides in the ocean?"
        st.rerun()

    if col_e3.button("📊 Market analysis", use_container_width=True):
        st.session_state.query_text = "Write a detailed 1000-word analysis of the impact of AI on the global semiconductor industry."
        st.rerun()

    query = st.text_area(
        "Enter your request:",
        value=st.session_state.get("query_text", ""),
        height=100,
        placeholder="Enter request... (e.g., 'Turn on the lights', 'What is photosynthesis?', 'Plan a 7-day trip to Japan')",
        label_visibility="collapsed",
        key="main_query_field"
    )

    # Sync text area with session state
    st.session_state.query_text = query

    route_btn = st.button("⚡ ROUTE REQUEST", type="primary", use_container_width=True)

    if route_btn:
        cleaned = query.strip()
        if not cleaned:
            st.warning("Please enter a query before routing.")
        else:
            with st.status("Analyzing request & executing routing...", expanded=True) as status:
                st.write("Running Qwen2.5-1.5B classifier...")
                result = router.route(cleaned)
                st.write(f"Routed to **{result.get('route')}** handler.")
                st.session_state.result = result
                status.update(label="Request routed successfully!", state="complete", expanded=False)
            st.rerun()


def render_route_card(result: Dict[str, Any]):
    """Render large dynamic decision card after routing."""
    route = result.get("route", "UNKNOWN")
    handler = result.get("handler", "None")
    model = result.get("model", "N/A")
    mode = result.get("mode", "UNKNOWN")

    if route == "LOCAL":
        badge_icon = "◉"
        title = "LOCAL ROUTE"
        intent = "Lightweight request suitable for on-device inference"
        border_color = "#22c55e"
        bg_color = "#f0fdf4"
        status_label = "● LOCAL"
    elif route == "COMMAND":
        badge_icon = "⚙"
        title = "COMMAND ROUTE"
        intent = "External action detected"
        border_color = "#f97316"
        bg_color = "#fff7ed"
        status_label = "● EXECUTED"
    elif route == "CLOUD":
        badge_icon = "☁"
        title = "CLOUD ROUTE"
        intent = "Complex workload detected"
        border_color = "#a855f7"
        bg_color = "#faf5ff"
        status_label = f"● {mode.upper()}"
    else:
        badge_icon = "⚠️"
        title = "UNKNOWN ROUTE"
        intent = "Unrecognized request intent"
        border_color = "#64748b"
        bg_color = "#f8fafc"
        status_label = "● UNRESOLVED"

    st.markdown(f"""
        <div class='decision-card' style='border-left: 6px solid {border_color}; background: {bg_color};'>
            <div class='decision-header'>
                <div class='decision-route-title' style='color: {border_color};'>
                    {badge_icon} {title}
                </div>
                <div class='mono' style='font-size: 0.8rem; font-weight:700; color: {border_color};'>
                    {status_label}
                </div>
            </div>
            <div class='decision-intent'>{intent}</div>
            <div class='decision-grid'>
                <div>
                    <div class='decision-cell-label'>Handler</div>
                    <div class='decision-cell-val'>{handler}</div>
                </div>
                <div>
                    <div class='decision-cell-label'>Model</div>
                    <div class='decision-cell-val'>{model}</div>
                </div>
                <div>
                    <div class='decision-cell-label'>Status</div>
                    <div class='decision-cell-val'>{status_label}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_result(result: Dict[str, Any]):
    """Render prominent result area matching route specifications."""
    route = result.get("route", "UNKNOWN")
    raw_response = result.get("response", "")

    if route == "LOCAL":
        st.markdown("""
            <div class='result-box' style='border-top: 4px solid #22c55e;'>
                <div class='result-box-title' style='color: #15803d;'>
                    ◉ LOCAL SLM RESPONSE
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(raw_response)

    elif route == "COMMAND":
        details = result.get("details", {})
        action_name = result.get("action", "Unknown Action")
        exec_details = details.get("execution_details", "None")
        status_text = "✓ Simulated Successfully" if result.get("success") else "✗ Execution Rejected"

        st.markdown(f"""
            <div class='result-box' style='border-top: 4px solid #f97316;'>
                <div class='result-box-title' style='color: #c2410c;'>
                    ⚙ COMMAND EXECUTED
                </div>
                <div style='margin-bottom: 12px;'>
                    <table class='telemetry-table'>
                        <tr><td class='label'>Action</td><td class='val'>{action_name}</td></tr>
                        <tr><td class='label'>Details / Duration</td><td class='val'>{exec_details}</td></tr>
                        <tr><td class='label'>Status</td><td class='val' style='color: {"#16a34a" if result.get("success") else "#dc2626"};'>{status_text}</td></tr>
                    </table>
                </div>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("Command Output Log", expanded=True):
            st.code(raw_response, language="text")

    elif route == "CLOUD":
        model_name = result.get("model", "Cloud Model")
        mode = result.get("mode", "LIVE")
        is_error = (mode == "ERROR" or not result.get("success", True))
        border_col = "#dc2626" if is_error else "#a855f7"
        title_col = "#b91c1c" if is_error else "#7e22ce"

        st.markdown(f"""
            <div class='result-box' style='border-top: 4px solid {border_col};'>
                <div class='result-box-title' style='color: {title_col};'>
                    ☁ CLOUD LLM {'ERROR' if is_error else 'RESPONSE'}
                </div>
                <div style='margin-bottom: 8px; font-size: 0.78rem; color: #64748b; font-family: monospace;'>
                    MODEL: <b>{model_name}</b> | MODE: <b>{mode}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if is_error:
            st.error(raw_response)
        else:
            st.markdown(raw_response)

    else:
        st.error(raw_response)


def render_telemetry(result: Dict[str, Any]):
    """Render technical information panel with real measured timings."""
    timings = result.get("timings", {})
    cls_time = timings.get("classification", 0.0)
    handler_time = timings.get("handler", 0.0)
    total_time = timings.get("total", 0.0)

    query_len = len(result.get("query", ""))
    success_str = "SUCCESS" if result.get("success", True) else "ERROR"
    status_col = "#16a34a" if result.get("success", True) else "#dc2626"

    with st.container(border=True):
        st.markdown("<div class='mono' style='font-size:0.8rem; font-weight:700; color:#475569; margin-bottom:8px;'>ROUTING TELEMETRY</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <table class='telemetry-table'>
                <tr><td class='label'>Classification</td><td class='val'>{result.get('route', 'N/A')}</td></tr>
                <tr><td class='label'>Handler</td><td class='val'>{result.get('handler', 'N/A')}</td></tr>
                <tr><td class='label'>Model</td><td class='val'>{result.get('model', 'N/A')}</td></tr>
                <tr><td class='label'>Execution Mode</td><td class='val'>{result.get('mode', 'N/A')}</td></tr>
                <tr><td class='label'>Query Length</td><td class='val'>{query_len} chars</td></tr>
                <tr><td class='label'>Response Status</td><td class='val' style='color:{status_col};'>{success_str}</td></tr>
                <tr><td class='label'>Routing Time</td><td class='val'>{cls_time:.3f}s</td></tr>
                <tr><td class='label'>Response Time</td><td class='val'>{handler_time:.3f}s</td></tr>
                <tr><td class='label'>Total Time</td><td class='val'>{total_time:.3f}s</td></tr>
            </table>
        """, unsafe_allow_html=True)


def render_benchmark():
    """Render compact benchmark health cards and validation badge."""
    with st.container(border=True):
        st.markdown("""
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='mono' style='font-size:0.8rem; font-weight:700; color:#475569;'>ROUTER BENCHMARK</div>
                <div class='mono' style='font-size:0.68rem; background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px; font-weight:700;'>
                    V3 CLASSIFIER ✓ VALIDATED
                </div>
            </div>
            <div class='benchmark-grid'>
                <div class='benchmark-metric'>
                    <div class='benchmark-metric-val'>100%</div>
                    <div class='benchmark-metric-lbl'>Protected (15)</div>
                </div>
                <div class='benchmark-metric'>
                    <div class='benchmark-metric-val'>100%</div>
                    <div class='benchmark-metric-lbl'>Unseen (30)</div>
                </div>
                <div class='benchmark-metric'>
                    <div class='benchmark-metric-val'>95%</div>
                    <div class='benchmark-metric-lbl'>Generalization (60)</div>
                </div>
                <div class='benchmark-metric'>
                    <div class='benchmark-metric-val'>97.1%</div>
                    <div class='benchmark-metric-lbl'>Combined (105)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_architecture():
    """Render compact expandable architecture and routing policies."""
    with st.expander("Architecture & Routing Policy", expanded=False):
        st.markdown("""
        **Routing Principles:**
        - **◉ LOCAL (On-Device SLM):**
          Factual questions, concise explanations, simple code snippets, short creative prompts, translation. Computed entirely on-device using `Qwen2.5-1.5B-Instruct`. Zero cloud latency and 100% data privacy.
        
        - **⚙ COMMAND (Safe Action Engine):**
          External actions targeting devices, smart appliances, or simulated operating systems (e.g. turning on sprinkler timers, thermostat toggles, alarm configuration). Sandboxed within safe demonstration registry.
        
        - **☁ CLOUD (Cloud LLM):**
          Workloads demanding multi-step research, comprehensive itineraries, in-depth corporate reports, and complex reasoning exceeding edge compute budgets. Dispatched via Google Gemini (`gemini-2.5-flash`).
        """)


def main():
    st.set_page_config(
        page_title="SLM Router — Edge AI Intelligence Console",
        page_icon="⚡",
        layout="wide"
    )

    inject_custom_css()
    router = get_router()

    # Determine Cloud API status safely without ever logging or displaying the key
    cloud_status = router.cloud.get_api_status()

    # Session state initialization
    if "result" not in st.session_state:
        st.session_state.result = None
    if "query_text" not in st.session_state:
        st.session_state.query_text = ""

    # Header section
    render_header(cloud_status)

    # Active route for pipeline
    active_route = st.session_state.result.get("route") if st.session_state.result else None

    # Two column layout: Left = Interaction & Pipeline & Results, Right = Telemetry & Benchmarks
    col_main, col_side = st.columns([1.2, 0.8], gap="large")

    with col_main:
        # Dynamic Pipeline Visualization
        render_pipeline(active_route)

        # Query Input Area
        render_query_input(router)

        # Result display if routing has executed
        if st.session_state.result:
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            render_route_card(st.session_state.result)
            render_result(st.session_state.result)

    with col_side:
        # Live status / Telemetry
        if st.session_state.result:
            render_telemetry(st.session_state.result)

        # Benchmark health cards
        render_benchmark()

        # Expandable Architecture Section
        render_architecture()


if __name__ == "__main__":
    main()
