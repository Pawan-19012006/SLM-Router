class IntentDetector:

    def __init__(self, slm):
        self.slm = slm

    def is_command(self, query):

        prompt = f"""Classify the user request into exactly one label.

COMMAND:
The user wants a computer, device, or system to perform an action.

NON-COMMAND:
The user is asking a question, requesting information,
asking for an explanation, asking for content, or asking for analysis.

Examples:

User: Turn on the light.
Label: COMMAND

User: Turn off the fan.
Label: COMMAND

User: Open the door.
Label: COMMAND

User: Start the music.
Label: COMMAND

User: What is 2 + 2?
Label: NON-COMMAND

User: What is the capital of India?
Label: NON-COMMAND

User: Explain photosynthesis.
Label: NON-COMMAND

User: Write a story about Mars.
Label: NON-COMMAND

User: Analyze the economic impact of artificial intelligence.
Label: NON-COMMAND

Now classify:

User: {query}

Label:"""

        result = self.slm.generate(
            prompt,
            max_new_tokens=5
        )

        print(f"  RAW SLM OUTPUT: [{result}]")

        answer = result.strip().upper()

        # Only accept an exact classification.
        first_line = answer.splitlines()[0].strip()
        first_line = first_line.rstrip(" .,:;")

        if first_line == "COMMAND":
            return True

        if first_line == "NON-COMMAND":
            return False

        # Unknown output -> fail safely.
        return False