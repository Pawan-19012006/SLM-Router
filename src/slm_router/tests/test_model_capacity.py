import sys
from pathlib import Path
from collections import defaultdict

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM, MODEL_NAME
from slm_router.classifier import Classifier

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


def evaluate_dataset(classifier, dataset, dataset_name):
    total = len(dataset)
    correct = 0
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    confusion = {true_cls: {pred_cls: 0 for pred_cls in CLASSES + ["UNKNOWN"]} for true_cls in CLASSES}
    records = []
    incorrect_records = []

    print(f"\n{'='*70}")
    print(f"RUNNING EVALUATION: {dataset_name} ({total} queries)")
    print(f"{'='*70}")

    for idx, (query, expected) in enumerate(dataset, start=1):
        pred, raw = classifier.classify_with_raw(query)
        is_correct = (pred == expected)
        if is_correct:
            correct += 1
            class_correct[expected] += 1
        else:
            incorrect_records.append({
                "idx": idx,
                "query": query,
                "expected": expected,
                "predicted": pred,
                "raw": raw
            })

        class_total[expected] += 1
        pred_key = pred if pred in CLASSES else "UNKNOWN"
        confusion[expected][pred_key] += 1

        records.append({
            "idx": idx,
            "query": query,
            "expected": expected,
            "predicted": pred,
            "raw": raw,
            "correct": is_correct
        })

        status = "PASS" if is_correct else "FAIL"
        print(f"[{idx:02d}/{total:02d}] {status} | Query: \"{query}\" | Expected: {expected} | Pred: {pred} | Raw: [{raw}]")

    accuracy = (correct / total * 100.0) if total > 0 else 0.0

    print(f"\n{'-'*70}")
    print(f"SUMMARY: {dataset_name}")
    print(f"Overall Accuracy: {correct}/{total} = {accuracy:.2f}%")
    print(f"{'-'*70}")
    print("Per-class Accuracy:")
    class_acc = {}
    for c in CLASSES:
        cnt = class_total[c]
        cor = class_correct[c]
        acc = (cor / cnt * 100.0) if cnt > 0 else 0.0
        class_acc[c] = (cor, cnt, acc)
        print(f"  {c:<8}: {cor}/{cnt} = {acc:.2f}%")

    print(f"{'-'*70}")
    print("Confusion Matrix (Rows: True, Columns: Predicted):")
    headers = ["True\\Pred"] + CLASSES + ["UNKNOWN"]
    print(f"  {headers[0]:<12} " + " ".join(f"{h:>8}" for h in headers[1:]))
    for true_cls in CLASSES:
        row = f"  {true_cls:<12} " + " ".join(f"{confusion[true_cls][p]:>8}" for p in CLASSES + ["UNKNOWN"])
        print(row)

    print(f"{'-'*70}")
    if incorrect_records:
        print(f"Full list of incorrect predictions ({len(incorrect_records)}):")
        for rec in incorrect_records:
            print(f"  {rec['idx']:02d}. Query: \"{rec['query']}\"")
            print(f"      Expected: {rec['expected']} | Predicted: {rec['predicted']} | Raw: [{rec['raw']}]")
    else:
        print("Incorrect predictions: None (100% accuracy)!")
    print(f"{'='*70}")

    return {
        "dataset_name": dataset_name,
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "class_acc": class_acc,
        "confusion": confusion,
        "records": records,
        "incorrect_records": incorrect_records
    }


def main():
    print(f"Configured MODEL_NAME in slm_router.model: {MODEL_NAME}")
    print("Instantiating SLM...")
    slm = SLM()
    print("SLM instantiated successfully.")
    
    classifier = Classifier(slm)
    print("Classifier initialized with active baseline prompt.")

    # 1. Protected 15 Benchmark
    prot_res = evaluate_dataset(classifier, PROTECTED_15, "PROTECTED 15-QUERY BENCHMARK")

    # 2. Unseen 30 Benchmark
    unseen_res = evaluate_dataset(classifier, UNSEEN_30, "UNSEEN 30-QUERY BENCHMARK")

    print("\n" + "#"*70)
    print("FINAL CAPACITY COMPARISON")
    print("#"*70)
    print(f"{'Benchmark / Class':<25} | {'0.5B Baseline':<15} | {'1.5B Model':<15}")
    print("-" * 60)
    print(f"{'Protected (15 queries)':<25} | {'73.33% (11/15)':<15} | {prot_res['accuracy']:.2f}% ({prot_res['correct']}/{prot_res['total']})")
    print(f"{'Unseen (30 queries)':<25} | {'56.67% (17/30)':<15} | {unseen_res['accuracy']:.2f}% ({unseen_res['correct']}/{unseen_res['total']})")
    print("-" * 60)
    for c in CLASSES:
        prot_cor, prot_tot, prot_pct = prot_res['class_acc'][c]
        unseen_cor, unseen_tot, unseen_pct = unseen_res['class_acc'][c]
        tot_cor = prot_cor + unseen_cor
        tot_tot = prot_tot + unseen_tot
        tot_pct = (tot_cor / tot_tot * 100.0) if tot_tot > 0 else 0.0
        print(f"  {c + ' (Protected)':<23} | {'--':<15} | {prot_pct:.2f}% ({prot_cor}/{prot_tot})")
        print(f"  {c + ' (Unseen)':<23} | {'--':<15} | {unseen_pct:.2f}% ({unseen_cor}/{unseen_tot})")
    print("#"*70)


if __name__ == "__main__":
    main()
