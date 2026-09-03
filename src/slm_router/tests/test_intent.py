from slm_router.model import SLM
from slm_router.intent import IntentDetector


slm = SLM()
intent_detector = IntentDetector(slm)


queries = [
    "Turn on the light.",
    "What is 2 + 2?",
]


for query in queries:
    result = intent_detector.is_command(query)

    print(
        f"{query} -> "
        f"{'COMMAND' if result else 'NON-COMMAND'}"
    )