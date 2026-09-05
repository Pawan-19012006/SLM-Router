import sys
from pathlib import Path
from collections import defaultdict

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM, MODEL_NAME
from slm_router.classifier import Classifier

# Protected Benchmark (15 queries)
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

# Unseen Benchmark (30 queries)
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

# NEW Independent Generalization Benchmark (60 queries: 20 LOCAL, 20 COMMAND, 20 CLOUD)
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

CLASSES = ["LOCAL", "COMMAND", "CLOUD"]


def evaluate(classifier, dataset, name):
    total = len(dataset)
    correct = 0
    class_correct = defaultdict(int)
    class_total = defaultdict(int)
    confusion = {true_cls: {pred_cls: 0 for pred_cls in CLASSES + ["UNKNOWN"]} for true_cls in CLASSES}
    incorrect_list = []

    print(f"\n{'='*75}")
    print(f"RUNNING EVALUATION: {name} ({total} queries)")
    print(f"{'='*75}")

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

        class_total[expected] += 1
        pred_key = pred if pred in CLASSES else "UNKNOWN"
        confusion[expected][pred_key] += 1

        status = "PASS" if passed else "FAIL"
        print(f"[{idx:02d}/{total:02d}] {status} | Expected: {expected:<7} | Pred: {pred:<7} | Raw: [{raw}] | Query: \"{query}\"")

    accuracy = (correct / total * 100.0) if total > 0 else 0.0
    class_acc = {}
    for c in CLASSES:
        cnt = class_total[c]
        cor = class_correct[c]
        acc = (cor / cnt * 100.0) if cnt > 0 else 0.0
        class_acc[c] = (cor, cnt, acc)

    print(f"\n{'-'*75}")
    print(f"SUMMARY: {name}")
    print(f"Overall Accuracy: {correct}/{total} = {accuracy:.2f}%")
    print(f"{'-'*75}")
    print("Per-class Accuracy:")
    for c in CLASSES:
        cor, cnt, acc = class_acc[c]
        print(f"  {c:<8}: {cor}/{cnt} = {acc:.2f}%")

    print(f"{'-'*75}")
    print("Confusion Matrix (Rows: True, Columns: Predicted):")
    headers = ["True\\Pred"] + CLASSES + ["UNKNOWN"]
    print(f"  {headers[0]:<12} " + " ".join(f"{h:>8}" for h in headers[1:]))
    for true_cls in CLASSES:
        row = f"  {true_cls:<12} " + " ".join(f"{confusion[true_cls][p]:>8}" for p in CLASSES + ["UNKNOWN"])
        print(row)

    print(f"{'-'*75}")
    if incorrect_list:
        print(f"Incorrect predictions ({len(incorrect_list)}):")
        for item in incorrect_list:
            print(f"  {item['idx']:02d}. Query: \"{item['query']}\"")
            print(f"      Expected: {item['expected']} | Predicted: {item['predicted']} | Raw Output: [{item['raw']}]")
    else:
        print("Incorrect predictions: None (100% accuracy)!")
    print(f"{'='*75}")

    return {
        "name": name,
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "class_acc": class_acc,
        "confusion": confusion,
        "incorrect_list": incorrect_list
    }


def main():
    print(f"Loading SLM with model: {MODEL_NAME}...")
    slm = SLM()
    classifier = Classifier(slm)

    # 1. Run New 60-Query Generalization Benchmark
    res_60 = evaluate(classifier, GENERALIZATION_60, "NEW 60-QUERY GENERALIZATION BENCHMARK")

    # 2. Run Existing Benchmarks for Comprehensive Verification
    res_prot15 = evaluate(classifier, PROTECTED_15, "PROTECTED 15-QUERY BENCHMARK")
    res_unseen30 = evaluate(classifier, UNSEEN_30, "EXISTING 30-QUERY UNSEEN BENCHMARK")

    # 3. Overall Combined Statistics (105 queries)
    total_105 = res_prot15['total'] + res_unseen30['total'] + res_60['total']
    correct_105 = res_prot15['correct'] + res_unseen30['correct'] + res_60['correct']
    acc_105 = (correct_105 / total_105 * 100.0)

    print("\n" + "#"*75)
    print("                 COMPREHENSIVE MULTI-BENCHMARK SUMMARY")
    print("#"*75)
    print(f"Protected Benchmark (15 queries):     {res_prot15['correct']}/{res_prot15['total']} = {res_prot15['accuracy']:.2f}%")
    print(f"Existing Unseen Benchmark (30 queries): {res_unseen30['correct']}/{res_unseen30['total']} = {res_unseen30['accuracy']:.2f}%")
    print(f"NEW Generalization Benchmark (60 queries): {res_60['correct']}/{res_60['total']} = {res_60['accuracy']:.2f}%")
    print("-" * 75)
    print(f"COMBINED TOTAL (105 QUERIES):         {correct_105}/{total_105} = {acc_105:.2f}%")
    print("#"*75)


if __name__ == "__main__":
    main()
