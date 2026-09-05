import sys
from pathlib import Path
from collections import defaultdict

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM
from slm_router.classifier_v2 import ClassifierV2

PROTECTED_15 = [
    # LOCAL (5)
    ("What is 2 + 2?", "LOCAL"),
    ("What is the capital of India?", "LOCAL"),
    ("Explain photosynthesis in simple terms.", "LOCAL"),
    ("What is TCP?", "LOCAL"),
    ("Who wrote Romeo and Juliet?", "LOCAL"),

    # COMMAND (5)
    ("Turn on the light.", "COMMAND"),
    ("Turn off the fan.", "COMMAND"),
    ("Open the door.", "COMMAND"),
    ("Start the music.", "COMMAND"),
    ("Launch the browser.", "COMMAND"),

    # CLOUD (5)
    ("Tell me a 500-word story about a dragon.", "CLOUD"),
    ("Write a detailed research report about quantum computing.", "CLOUD"),
    ("Analyze the economic impact of artificial intelligence in detail.", "CLOUD"),
    ("Write a 3000-word essay about climate change.", "CLOUD"),
    ("Develop a detailed production-ready distributed system architecture.", "CLOUD"),
]

UNSEEN_30 = [
    # LOCAL (10)
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

    # COMMAND (10)
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

    # CLOUD (10)
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

CLASSES = ["LOCAL", "COMMAND", "CLOUD"]


def evaluate(classifier, dataset, name):
    total = len(dataset)
    correct = 0
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    confusion = {true_cls: {pred_cls: 0 for pred_cls in CLASSES + ["UNKNOWN"]} for true_cls in CLASSES}
    unknown_count = 0
    incorrect_list = []

    for idx, (query, expected) in enumerate(dataset, start=1):
        pred, raw = classifier.classify_with_raw(query)
        passed = (pred == expected)

        if passed:
            correct += 1
            class_correct[expected] += 1
        else:
            incorrect_list.append({
                "idx": idx,
                "query": query,
                "expected": expected,
                "predicted": pred,
                "raw": raw
            })

        if pred == "UNKNOWN":
            unknown_count += 1

        class_total[expected] += 1
        pred_key = pred if pred in CLASSES else "UNKNOWN"
        confusion[expected][pred_key] += 1

    accuracy = (correct / total * 100.0) if total > 0 else 0.0
    class_acc = {}
    for c in CLASSES:
        cnt = class_total[c]
        cor = class_correct[c]
        acc = (cor / cnt * 100.0) if cnt > 0 else 0.0
        class_acc[c] = (cor, cnt, acc)

    return {
        "name": name,
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy": accuracy,
        "class_acc": class_acc,
        "confusion": confusion,
        "unknown_count": unknown_count,
        "incorrect_list": incorrect_list
    }


def print_evaluation(res):
    print("\n" + "=" * 60)
    print(f"EVALUATION RESULTS: {res['name']}")
    print("=" * 60)
    print(f"Overall Accuracy: {res['correct']}/{res['total']} = {res['accuracy']:.2f}%")
    print(f"UNKNOWN Count:   {res['unknown_count']}")
    print("-" * 60)
    print("Per-class accuracy:")
    for c in CLASSES:
        cor, cnt, acc = res['class_acc'][c]
        print(f"  {c:<8}: {cor}/{cnt} = {acc:.2f}%")
    print("-" * 60)
    print("Confusion Matrix (Rows: True, Columns: Predicted):")
    headers = ["True\\Pred"] + CLASSES + ["UNKNOWN"]
    print(f"  {headers[0]:<12} " + " ".join(f"{h:>8}" for h in headers[1:]))
    for true_cls in CLASSES:
        row = f"  {true_cls:<12} " + " ".join(f"{res['confusion'][true_cls][p]:>8}" for p in CLASSES + ["UNKNOWN"])
        print(row)
    print("-" * 60)
    if res['incorrect_list']:
        print(f"Incorrect queries ({len(res['incorrect_list'])}):")
        for item in res['incorrect_list']:
            print(f"  {item['idx']}. \"{item['query']}\" → predicted: {item['predicted']} (raw: [{item['raw']}]) → expected: {item['expected']}")
    else:
        print("Incorrect queries: None! Perfect score.")
    print("=" * 60)


def main():
    print("Loading SLM model...")
    slm = SLM()
    classifier_v2 = ClassifierV2(slm)

    print("\nEvaluating V2 on Protected 15 Benchmark...")
    v2_prot = evaluate(classifier_v2, PROTECTED_15, "V2 PROTECTED (15 queries)")
    print_evaluation(v2_prot)

    print("\nEvaluating V2 on Unseen 30 Benchmark...")
    v2_unseen = evaluate(classifier_v2, UNSEEN_30, "V2 UNSEEN (30 queries)")
    print_evaluation(v2_unseen)

    print("\n" + "=" * 60)
    print("               FINAL V2 BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"V2 PROTECTED: {v2_prot['correct']}/{v2_prot['total']} = {v2_prot['accuracy']:.2f}%  (Baseline: 11/15 = 73.33%)")
    print(f"V2 UNSEEN:    {v2_unseen['correct']}/{v2_unseen['total']} = {v2_unseen['accuracy']:.2f}%  (Baseline: 17/30 = 56.67%)")
    print("-" * 60)
    
    passed_gate = v2_prot['accuracy'] >= 73.33
    gate_verdict = "PASS REGRESSION GATE" if passed_gate else "FAIL REGRESSION GATE"
    print(f"Regression Gate Verdict: {gate_verdict} (Threshold: 73.33%)")

    improved_unseen = v2_unseen['accuracy'] > 56.67
    generalization_verdict = "YES, improved unseen generalization" if improved_unseen else ("NO, did not improve" if v2_unseen['accuracy'] < 56.67 else "EQUAL to baseline")
    print(f"Unseen Generalization:   {generalization_verdict}")
    print("=" * 60)


if __name__ == "__main__":
    main()
