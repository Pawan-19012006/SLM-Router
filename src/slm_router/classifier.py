from slm_router.model import SLM


class Classifier:

    def __init__(self, slm): #passing our already loaded slm into this class
        self.slm = slm

    def classify(self, query):

        prompt = f"""
You are a request classifier.

Classify the user's request into exactly ONE category:

LOCAL
COMMAND
CLOUD

LOCAL:
The user wants an answer, explanation, calculation, translation,
or other simple information that can be handled locally.

COMMAND:
The user wants the computer, device, or system to perform an action.
Examples include turning something on/off, opening/closing something,
starting/stopping something, or controlling a device.

CLOUD:
The user wants a complex task that requires a larger language model,
such as long-form writing, deep analysis, complex reasoning, or
large-scale generation.

Examples:

User: What is 2 + 2?
Category: LOCAL

User: What is the capital of India?
Category: LOCAL

User: Explain photosynthesis.
Category: LOCAL

User: Turn on the light.
Category: COMMAND

User: Turn off the light.
Category: COMMAND

User: Open the door.
Category: COMMAND

User: Close the door.
Category: COMMAND

User: Start the fan.
Category: COMMAND

User: Stop the fan.
Category: COMMAND

User: Write a 3000-word story about a dragon.
Category: CLOUD

User: Analyze the economic impact of artificial intelligence in detail.
Category: CLOUD

User: Write a detailed research report about quantum computing.
Category: CLOUD

IMPORTANT:
Return ONLY one word:
LOCAL
COMMAND
or
CLOUD

User: {query}

Category:
"""

        result = self.slm.generate(prompt, max_new_tokens=10)

        result = result.strip().upper()

        if "COMMAND" in result:
            return "COMMAND"
        elif "CLOUD" in result:
            return "CLOUD"
        elif "LOCAL" in result:
            return "LOCAL"
        else:
            return "CLOUD"