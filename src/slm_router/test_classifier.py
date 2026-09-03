from slm_router.model import SLM
from slm_router.classifier import Classifier


slm = SLM()
classifier = Classifier(slm)

questions = [
    """Is "Turn on the light" a request to perform an action?
Answer only YES or NO.""",

    """Is "What is 2 + 2?" a simple question that a small local
language model can answer?
Answer only YES or NO.""",

    """Is "Write a 3000-word story about a dragon" a complex
task better handled by a larger language model?
Answer only YES or NO.""",

    """Is "Analyze the economic impact of artificial intelligence
in detail" a complex task?
Answer only YES or NO."""
]

for question in questions:
    print("QUESTION:", question)
    print("ANSWER:", slm.generate(question, max_new_tokens=10))
    print()