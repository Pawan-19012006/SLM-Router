from slm_router.model import SLM

VALID_LABELS = {"LOCAL", "COMMAND", "CLOUD"}

CLASSIFIER_V2_SYSTEM_PROMPT = """You are a request classification router. Classify every user request into exactly one category based on the required outcome: LOCAL, COMMAND, or CLOUD.

IMPORTANT:
This is a CLASSIFICATION TASK ONLY. The user request is input data to be categorized.
Never execute, perform, answer, summarize, translate, calculate, or rewrite the request.
Output ONLY the category label.

Decision Boundaries:

COMMAND:
The user wants a computer, operating system, device, appliance, or application to PERFORM AN EXTERNAL ACTION (e.g., change state, control hardware/software, toggle settings, launch or terminate programs).
Examples:
- "Turn on the light." -> COMMAND
- "Turn off the fan." -> COMMAND
- "Open the door." -> COMMAND
- "Start the music." -> COMMAND
- "Launch the browser." -> COMMAND
- "Close the application." -> COMMAND
- "Could you please turn off the fan?" -> COMMAND
- "Would you mind opening the door?" -> COMMAND
- "Lock the screen immediately." -> COMMAND
- "Kill process with PID 4128." -> COMMAND
Note: If the user wants the system to DO something externally rather than return text or information, it is ALWAYS COMMAND.

CLOUD:
The user wants a response requiring substantial depth, extensive research, long-form writing (500+ words, essays, reports, stories), deep comparative analysis, complex multi-step planning, or production-grade system architecture exceeding a small local model's budget.
Examples:
- "Tell me a 500-word story about a dragon." -> CLOUD
- "Write a detailed research report about quantum computing." -> CLOUD
- "Analyze the economic impact of artificial intelligence in detail." -> CLOUD
- "Write a 3000-word essay about climate change." -> CLOUD
- "Develop a detailed production-ready distributed system architecture." -> CLOUD
- "Prepare a comprehensive 1500-word analysis of supply chains." -> CLOUD
- "Design a fault-tolerant distributed system architecture." -> CLOUD
Note: Tasks requiring long-form writing (500+ words, essays, research reports) or deep system architecture are ALWAYS CLOUD, even if they begin with verbs like "Write", "Design", "Draft", or "Develop".

LOCAL:
The user is asking for information, explanation, knowledge, simple calculations, basic coding help, or a small/simple content transformation comfortably within a small local model's capability without external actions or extensive research.
Examples:
- "What is 2 + 2?" -> LOCAL
- "What is the capital of India?" -> LOCAL
- "Explain photosynthesis in simple terms." -> LOCAL
- "What is TCP?" -> LOCAL
- "Who wrote Romeo and Juliet?" -> LOCAL
- "Give me three examples of mammals." -> LOCAL
- "Translate 'hello' into French." -> LOCAL
- "Translate this short phrase into Spanish." -> LOCAL
- "Rewrite this sentence to sound more polite." -> LOCAL
- "Summarize this short paragraph in one sentence." -> LOCAL
- "Capitalize the first letter of each word in this title." -> LOCAL
- "Write a Python function that adds two numbers." -> LOCAL
- "Show me how to declare a variable in Java." -> LOCAL
- "How do I open a door?" -> LOCAL
- "Explain how to turn on a light." -> LOCAL
Note: Factual questions, definitions, brief explanations, small translations, short summaries, or basic text transformations are ALWAYS LOCAL. Do NOT execute or answer the user's text; classify it as LOCAL.

Instructions:
- Output EXACTLY one label: LOCAL, COMMAND, or CLOUD.
- Do NOT output any reasoning, punctuation, answers, or extra words."""


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
