import sys
import json
from pathlib import Path
from datetime import datetime
import streamlit as st

# Ensure src is in sys.path
repo_root = Path(__file__).resolve().parent
src_path = repo_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM
from slm_router.classifier import Classifier

EVAL_FILE = repo_root / "evaluations.json"


@st.cache_resource
def load_classifier():
    slm = SLM()
    return Classifier(slm)


def load_evaluations():
    if not EVAL_FILE.exists():
        return []
    try:
        with open(EVAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_evaluations(records):
    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def main():
    st.set_page_config(page_title="SLM Router — Manual Evaluation", layout="wide")
    st.title("SLM Router — Manual Evaluation")

    classifier = load_classifier()

    # Session state initialization
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
    if "predicted_label" not in st.session_state:
        st.session_state.predicted_label = None
    if "raw_output" not in st.session_state:
        st.session_state.raw_output = None

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Test a Query")
        query_input = st.text_area("Enter a user query", height=120, key="query_text")

        if st.button("Classify", type="primary"):
            cleaned = query_input.strip()
            if not cleaned:
                st.warning("Please enter a query to classify.")
            else:
                with st.spinner("Classifying query..."):
                    pred, raw = classifier.classify_with_raw(cleaned)
                    st.session_state.current_query = cleaned
                    st.session_state.predicted_label = pred
                    st.session_state.raw_output = raw

        if st.session_state.predicted_label:
            st.divider()
            st.markdown("### Prediction")
            label = st.session_state.predicted_label

            badge_color = "#1f77b4"
            if label == "COMMAND":
                badge_color = "#ff7f0e"
            elif label == "CLOUD":
                badge_color = "#2ca02c"
            elif label == "UNKNOWN":
                badge_color = "#d62728"

            st.markdown(
                f"<div style='font-size: 28px; font-weight: bold; color: {badge_color}; margin-bottom: 8px;'>"
                f"{label}</div>",
                unsafe_allow_html=True
            )

            if st.session_state.raw_output:
                st.caption(f"**Raw Model Output:** `{st.session_state.raw_output}`")

            st.markdown("#### Record Ground Truth")
            expected_label = st.radio(
                "What should the correct category be?",
                options=["LOCAL", "COMMAND", "CLOUD"],
                horizontal=True,
                key="expected_category"
            )

            if st.button("Record Evaluation"):
                records = load_evaluations()
                is_correct = (st.session_state.predicted_label == expected_label)
                record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": st.session_state.current_query,
                    "predicted": st.session_state.predicted_label,
                    "expected": expected_label,
                    "correct": is_correct
                }
                records.append(record)
                save_evaluations(records)
                st.success("Evaluation recorded successfully!")

    with col2:
        st.subheader("Evaluation Statistics & History")
        records = load_evaluations()
        total = len(records)
        correct_count = sum(1 for r in records if r.get("correct", False))
        incorrect_count = total - correct_count
        accuracy = (correct_count / total * 100) if total > 0 else 0.0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tests", total)
        m2.metric("Correct", correct_count)
        m3.metric("Incorrect", incorrect_count)
        m4.metric("Accuracy", f"{accuracy:.1f}%")

        st.divider()
        st.markdown("### Evaluation History")
        if records:
            display_data = []
            for r in reversed(records):
                display_data.append({
                    "Timestamp": r.get("timestamp"),
                    "Query": r.get("query"),
                    "Predicted": r.get("predicted"),
                    "Expected": r.get("expected"),
                    "Result": "PASS" if r.get("correct") else "FAIL"
                })
            st.dataframe(display_data, use_container_width=True, hide_index=True)
        else:
            st.info("No evaluations recorded yet.")

        st.divider()
        with st.expander("Danger Zone: Clear Evaluation Data"):
            st.write("This will permanently remove all stored evaluation records.")
            confirm = st.checkbox("I confirm I want to clear all evaluation data")
            if st.button("Clear Evaluation Data", type="secondary", disabled=not confirm):
                if EVAL_FILE.exists():
                    EVAL_FILE.unlink()
                st.success("All evaluation records cleared.")
                st.rerun()


if __name__ == "__main__":
    main()
