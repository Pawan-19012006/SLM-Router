from slm_router.model import SLM
from slm_router.classifier import Classifier

TEST_CASES = [
    # --- 10 LOCAL ---
    {
        "query": "What is the capital of France?",
        "expected": "LOCAL"
    },
    {
        "query": "What is 15 * 12?",
        "expected": "LOCAL"
    },
    {
        "query": "Explain photosynthesis in two sentences.",
        "expected": "LOCAL"
    },
    {
        "query": "How many days are in a leap year?",
        "expected": "LOCAL"
    },
    {
        "query": "Translate 'hello, how are you' into Spanish.",
        "expected": "LOCAL"
    },
    {
        "query": "Convert 50 miles to kilometers.",
        "expected": "LOCAL"
    },
    {
        "query": "Who wrote the play Hamlet?",
        "expected": "LOCAL"
    },
    {
        "query": "What is the boiling point of water in Celsius?",
        "expected": "LOCAL"
    },
    {
        "query": "Fix the spelling and grammar in this sentence: 'He dont have no time today.'",
        "expected": "LOCAL"
    },
    {
        "query": "Give me 3 synonyms for the word 'happy'.",
        "expected": "LOCAL"
    },

    # --- 10 COMMAND ---
    {
        "query": "Turn on the living room lights.",
        "expected": "COMMAND"
    },
    {
        "query": "Open Spotify and play my Discover Weekly playlist.",
        "expected": "COMMAND"
    },
    {
        "query": "Set a timer for 15 minutes.",
        "expected": "COMMAND"
    },
    {
        "query": "Mute the system audio.",
        "expected": "COMMAND"
    },
    {
        "query": "Delete all temporary files in the downloads directory.",
        "expected": "COMMAND"
    },
    {
        "query": "Create a new folder called 'ProjectDocs' on my desktop.",
        "expected": "COMMAND"
    },
    {
        "query": "Shutdown the computer in 30 minutes.",
        "expected": "COMMAND"
    },
    {
        "query": "Send an email to team@example.com with the subject 'Meeting Notes'.",
        "expected": "COMMAND"
    },
    {
        "query": "Increase screen brightness to 80%.",
        "expected": "COMMAND"
    },
    {
        "query": "Lock my workstation.",
        "expected": "COMMAND"
    },

    # --- 10 CLOUD ---
    {
        "query": "Write a 2000-word research report on quantum computing algorithms and their cryptography implications.",
        "expected": "CLOUD"
    },
    {
        "query": "Perform an in-depth economic analysis of the macroeconomic effects of generative AI on global labor markets over the next decade.",
        "expected": "CLOUD"
    },
    {
        "query": "Design an end-to-end fault-tolerant distributed consensus system supporting multi-region replication and Byzantine fault tolerance.",
        "expected": "CLOUD"
    },
    {
        "query": "Write a comprehensive 15-page market entry strategy and financial projection model for a B2B SaaS startup.",
        "expected": "CLOUD"
    },
    {
        "query": "Analyze the sociopolitical causes and long-term geopolitical consequences of the fall of the Roman Empire in detail.",
        "expected": "CLOUD"
    },
    {
        "query": "Implement a complete production-ready Kubernetes custom resource controller in Go with full reconciliation loops and metric instrumentation.",
        "expected": "CLOUD"
    },
    {
        "query": "Write a multi-chapter science fiction novella exploring transhumanism and consciousness uploading with rich character development.",
        "expected": "CLOUD"
    },
    {
        "query": "Critically evaluate the architectural tradeoffs between microservices, event-driven architectures, and modular monoliths in high-throughput banking systems.",
        "expected": "CLOUD"
    },
    {
        "query": "Draft a comprehensive legal and regulatory compliance framework for handling multi-jurisdictional health data under GDPR and HIPAA.",
        "expected": "CLOUD"
    },
    {
        "query": "Deconstruct the mathematical proofs behind zero-knowledge SNARKs and compare them with STARKs in computational complexity.",
        "expected": "CLOUD"
    }
]


def run_experiment():
    print("Initializing SLM...")
    slm = SLM()
    classifier = Classifier(slm)

    total = len(TEST_CASES)
    correct = 0

    print("\nStarting 30-Query Router Experiment\n" + "=" * 60)

    for i, test in enumerate(TEST_CASES, start=1):
        query = test["query"]
        expected = test["expected"]

        predicted, raw_output = classifier.classify_with_raw(query)
        passed = (predicted == expected)

        if passed:
            correct += 1

        status = "PASS" if passed else "FAIL"

        print(f"\nTEST {i}")
        print(f"QUERY: {query}")
        print(f"RAW SLM: [{raw_output}]")
        print(f"EXPECTED: {expected}")
        print(f"PREDICTED: {predicted}")
        print(f"RESULT: {status}")

    accuracy = (correct / total) * 100.0

    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print(f"Total: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    run_experiment()
