import sys
from pathlib import Path
from collections import defaultdict

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM, MODEL_NAME
from slm_router.classifier_v2 import ClassifierV2

# 1. Protected Benchmark (15 queries)
PROTECTED_15 = [
    ("What is 2 + 2?", "LOCAL"),
    ("What is the capital of India?", "LOCAL"),
    ("Explain photosynthesis in simple terms.", "LOCAL"),
    ("What is TCP?", "LOCAL"),
    ("Who wrote Romeo and Juliet?", "LOCAL"),
    ("Turn on the light.", "COMMAND"),
    ("Turn off the fan.", "COMMAND"),
    ("Open the door.", "COMMAND"),
    ("Start the music.", "COMMAND"),
    ("Launch the browser.", "COMMAND"),
    ("Tell me a 500-word story about a dragon.", "CLOUD"),
    ("Write a detailed research report about quantum computing.", "CLOUD"),
    ("Analyze the economic impact of artificial intelligence in detail.", "CLOUD"),
    ("Write a 3000-word essay about climate change.", "CLOUD"),
    ("Develop a detailed production-ready distributed system architecture.", "CLOUD"),
]

# 2. Existing Unseen Benchmark (30 queries)
UNSEEN_30 = [
    ("Give me a quick definition of recursion.", "LOCAL"),
    ("How many bytes are in a kilobyte?", "LOCAL"),
    ("Why does the sky appear blue?", "LOCAL"),
    ("Give me a simple explanation of DNS.", "LOCAL"),
    ("What is the speed of sound in air?", "LOCAL"),
    ("How do I print hello world in Python?", "LOCAL"),
    ("What is the chemical formula for water?", "LOCAL"),
    ("Translate 'good morning' to Spanish.", "LOCAL"),
    ("Can you provide a synonym for happy?", "LOCAL"),
    ("What is the freezing point of water in Celsius?", "LOCAL"),
    ("Could you activate the projector?", "COMMAND"),
    ("Please close the music player.", "COMMAND"),
    ("Would you mute the microphone?", "COMMAND"),
    ("Can you restart the application?", "COMMAND"),
    ("Lock the workstation now.", "COMMAND"),
    ("Set the system volume to 50 percent.", "COMMAND"),
    ("Disconnect from the current Wi-Fi network.", "COMMAND"),
    ("Dim the screen brightness.", "COMMAND"),
    ("Unmute the audio output.", "COMMAND"),
    ("Terminate the background process.", "COMMAND"),
    ("Prepare a comprehensive 1500-word analysis of semiconductor supply chains.", "CLOUD"),
    ("Create an extensive comparison of modern database architectures.", "CLOUD"),
    ("Develop a detailed implementation plan for a production-scale distributed system.", "CLOUD"),
    ("Write a thorough 2500-word research paper examining renewable energy storage technologies.", "CLOUD"),
    ("Draft a full enterprise disaster recovery strategy and multi-region failover guide.", "CLOUD"),
    ("Provide an exhaustive architectural breakdown of Kubernetes internal components and consensus algorithms.", "CLOUD"),
    ("Compose a detailed comparative study of zero-knowledge proofs versus optimistic rollups.", "CLOUD"),
    ("Formulate an in-depth security audit report identifying common vulnerabilities in DeFi smart contracts.", "CLOUD"),
    ("Produce an extensive 2000-word market overview on autonomous vehicle sensor fusion methods.", "CLOUD"),
    ("Design an end-to-end event-driven microservices architecture handling millions of transactions per second.", "CLOUD"),
]

# 3. New Generalization Benchmark (60 queries)
GENERALIZATION_60 = [
    # LOCAL (20)
    ("Show me the syntax for a for-loop in JavaScript.", "LOCAL"),
    ("Convert 'hello world' to uppercase.", "LOCAL"),
    ("What is the boiling point of ethanol?", "LOCAL"),
    ("Write a Python function that adds two numbers.", "LOCAL"),
    ("Translate 'thank you very much' into German.", "LOCAL"),
    ("Explain the difference between a stack and a queue.", "LOCAL"),
    ("How many ounces are in a pound?", "LOCAL"),
    ("Rephrase this sentence to sound more polite: 'Send me the invoice now.'", "LOCAL"),
    ("Calculate the square root of 144.", "LOCAL"),
    ("What does HTTP status code 404 signify?", "LOCAL"),
    ("Give me three examples of mammals that lay eggs.", "LOCAL"),
    ("How do I check if a key exists in a Python dictionary?", "LOCAL"),
    ("Capitalize the first letter of each word in 'data science institute'.", "LOCAL"),
    ("What is the primary function of hemoglobin in red blood cells?", "LOCAL"),
    ("Summarize the law of conservation of energy in one sentence.", "LOCAL"),
    ("Write a regex pattern to match a valid email address.", "LOCAL"),
    ("Translate the word 'butterfly' into French.", "LOCAL"),
    ("What year did the Apollo 11 moon landing occur?", "LOCAL"),
    ("Generate a short two-line rhyming couplet about autumn.", "LOCAL"),
    ("Tell me how to comment out a block of code in C++.", "LOCAL"),

    # COMMAND (20)
    ("Please reboot my laptop.", "COMMAND"),
    ("Could you switch to dark mode in the editor?", "COMMAND"),
    ("Empty the system recycle bin right away.", "COMMAND"),
    ("Would you mind pausing the download queue?", "COMMAND"),
    ("Open my terminal and run the test suite.", "COMMAND"),
    ("Turn off Bluetooth on this machine.", "COMMAND"),
    ("Kill process with PID 4128.", "COMMAND"),
    ("Can you take a screenshot and save it to my desktop?", "COMMAND"),
    ("Please log out of my user session.", "COMMAND"),
    ("Increase screen brightness to 80 percent.", "COMMAND"),
    ("Could you enable airplane mode?", "COMMAND"),
    ("Clear all browser cookies and cache.", "COMMAND"),
    ("Switch the audio output device to headphones.", "COMMAND"),
    ("Please start the PostgreSQL service.", "COMMAND"),
    ("Eject the external USB drive safely.", "COMMAND"),
    ("Lock the screen immediately.", "COMMAND"),
    ("Disable the webcam device.", "COMMAND"),
    ("Unzip the archive named data.zip into the current folder.", "COMMAND"),
    ("Please mute system notifications for the next hour.", "COMMAND"),
    ("Could you close all background tabs in Safari?", "COMMAND"),

    # CLOUD (20)
    ("Write a comprehensive 2000-word historical analysis of the fall of the Western Roman Empire.", "CLOUD"),
    ("Design a fault-tolerant multi-region event streaming pipeline handling 500k events per second.", "CLOUD"),
    ("Provide an exhaustive comparative technical study between Transformer attention mechanisms and State Space Models.", "CLOUD"),
    ("Draft a full 3000-word legal and regulatory compliance assessment for AI deployment in healthcare.", "CLOUD"),
    ("Develop an end-to-end disaster recovery and high-availability architecture for a global fintech platform.", "CLOUD"),
    ("Conduct a deep multi-page security vulnerability audit of an OAuth2 and OpenID Connect implementation.", "CLOUD"),
    ("Compose a detailed 1500-word research essay evaluating the environmental impact of lithium-ion battery recycling.", "CLOUD"),
    ("Create a complete production-grade microservices migration roadmap from a monolithic banking application.", "CLOUD"),
    ("Formulate an in-depth comparative breakdown of zero-knowledge rollup proofs: STARKs versus SNARKs.", "CLOUD"),
    ("Write an extensive 2500-word dissertation chapter on quantum decoherence and quantum error correction codes.", "CLOUD"),
    ("Develop a full machine learning operations (MLOps) architecture specification including feature store, monitoring, and automated retraining.", "CLOUD"),
    ("Produce an exhaustive 2000-word economic forecast analyzing the impact of demographic aging on global sovereign debt.", "CLOUD"),
    ("Design a distributed consensus protocol and state machine replication strategy for an untrusted peer-to-peer network.", "CLOUD"),
    ("Draft a comprehensive 3000-word enterprise cybersecurity incident response playbook.", "CLOUD"),
    ("Provide an in-depth architectural blueprint for an ultra-low-latency high-frequency trading matching engine.", "CLOUD"),
    ("Write a detailed 2000-word comparative review of modern compiler optimization techniques for heterogeneous compute.", "CLOUD"),
    ("Formulate a multi-phased digital transformation strategy for an international logistics network with legacy ERP systems.", "CLOUD"),
    ("Develop an extensive technical specification and database schema for a high-concurrency real-time collaborative document editor.", "CLOUD"),
    ("Compose a 2500-word critical evaluation of philosophical theories regarding consciousness and functionalism.", "CLOUD"),
    ("Create an exhaustive performance benchmarking guide and tuning methodology for petabyte-scale distributed data warehouses.", "CLOUD"),
]

# Known exact deterministic V1 predictions for all 105 queries
V1_PREDICTIONS = {
    # Protected 15 (15/15 correct)
    "What is 2 + 2?": "LOCAL",
    "What is the capital of India?": "LOCAL",
    "Explain photosynthesis in simple terms.": "LOCAL",
    "What is TCP?": "LOCAL",
    "Who wrote Romeo and Juliet?": "LOCAL",
    "Turn on the light.": "COMMAND",
    "Turn off the fan.": "COMMAND",
    "Open the door.": "COMMAND",
    "Start the music.": "COMMAND",
    "Launch the browser.": "COMMAND",
    "Tell me a 500-word story about a dragon.": "CLOUD",
    "Write a detailed research report about quantum computing.": "CLOUD",
    "Analyze the economic impact of artificial intelligence in detail.": "CLOUD",
    "Write a 3000-word essay about climate change.": "CLOUD",
    "Develop a detailed production-ready distributed system architecture.": "CLOUD",

    # Unseen 30 (28/30 correct)
    "Give me a quick definition of recursion.": "LOCAL",
    "How many bytes are in a kilobyte?": "LOCAL",
    "Why does the sky appear blue?": "LOCAL",
    "Give me a simple explanation of DNS.": "LOCAL",
    "What is the speed of sound in air?": "LOCAL",
    "How do I print hello world in Python?": "COMMAND", # error
    "What is the chemical formula for water?": "LOCAL",
    "Translate 'good morning' to Spanish.": "CLOUD",   # error
    "Can you provide a synonym for happy?": "LOCAL",
    "What is the freezing point of water in Celsius?": "LOCAL",
    "Could you activate the projector?": "COMMAND",
    "Please close the music player.": "COMMAND",
    "Would you mute the microphone?": "COMMAND",
    "Can you restart the application?": "COMMAND",
    "Lock the workstation now.": "COMMAND",
    "Set the system volume to 50 percent.": "COMMAND",
    "Disconnect from the current Wi-Fi network.": "COMMAND",
    "Dim the screen brightness.": "COMMAND",
    "Unmute the audio output.": "COMMAND",
    "Terminate the background process.": "COMMAND",
    "Prepare a comprehensive 1500-word analysis of semiconductor supply chains.": "CLOUD",
    "Create an extensive comparison of modern database architectures.": "CLOUD",
    "Develop a detailed implementation plan for a production-scale distributed system.": "CLOUD",
    "Write a thorough 2500-word research paper examining renewable energy storage technologies.": "CLOUD",
    "Draft a full enterprise disaster recovery strategy and multi-region failover guide.": "CLOUD",
    "Provide an exhaustive architectural breakdown of Kubernetes internal components and consensus algorithms.": "CLOUD",
    "Compose a detailed comparative study of zero-knowledge proofs versus optimistic rollups.": "CLOUD",
    "Formulate an in-depth security audit report identifying common vulnerabilities in DeFi smart contracts.": "CLOUD",
    "Produce an extensive 2000-word market overview on autonomous vehicle sensor fusion methods.": "CLOUD",
    "Design an end-to-end event-driven microservices architecture handling millions of transactions per second.": "CLOUD",

    # New 60 Generalization (52/60 correct)
    "Show me the syntax for a for-loop in JavaScript.": "LOCAL",
    "Convert 'hello world' to uppercase.": "COMMAND", # error
    "What is the boiling point of ethanol?": "LOCAL",
    "Write a Python function that adds two numbers.": "LOCAL",
    "Translate 'thank you very much' into German.": "CLOUD", # error
    "Explain the difference between a stack and a queue.": "LOCAL",
    "How many ounces are in a pound?": "LOCAL",
    "Rephrase this sentence to sound more polite: 'Send me the invoice now.'": "UNKNOWN", # error
    "Calculate the square root of 144.": "LOCAL",
    "What does HTTP status code 404 signify?": "LOCAL",
    "Give me three examples of mammals that lay eggs.": "CLOUD", # error
    "How do I check if a key exists in a Python dictionary?": "LOCAL",
    "Capitalize the first letter of each word in 'data science institute'.": "UNKNOWN", # error
    "What is the primary function of hemoglobin in red blood cells?": "LOCAL",
    "Summarize the law of conservation of energy in one sentence.": "UNKNOWN", # error
    "Write a regex pattern to match a valid email address.": "LOCAL",
    "Translate the word 'butterfly' into French.": "CLOUD", # error
    "What year did the Apollo 11 moon landing occur?": "LOCAL",
    "Generate a short two-line rhyming couplet about autumn.": "UNKNOWN", # error
    "Tell me how to comment out a block of code in C++.": "LOCAL",
    "Please reboot my laptop.": "COMMAND",
    "Could you switch to dark mode in the editor?": "COMMAND",
    "Empty the system recycle bin right away.": "COMMAND",
    "Would you mind pausing the download queue?": "COMMAND",
    "Open my terminal and run the test suite.": "COMMAND",
    "Turn off Bluetooth on this machine.": "COMMAND",
    "Kill process with PID 4128.": "COMMAND",
    "Can you take a screenshot and save it to my desktop?": "COMMAND",
    "Please log out of my user session.": "COMMAND",
    "Increase screen brightness to 80 percent.": "COMMAND",
    "Could you enable airplane mode?": "COMMAND",
    "Clear all browser cookies and cache.": "COMMAND",
    "Switch the audio output device to headphones.": "COMMAND",
    "Please start the PostgreSQL service.": "COMMAND",
    "Eject the external USB drive safely.": "COMMAND",
    "Lock the screen immediately.": "COMMAND",
    "Disable the webcam device.": "COMMAND",
    "Unzip the archive named data.zip into the current folder.": "COMMAND",
    "Please mute system notifications for the next hour.": "COMMAND",
    "Could you close all background tabs in Safari?": "COMMAND",
    "Write a comprehensive 2000-word historical analysis of the fall of the Western Roman Empire.": "CLOUD",
    "Design a fault-tolerant multi-region event streaming pipeline handling 500k events per second.": "CLOUD",
    "Provide an exhaustive comparative technical study between Transformer attention mechanisms and State Space Models.": "CLOUD",
    "Draft a full 3000-word legal and regulatory compliance assessment for AI deployment in healthcare.": "CLOUD",
    "Develop an end-to-end disaster recovery and high-availability architecture for a global fintech platform.": "CLOUD",
    "Conduct a deep multi-page security vulnerability audit of an OAuth2 and OpenID Connect implementation.": "CLOUD",
    "Compose a detailed 1500-word research essay evaluating the environmental impact of lithium-ion battery recycling.": "CLOUD",
    "Create a complete production-grade microservices migration roadmap from a monolithic banking application.": "CLOUD",
    "Formulate an in-depth comparative breakdown of zero-knowledge rollup proofs: STARKs versus SNARKs.": "CLOUD",
    "Write an extensive 2500-word dissertation chapter on quantum decoherence and quantum error correction codes.": "CLOUD",
    "Develop a full machine learning operations (MLOps) architecture specification including feature store, monitoring, and automated retraining.": "CLOUD",
    "Produce an exhaustive 2000-word economic forecast analyzing the impact of demographic aging on global sovereign debt.": "CLOUD",
    "Design a distributed consensus protocol and state machine replication strategy for an untrusted peer-to-peer network.": "CLOUD",
    "Draft a comprehensive 3000-word enterprise cybersecurity incident response playbook.": "CLOUD",
    "Provide an in-depth architectural blueprint for an ultra-low-latency high-frequency trading matching engine.": "CLOUD",
    "Write a detailed 2000-word comparative review of modern compiler optimization techniques for heterogeneous compute.": "CLOUD",
    "Formulate a multi-phased digital transformation strategy for an international logistics network with legacy ERP systems.": "CLOUD",
    "Develop an extensive technical specification and database schema for a high-concurrency real-time collaborative document editor.": "CLOUD",
    "Compose a 2500-word critical evaluation of philosophical theories regarding consciousness and functionalism.": "CLOUD",
    "Create an exhaustive performance benchmarking guide and tuning methodology for petabyte-scale distributed data warehouses.": "CLOUD",
}

CLASSES = ["LOCAL", "COMMAND", "CLOUD"]


def evaluate_dataset(classifier_v2, dataset, dataset_name):
    total = len(dataset)
    correct_v2 = 0
    class_correct_v2 = defaultdict(int)
    class_total = defaultdict(int)
    confusion_v2 = {true_cls: {pred_cls: 0 for pred_cls in CLASSES + ["UNKNOWN"]} for true_cls in CLASSES}
    records = []

    print(f"\n{'='*75}")
    print(f"RUNNING V2 EVALUATION: {dataset_name} ({total} queries)")
    print(f"{'='*75}")

    for idx, (query, expected) in enumerate(dataset, start=1):
        pred_v2, raw_v2 = classifier_v2.classify_with_raw(query)
        pred_v1 = V1_PREDICTIONS[query]

        is_correct_v2 = (pred_v2 == expected)
        is_correct_v1 = (pred_v1 == expected)

        if is_correct_v2:
            correct_v2 += 1
            class_correct_v2[expected] += 1

        class_total[expected] += 1
        pred_key = pred_v2 if pred_v2 in CLASSES else "UNKNOWN"
        confusion_v2[expected][pred_key] += 1

        change_marker = ""
        if pred_v2 != pred_v1:
            if is_correct_v2 and not is_correct_v1:
                change_marker = " [IMPROVED!]"
            elif not is_correct_v2 and is_correct_v1:
                change_marker = " [REGRESSION!]"
            else:
                change_marker = " [CHANGED]"

        records.append({
            "idx": idx,
            "query": query,
            "expected": expected,
            "v1_pred": pred_v1,
            "v2_pred": pred_v2,
            "v2_raw": raw_v2,
            "v1_correct": is_correct_v1,
            "v2_correct": is_correct_v2,
            "marker": change_marker
        })

        status_v2 = "PASS" if is_correct_v2 else "FAIL"
        print(f"[{idx:02d}/{total:02d}] {status_v2} | Exp: {expected:<7} | V1: {pred_v1:<7} | V2: {pred_v2:<7} | Raw: [{raw_v2}]{change_marker} | \"{query}\"")

    accuracy_v2 = (correct_v2 / total * 100.0) if total > 0 else 0.0

    class_acc_v2 = {}
    for c in CLASSES:
        cnt = class_total[c]
        cor = class_correct_v2[c]
        acc = (cor / cnt * 100.0) if cnt > 0 else 0.0
        class_acc_v2[c] = (cor, cnt, acc)

    return {
        "name": dataset_name,
        "total": total,
        "correct": correct_v2,
        "accuracy": accuracy_v2,
        "class_acc": class_acc_v2,
        "confusion": confusion_v2,
        "records": records
    }


def main():
    print(f"Loading SLM with {MODEL_NAME}...")
    slm = SLM()
    classifier_v2 = ClassifierV2(slm)

    res_prot = evaluate_dataset(classifier_v2, PROTECTED_15, "PROTECTED 15-QUERY BENCHMARK")
    res_unseen = evaluate_dataset(classifier_v2, UNSEEN_30, "EXISTING 30-QUERY UNSEEN BENCHMARK")
    res_gen60 = evaluate_dataset(classifier_v2, GENERALIZATION_60, "NEW 60-QUERY GENERALIZATION BENCHMARK")

    all_records = res_prot["records"] + res_unseen["records"] + res_gen60["records"]
    total_105 = len(all_records)
    v2_total_correct = sum(1 for r in all_records if r["v2_correct"])
    v1_total_correct = sum(1 for r in all_records if r["v1_correct"])
    v2_acc_105 = (v2_total_correct / total_105 * 100.0)
    v1_acc_105 = (v1_total_correct / total_105 * 100.0)

    # Per-class totals
    v1_class_cor = defaultdict(int)
    v2_class_cor = defaultdict(int)
    class_totals = defaultdict(int)
    v2_unknown_count = sum(1 for r in all_records if r["v2_pred"] not in CLASSES)
    v1_unknown_count = sum(1 for r in all_records if r["v1_pred"] not in CLASSES)

    for r in all_records:
        exp = r["expected"]
        class_totals[exp] += 1
        if r["v1_correct"]:
            v1_class_cor[exp] += 1
        if r["v2_correct"]:
            v2_class_cor[exp] += 1

    changed = [r for r in all_records if r["v1_pred"] != r["v2_pred"]]
    regressions = [r for r in all_records if r["v1_correct"] and not r["v2_correct"]]
    newly_corrected = [r for r in all_records if not r["v1_correct"] and r["v2_correct"]]
    remaining_local_errors = [r for r in all_records if r["expected"] == "LOCAL" and not r["v2_correct"]]

    print("\n" + "#" * 80)
    print("                    V1 vs V2 EXPERIMENTAL COMPARISON")
    print("#" * 80)
    print(f"{'Benchmark Slice':<35} | {'V1 Baseline':<18} | {'V2 Candidate':<18} | {'Delta'}")
    print("-" * 80)
    print(f"{'Protected Benchmark (15 queries)':<35} | 15/15 (100.00%)    | {res_prot['correct']}/15 ({res_prot['accuracy']:.2f}%)   | {res_prot['accuracy'] - 100.0:+.2f}%")
    print(f"{'Existing Unseen (30 queries)':<35} | 28/30 (93.33%)     | {res_unseen['correct']}/30 ({res_unseen['accuracy']:.2f}%)   | {res_unseen['accuracy'] - 93.33:+.2f}%")
    print(f"{'New Generalization (60 queries)':<35} | 52/60 (86.67%)     | {res_gen60['correct']}/60 ({res_gen60['accuracy']:.2f}%)   | {res_gen60['accuracy'] - 86.67:+.2f}%")
    print("-" * 80)
    print(f"{'COMBINED TOTAL (105 QUERIES)':<35} | {v1_total_correct}/105 ({v1_acc_105:.2f}%)  | {v2_total_correct}/105 ({v2_acc_105:.2f}%)  | {v2_acc_105 - v1_acc_105:+.2f}%")
    print("#" * 80)

    print("\nPER-CLASS ACCURACY COMPARISON:")
    print(f"{'Class':<12} | {'V1 Baseline':<18} | {'V2 Candidate':<18} | {'Delta'}")
    print("-" * 60)
    for c in CLASSES:
        cnt = class_totals[c]
        v1_c = v1_class_cor[c]
        v2_c = v2_class_cor[c]
        v1_p = (v1_c / cnt * 100.0) if cnt > 0 else 0.0
        v2_p = (v2_c / cnt * 100.0) if cnt > 0 else 0.0
        print(f"{c:<12} | {v1_c}/{cnt} ({v1_p:.2f}%)     | {v2_c}/{cnt} ({v2_p:.2f}%)     | {v2_p - v1_p:+.2f}%")
    print(f"{'UNKNOWN':<12} | {v1_unknown_count:<18} | {v2_unknown_count:<18} | {v2_unknown_count - v1_unknown_count:+d}")

    print("\n" + "=" * 80)
    print(f"CHANGED PREDICTIONS ({len(changed)} total):")
    print("=" * 80)
    for r in changed:
        print(f"- \"{r['query']}\"")
        print(f"  Expected: {r['expected']} | V1: {r['v1_pred']} | V2: {r['v2_pred']} (raw: [{r['v2_raw']}]) {r['marker']}")

    print("\n" + "=" * 80)
    print(f"REGRESSIONS ({len(regressions)} total):")
    print("=" * 80)
    if regressions:
        for r in regressions:
            print(f"- \"{r['query']}\"")
            print(f"  Expected: {r['expected']} | V1: {r['v1_pred']} (PASS) -> V2: {r['v2_pred']} (FAIL, raw: [{r['v2_raw']}])")
    else:
        print("None! Zero regressions.")

    print("\n" + "=" * 80)
    print(f"NEWLY CORRECTED LOCAL ERRORS ({len(newly_corrected)} total):")
    print("=" * 80)
    if newly_corrected:
        for r in newly_corrected:
            print(f"- \"{r['query']}\"")
            print(f"  Expected: {r['expected']} | V1: {r['v1_pred']} (FAIL) -> V2: {r['v2_pred']} (PASS, raw: [{r['v2_raw']}])")
    else:
        print("None.")

    print("\n" + "=" * 80)
    print(f"REMAINING LOCAL ERRORS IN V2 ({len(remaining_local_errors)} total):")
    print("=" * 80)
    for r in remaining_local_errors:
        print(f"- \"{r['query']}\"")
        print(f"  Expected: {r['expected']} | V2: {r['v2_pred']} (raw: [{r['v2_raw']}])")

    print("\n" + "=" * 80)
    print("V2 CONFUSION MATRIX (105 Queries):")
    headers = ["True\\Pred"] + CLASSES + ["UNKNOWN"]
    print(f"  {headers[0]:<12} " + " ".join(f"{h:>8}" for h in headers[1:]))
    tot_confusion = {tc: {pc: 0 for pc in CLASSES + ["UNKNOWN"]} for tc in CLASSES}
    for r in all_records:
        tc = r["expected"]
        pc = r["v2_pred"] if r["v2_pred"] in CLASSES else "UNKNOWN"
        tot_confusion[tc][pc] += 1
    for true_cls in CLASSES:
        row = f"  {true_cls:<12} " + " ".join(f"{tot_confusion[true_cls][p]:>8}" for p in CLASSES + ["UNKNOWN"])
        print(row)
    print("=" * 80)


if __name__ == "__main__":
    main()
