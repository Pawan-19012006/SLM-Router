import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Ensure src is in sys.path
repo_root = Path(__file__).resolve().parent
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.router import Router


@st.cache_resource
def get_router():
    """Load SLM and Router once in memory."""
    return Router()


def main():
    st.set_page_config(
        page_title="SLM Router — 3-Way AI Request Router",
        page_icon="⚡",
        layout="wide"
    )

    # Custom styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #6c757d;
            margin-bottom: 1.5rem;
        }
        .pipeline-box {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 14px;
            font-family: monospace;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        .route-card {
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-header'>⚡ SLM ROUTER</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-header'>Local 3-Way Request Classifier & Execution Dispatcher powered by <b>Qwen2.5-1.5B-Instruct</b></div>",
        unsafe_allow_html=True
    )

    # Pipeline visualization banner
    st.markdown("""
    <div class='pipeline-box'>
        <b>ROUTING PIPELINE:</b><br>
        [USER QUERY] ➔ <b>[Qwen2.5-1.5B V3 CLASSIFIER]</b> ➔ <b>{ LOCAL | COMMAND | CLOUD }</b> ➔ [SELECTED HANDLER] ➔ [FINAL RESULT]
    </div>
    """, unsafe_allow_html=True)

    router = get_router()

    # Session state initialization
    if "result" not in st.session_state:
        st.session_state.result = None
    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.subheader("Ask something:")
        
        # Example quick buttons
        st.caption("Quick sample queries:")
        b_col1, b_col2, b_col3 = st.columns(3)
        if b_col1.button("💧 Sprinkler (COMMAND)"):
            st.session_state.query_input = "Turn the garden sprinkler on for 15 minutes."
        if b_col2.button("🌊 Ocean Blue (LOCAL)"):
            st.session_state.query_input = "Why is the ocean blue?"
        if b_col3.button("📊 AI Report (CLOUD)"):
            st.session_state.query_input = "Create a detailed 3000-word research report on AI employment."

        user_query = st.text_area(
            "Enter your request:",
            value=st.session_state.query_input,
            height=110,
            placeholder="Type any question, command, or research request here...",
            label_visibility="collapsed"
        )

        route_clicked = st.button("⚡ ROUTE REQUEST", type="primary", use_container_width=True)

        if route_clicked:
            cleaned = user_query.strip()
            if not cleaned:
                st.warning("Please enter a query before routing.")
            else:
                with st.spinner("Classifying and routing request..."):
                    result = router.route(cleaned)
                    st.session_state.result = result

        if st.session_state.result:
            res = st.session_state.result
            route = res.get("route", "UNKNOWN")
            handler = res.get("handler", "None")

            st.divider()
            st.subheader("Routing Decision")

            badge_color = "#1f77b4"
            badge_icon = "ℹ️"
            if route == "LOCAL":
                badge_color = "#2ca02c"
                badge_icon = "💻"
            elif route == "COMMAND":
                badge_color = "#ff7f0e"
                badge_icon = "⚙️"
            elif route == "CLOUD":
                badge_color = "#17a2b8"
                badge_icon = "☁️"

            st.markdown(
                f"""
                <div style='background-color: {badge_color}15; border-left: 5px solid {badge_color}; padding: 12px; border-radius: 4px; margin-bottom: 12px;'>
                    <div style='font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: {badge_color}; font-weight: bold;'>
                        {badge_icon} Automated Route: {route}
                    </div>
                    <div style='font-size: 18px; font-weight: 600; color: #212529;'>
                        Handler: {handler}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("Result")

            if route == "LOCAL":
                st.success("✅ Processed locally via Qwen2.5-1.5B SLM")
                st.markdown("#### Generated Answer:")
                st.write(res.get("response", ""))
                with st.expander("Technical Execution Metadata"):
                    st.json(res.get("details", {}))

            elif route == "COMMAND":
                st.info("⚙️ Dispatched to Safe Simulated Command Executor")
                col_c1, col_c2 = st.columns(2)
                col_c1.metric("Action Detected", res.get("action", ""))
                col_c2.metric("Execution Status", res.get("status", ""))

                details = res.get("details", {})
                if details.get("execution_details"):
                    st.caption(f"**Execution Details:** `{details.get('execution_details')}`")

                st.markdown("#### Execution Output:")
                st.code(res.get("response", ""), language="text")

            elif route == "CLOUD":
                st.info("☁️ Routed to Cloud LLM Offloader (Mock Mode)")
                st.metric("Status", res.get("status", "READY FOR CLOUD LLM"))
                st.caption(f"**Complexity Level:** `{res.get('details', {}).get('complexity')}`")
                st.markdown("#### Payload Summary:")
                st.code(res.get("response", ""), language="text")

            else:
                st.error("Ambiguous Route: Fallback handler engaged.")
                st.write(res.get("response", ""))

    with col2:
        st.subheader("Architecture & Guidelines")
        with st.container(border=True):
            st.markdown("### 🧭 Route Policies")
            st.markdown("""
            - **💻 LOCAL (Local SLM):**  
              Factual Q&A, definitions, brief explanations, simple calculations, basic coding questions, small translations, and short creative text. Computed directly on-device using `Qwen2.5-1.5B-Instruct`.
            
            - **⚙️ COMMAND (Command Executor):**  
              External actions performed on devices, appliances, operating systems, or applications (e.g. turning on lights, launching apps, audio control, sprinkler timers). Sandboxed in a safe demonstration registry without arbitrary shell execution.
            
            - **☁️ CLOUD (Cloud LLM):**  
              Workloads requiring deep research, comprehensive multi-day planning, production architecture, 500+ word essays, or heavy reasoning. Prepared for cloud API offloading.
            """)

        with st.container(border=True):
            st.markdown("### 📊 Router Benchmark Health")
            m1, m2 = st.columns(2)
            m1.metric("Protected 15 Suite", "100.0%")
            m2.metric("Unseen 30 Suite", "100.0%")
            m3, m4 = st.columns(2)
            m3.metric("Generalization 60 Suite", "95.0%")
            m4.metric("Combined 105 Accuracy", "97.1%")


if __name__ == "__main__":
    main()
