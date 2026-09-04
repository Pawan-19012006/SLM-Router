from slm_router.model import SLM

VALID_LABELS = {"LOCAL", "COMMAND", "CLOUD"}

CLASSIFIER_SYSTEM_PROMPT = """You are a request classification router. Classify every user request into exactly one category: LOCAL, COMMAND, or CLOUD.

Decision Boundaries:

COMMAND:
Requests that ask the system, computer, device, appliance, or application to PERFORM AN ACTION.
This includes operations such as: turn on/off, open, close, start, stop, launch, play, pause, increase, decrease, shut down.
Examples:
- "Turn on the light." -> COMMAND
- "Turn off the fan." -> COMMAND
- "Open the door." -> COMMAND
- "Start the music." -> COMMAND
- "Launch the browser." -> COMMAND
Note: Controlling any physical device, light, fan, door, audio, or application is ALWAYS COMMAND.

CLOUD:
Tasks requiring substantial generation, deep analysis, detailed research, long-form writing, complex planning, extensive coding, or production-grade architecture.
Examples:
- "Tell me a 500-word story about a dragon." -> CLOUD
- "Write a detailed research report about quantum computing." -> CLOUD
- "Analyze the economic impact of artificial intelligence in detail." -> CLOUD
- "Write a 3000-word essay about climate change." -> CLOUD
- "Develop a detailed production-ready distributed system architecture." -> CLOUD
Note: Writing stories, essays, reports, deep economic analyses, or designing software architectures is ALWAYS CLOUD, never COMMAND.

LOCAL:
Simple informational questions, factual questions, definitions, explanations, basic calculations, and simple tasks that a small local model can reasonably answer.
Examples:
- "What is 2 + 2?" -> LOCAL
- "What is the capital of India?" -> LOCAL
- "Explain photosynthesis in simple terms." -> LOCAL
- "What is TCP?" -> LOCAL
- "Who wrote Romeo and Juliet?" -> LOCAL
Note: Asking questions, definitions, facts, or short explanations is ALWAYS LOCAL.

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


class Classifier:

    def __init__(self, slm):
        self.slm = slm
        self.last_raw_output = ""

    def classify(self, query: str) -> str:
        label, _ = self.classify_with_raw(query)
        return label

    def classify_with_raw(self, query: str) -> tuple[str, str]:
        messages = [
            {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
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