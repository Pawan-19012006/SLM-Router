import sys
from pathlib import Path

# Ensure src is in sys.path
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from slm_router.model import SLM
from slm_router.classifier import Classifier

TEST_CASES = [
    # LOCAL
    ("What is 2 + 2?", "LOCAL"),
    ("What is the capital of India?", "LOCAL"),
    ("Explain photosynthesis in simple terms.", "LOCAL"),
    ("What is TCP?", "LOCAL"),
    ("Who wrote Romeo and Juliet?", "LOCAL"),

    # COMMAND
    ("Turn on the light.", "COMMAND"),
    ("Turn off the fan.", "COMMAND"),
    ("Open the door.", "COMMAND"),
    ("Start the music.", "COMMAND"),
    ("Launch the browser.", "COMMAND"),

    # CLOUD
    ("Tell me a 500-word story about a dragon.", "CLOUD"),
    ("Write a detailed research report about quantum computing.", "CLOUD"),
    ("Analyze the economic impact of artificial intelligence in detail.", "CLOUD"),
    ("Write a 3000-word essay about climate change.", "CLOUD"),
    ("Develop a detailed production-ready distributed system architecture.", "CLOUD"),
]


def main():
    slm = SLM()
    classifier = Classifier(slm)

    total_tests = len(TEST_CASES)
    correct = 0
    incorrect = 0

    print("==================================================")
    print("STARTING 15-QUERY CLASSIFIER TEST")
    print("==================================================")

    for i, (query, expected) in enumerate(TEST_CASES, start=1):
        predicted = classifier.classify(query)
        passed = (predicted == expected)

        if passed:
            correct += 1
        else:
            incorrect += 1

        status = "PASS" if passed else "FAIL"

        print(f"\nTEST {i}")
        print(f"Query: {query}")
        if hasattr(classifier, "last_raw_output") and classifier.last_raw_output:
            print(f"Raw Output: [{classifier.last_raw_output}]")
        print(f"Expected: {expected}")
        print(f"Predicted: {predicted}")
        print(f"Status: {status}")

    accuracy = (correct / total_tests) * 100.0

    print("\n================ SUMMARY ================")
    print(f"Total Tests: {total_tests}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("==========================================")


if __name__ == "__main__":
    main()