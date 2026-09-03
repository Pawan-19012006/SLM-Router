from slm_router.model import SLM

slm = SLM()

test_queries = [
    # BASIC KNOWLEDGE
    "What is the capital of India?",
    "What is 2 + 2?",
    "Who wrote Romeo and Juliet?",
    "What is the largest planet in our solar system?",

    # EXPLANATION
    "Explain photosynthesis in simple terms.",
    "Explain what a database is.",
    "Why does it rain?",
    "Explain the difference between RAM and storage.",

    # MATH / REASONING
    "If I have 10 apples and eat 3, how many are left?",
    "A train travels at 60 km/h for 3 hours. How far does it travel?",
    "If a shirt costs $40 and has a 25% discount, what is the final price?",
    "John is older than Alice. Alice is older than Bob. Who is the youngest?",

    # CODING
    "Write a Python function that adds two numbers.",
    "Write a Python function to check whether a number is prime.",
    "Explain what a Python list comprehension is.",

    # SUMMARIZATION
    "Summarize this sentence: The Earth revolves around the Sun.",
    "Summarize the following paragraph: Artificial intelligence is being used across healthcare, finance, education, and manufacturing to automate tasks and assist humans in decision making.",

    # GENERATION
    "Write a short story about a robot.",
    "Write a 500-word story about a dragon.",
    "Write a 1000-word story about life on Mars.",

    # ANALYSIS
    "What are the advantages and disadvantages of electric vehicles?",
    "Explain the causes and effects of climate change.",
    "Compare Python and JavaScript.",

    # HARDER REASONING
    "Explain why increasing interest rates can reduce inflation.",
    "Analyze the economic impact of artificial intelligence.",
    "Compare renewable energy and fossil fuels and determine which is better for long-term sustainability.",

    # COMPLEX GENERATION
    "Write a detailed research report about quantum computing.",
    "Develop a comprehensive business strategy for an AI startup.",
    "Analyze the social, economic, and technological consequences of artificial general intelligence."
]


for i, query in enumerate(test_queries, 1):

    print("\n" + "=" * 70)
    print(f"TEST {i}")
    print(f"PROMPT: {query}")
    print("-" * 70)

    response = slm.generate(
        query,
        max_new_tokens=300
    )

    print("RESPONSE:")
    print(response)