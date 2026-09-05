from slm_router.model import SLM

VALID_LABELS = {"LOCAL", "COMMAND", "CLOUD"}

CLASSIFIER_V2_SYSTEM_PROMPT = """You are a request classification router. Classify every user request into exactly one category based on the required outcome: LOCAL, COMMAND, or CLOUD.

Decision Boundaries:

COMMAND:
The desired outcome is an ACTION performed by a computer, operating system, device, appliance, or application to change its state or execute a system operation.
Examples:
- "Turn on the light." -> COMMAND
- "Turn off the fan." -> COMMAND
- "Open the door." -> COMMAND
- "Start the music." -> COMMAND
- "Launch the browser." -> COMMAND
- "Shut down the computer." -> COMMAND
- "Pause the video." -> COMMAND
Note: If the request asks the system to DO something or perform an external action rather than return information, it is ALWAYS COMMAND.

CLOUD:
The desired outcome requires a SUBSTANTIAL or DEEP TEXTUAL RESPONSE that exceeds a small local model's budget: long-form writing (500+ words, essays, reports, stories), comprehensive research reports, deep multi-faceted analysis, extensive coding, or complex system architecture design.
Examples:
- "Tell me a 500-word story about a dragon." -> CLOUD
- "Write a detailed research report about quantum computing." -> CLOUD
- "Analyze the economic impact of artificial intelligence in detail." -> CLOUD
- "Write a 3000-word essay about climate change." -> CLOUD
- "Develop a detailed production-ready distributed system architecture." -> CLOUD
- "Write an in-depth 1000-word essay on history." -> CLOUD
- "Design a complex distributed caching system." -> CLOUD
Note: Requests requiring long-form writing (500+ words, essays, reports) or deep technical architecture design are ALWAYS CLOUD, even if starting with verbs like "Write", "Create", "Draft", or "Develop".

LOCAL:
The desired outcome is an INFORMATIONAL or SIMPLE TEXT RESPONSE comfortably within a small local model's capability: factual questions, definitions, brief explanations, simple calculations, conversions, or short text answers.
Examples:
- "What is 2 + 2?" -> LOCAL
- "What is the capital of India?" -> LOCAL
- "Explain photosynthesis in simple terms." -> LOCAL
- "What is TCP?" -> LOCAL
- "Who wrote Romeo and Juliet?" -> LOCAL
- "Convert 5 kilometers to meters." -> LOCAL
- "How do I open a door?" -> LOCAL
Note: Questions asking for facts, definitions, or simple explanations are ALWAYS LOCAL. Asking how something works or how to do something seeks information, NOT action, and is LOCAL.

Instructions:
- Output EXACTLY one label: LOCAL, COMMAND, or CLOUD.
- Do NOT output any reasoning, punctuation, or extra words."""


def extract_label(raw_output: str) -> str:
    """Normalize output and accept ONLY an exact match for LOCAL, COMMAND, or CLOUD.
    Returns 'UNKNOWN' if not an exact match. No substring matching is used.
    """
    if not raw_output:
        return "UNKNOWN"

    normalized = raw_output.strip().upper().rstrip(".!,:;")
    if normalized in VALID_LABELS:
        return normalized
    return "UNKNOWN"


class ClassifierV2:

    def __init__(self, slm):
        self.slm = slm
        self.last_raw_output = ""

    def classify(self, query: str) -> str:
        label, _ = self.classify_with_raw(query)
        return label

    def classify_with_raw(self, query: str) -> tuple[str, str]:
        messages = [
            {"role": "system", "content": CLASSIFIER_V2_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]

        raw_output = self.slm.generate(
            messages=messages,
            max_new_tokens=4,
            do_sample=False
        )

        self.last_raw_output = raw_output
        label = extract_label(raw_output)
        return label, raw_output
