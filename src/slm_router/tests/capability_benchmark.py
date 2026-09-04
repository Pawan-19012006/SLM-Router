from slm_router.model import SLM
import json
import os


QUERIES = [

    # ============================================================
    # BASIC KNOWLEDGE
    # ============================================================

    {
        "id": 1,
        "category": "knowledge",
        "difficulty": "easy",
        "prompt": "What is the capital of France?"
    },
    {
        "id": 2,
        "category": "knowledge",
        "difficulty": "easy",
        "prompt": "What planet is known as the Red Planet?"
    },
    {
        "id": 3,
        "category": "knowledge",
        "difficulty": "easy",
        "prompt": "How many days are there in a week?"
    },
    {
        "id": 4,
        "category": "knowledge",
        "difficulty": "easy",
        "prompt": "What gas do humans need to breathe?"
    },
    {
        "id": 5,
        "category": "knowledge",
        "difficulty": "easy",
        "prompt": "Who wrote Romeo and Juliet?"
    },

    {
        "id": 6,
        "category": "knowledge",
        "difficulty": "medium",
        "prompt": "Why does the Moon appear to change shape during the month?"
    },
    {
        "id": 7,
        "category": "knowledge",
        "difficulty": "medium",
        "prompt": "What is the difference between RAM and storage?"
    },
    {
        "id": 8,
        "category": "knowledge",
        "difficulty": "medium",
        "prompt": "Explain what photosynthesis does."
    },
    {
        "id": 9,
        "category": "knowledge",
        "difficulty": "medium",
        "prompt": "Why does rain happen?"
    },
    {
        "id": 10,
        "category": "knowledge",
        "difficulty": "medium",
        "prompt": "What is a database?"
    },

    {
        "id": 11,
        "category": "knowledge",
        "difficulty": "hard",
        "prompt": "Explain the difference between supervised and unsupervised machine learning."
    },
    {
        "id": 12,
        "category": "knowledge",
        "difficulty": "hard",
        "prompt": "Explain how a CPU executes an instruction."
    },
    {
        "id": 13,
        "category": "knowledge",
        "difficulty": "hard",
        "prompt": "Explain the basic idea behind quantum computing."
    },
    {
        "id": 14,
        "category": "knowledge",
        "difficulty": "hard",
        "prompt": "Explain how TCP differs from UDP."
    },
    {
        "id": 15,
        "category": "knowledge",
        "difficulty": "hard",
        "prompt": "Explain how neural networks learn using gradient descent."
    },


    # ============================================================
    # EXPLANATION
    # ============================================================

    {
        "id": 16,
        "category": "explanation",
        "difficulty": "easy",
        "prompt": "Explain gravity in simple terms."
    },
    {
        "id": 17,
        "category": "explanation",
        "difficulty": "easy",
        "prompt": "Explain what an operating system does."
    },
    {
        "id": 18,
        "category": "explanation",
        "difficulty": "easy",
        "prompt": "Explain what an API is."
    },
    {
        "id": 19,
        "category": "explanation",
        "difficulty": "easy",
        "prompt": "Explain what a variable is in programming."
    },
    {
        "id": 20,
        "category": "explanation",
        "difficulty": "easy",
        "prompt": "Explain what the internet is."
    },

    {
        "id": 21,
        "category": "explanation",
        "difficulty": "medium",
        "prompt": "Explain how HTTPS protects a website connection."
    },
    {
        "id": 22,
        "category": "explanation",
        "difficulty": "medium",
        "prompt": "Explain how a database index improves query performance."
    },
    {
        "id": 23,
        "category": "explanation",
        "difficulty": "medium",
        "prompt": "Explain how a compiler converts source code into a program."
    },
    {
        "id": 24,
        "category": "explanation",
        "difficulty": "medium",
        "prompt": "Explain why machine learning models can overfit."
    },
    {
        "id": 25,
        "category": "explanation",
        "difficulty": "medium",
        "prompt": "Explain how public-key cryptography works."
    },

    {
        "id": 26,
        "category": "explanation",
        "difficulty": "hard",
        "prompt": "Explain the difference between processes and threads and when each is useful."
    },
    {
        "id": 27,
        "category": "explanation",
        "difficulty": "hard",
        "prompt": "Explain how transformers use attention to process text."
    },
    {
        "id": 28,
        "category": "explanation",
        "difficulty": "hard",
        "prompt": "Explain the CAP theorem and its implications for distributed databases."
    },
    {
        "id": 29,
        "category": "explanation",
        "difficulty": "hard",
        "prompt": "Explain why distributed systems are difficult to design."
    },
    {
        "id": 30,
        "category": "explanation",
        "difficulty": "hard",
        "prompt": "Explain the bias-variance tradeoff in machine learning."
    },


    # ============================================================
    # SIMPLE MATH
    # ============================================================

    {
        "id": 31,
        "category": "math",
        "difficulty": "easy",
        "prompt": "What is 2 + 2?"
    },
    {
        "id": 32,
        "category": "math",
        "difficulty": "easy",
        "prompt": "What is 15 multiplied by 4?"
    },
    {
        "id": 33,
        "category": "math",
        "difficulty": "easy",
        "prompt": "What is 100 divided by 5?"
    },
    {
        "id": 34,
        "category": "math",
        "difficulty": "easy",
        "prompt": "What is 25% of 200?"
    },
    {
        "id": 35,
        "category": "math",
        "difficulty": "easy",
        "prompt": "What is 17 + 28?"
    },

    {
        "id": 36,
        "category": "math",
        "difficulty": "medium",
        "prompt": "A shirt costs $80 and is discounted by 25%. What is the final price?"
    },
    {
        "id": 37,
        "category": "math",
        "difficulty": "medium",
        "prompt": "A train travels at 60 km/h for 2.5 hours. How far does it travel?"
    },
    {
        "id": 38,
        "category": "math",
        "difficulty": "medium",
        "prompt": "If 3 notebooks cost $12, how much do 7 notebooks cost?"
    },
    {
        "id": 39,
        "category": "math",
        "difficulty": "medium",
        "prompt": "What is the average of 12, 18, 25, and 29?"
    },
    {
        "id": 40,
        "category": "math",
        "difficulty": "medium",
        "prompt": "If a number is increased from 80 to 100, what is the percentage increase?"
    },

    {
        "id": 41,
        "category": "math",
        "difficulty": "hard",
        "prompt": "A shop increases a product price by 20% and then gives a 20% discount. Is the final price the same as the original? Explain."
    },
    {
        "id": 42,
        "category": "math",
        "difficulty": "hard",
        "prompt": "If x + 7 = 19 and 2y = x, what is y?"
    },
    {
        "id": 43,
        "category": "math",
        "difficulty": "hard",
        "prompt": "A car travels half a journey at 40 km/h and the other half at 60 km/h. What is its average speed?"
    },
    {
        "id": 44,
        "category": "math",
        "difficulty": "hard",
        "prompt": "If 5 workers complete a task in 12 days at the same rate, how many days would 10 workers need?"
    },
    {
        "id": 45,
        "category": "math",
        "difficulty": "hard",
        "prompt": "A number is multiplied by 3, then 5 is added, producing 26. What was the original number?"
    },


    # ============================================================
    # REASONING
    # ============================================================

    {
        "id": 46,
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "John is older than Alice. Alice is older than Bob. Who is youngest?"
    },
    {
        "id": 47,
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "If today is Monday, what day will it be two days from now?"
    },
    {
        "id": 48,
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "All cats are animals. Milo is a cat. Is Milo an animal?"
    },
    {
        "id": 49,
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "If A is taller than B and B is taller than C, who is shortest?"
    },
    {
        "id": 50,
        "category": "reasoning",
        "difficulty": "easy",
        "prompt": "If a box contains 3 red balls and 2 blue balls, how many balls are there?"
    },

    {
        "id": 51,
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "Tom is faster than Sam. Sam is faster than Raj. Raj is faster than Leo. Who is second fastest?"
    },
    {
        "id": 52,
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "A is left of B. C is right of B. Which object is in the middle?"
    },
    {
        "id": 53,
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "If every engineer in a team knows Python, and Sarah is an engineer, what can we conclude about Sarah?"
    },
    {
        "id": 54,
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "A meeting starts at 2:30 PM and lasts 90 minutes. When does it end?"
    },
    {
        "id": 55,
        "category": "reasoning",
        "difficulty": "medium",
        "prompt": "There are 5 boxes. Each box contains 4 smaller boxes. How many boxes are inside the 5 large boxes?"
    },

    {
        "id": 56,
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "Three people—Alice, Bob, and Charlie—are standing in a line. Alice is not first. Bob is not last. Who could be first?"
    },
    {
        "id": 57,
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "If some programmers are musicians and all musicians are creative, can we conclude that some programmers are creative?"
    },
    {
        "id": 58,
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "A farmer has chickens and cows. There are 10 animals and 28 legs total. How many chickens and cows are there?"
    },
    {
        "id": 59,
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "Five people have different heights. A is taller than B, B is taller than C, D is taller than A, and E is shorter than C. Who is tallest?"
    },
    {
        "id": 60,
        "category": "reasoning",
        "difficulty": "hard",
        "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain."
    },


    # ============================================================
    # CODING
    # ============================================================

    {
        "id": 61,
        "category": "coding",
        "difficulty": "easy",
        "prompt": "Write a Python function that adds two numbers."
    },
    {
        "id": 62,
        "category": "coding",
        "difficulty": "easy",
        "prompt": "Write Python code to print numbers from 1 to 10."
    },
    {
        "id": 63,
        "category": "coding",
        "difficulty": "easy",
        "prompt": "How do you create a list in Python?"
    },
    {
        "id": 64,
        "category": "coding",
        "difficulty": "easy",
        "prompt": "Write a Python function that checks whether a number is even."
    },
    {
        "id": 65,
        "category": "coding",
        "difficulty": "easy",
        "prompt": "What is a Python dictionary?"
    },

    {
        "id": 66,
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python function that checks whether a number is prime."
    },
    {
        "id": 67,
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python program that counts how many vowels are in a string."
    },
    {
        "id": 68,
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python function that reverses a string without using slicing."
    },
    {
        "id": 69,
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Explain the difference between a Python list and tuple."
    },
    {
        "id": 70,
        "category": "coding",
        "difficulty": "medium",
        "prompt": "Write a Python function that finds the largest number in a list."
    },

    {
        "id": 71,
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Implement binary search in Python and explain its time complexity."
    },
    {
        "id": 72,
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Implement merge sort in Python and explain its time complexity."
    },
    {
        "id": 73,
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Design a Python LRU cache using an appropriate data structure."
    },
    {
        "id": 74,
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Write a Python program that reads a CSV file and calculates the average of a numeric column."
    },
    {
        "id": 75,
        "category": "coding",
        "difficulty": "hard",
        "prompt": "Explain the difference between asynchronous and synchronous programming in Python."
    },


    # ============================================================
    # SUMMARIZATION
    # ============================================================

    {
        "id": 76,
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize this sentence in one sentence: The cat slept on the sofa because it was tired."
    },
    {
        "id": 77,
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize this: Python is a popular programming language used for web development, data science, automation, and machine learning."
    },
    {
        "id": 78,
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize this: The meeting was postponed because several team members were unavailable."
    },
    {
        "id": 79,
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize: Exercise can improve physical fitness and mental well-being."
    },
    {
        "id": 80,
        "category": "summarization",
        "difficulty": "easy",
        "prompt": "Summarize: Solar panels convert sunlight into electricity."
    },

    {
        "id": 81,
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the main advantages and disadvantages of electric vehicles in 3 bullet points."
    },
    {
        "id": 82,
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the following paragraph in two sentences: Machine learning systems learn patterns from data and use those patterns to make predictions on new examples."
    },
    {
        "id": 83,
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the key differences between renewable and fossil energy sources."
    },
    {
        "id": 84,
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the main purpose of a database management system."
    },
    {
        "id": 85,
        "category": "summarization",
        "difficulty": "medium",
        "prompt": "Summarize the main causes and effects of climate change."
    },


    # ============================================================
    # COMPARISON
    # ============================================================

    {
        "id": 86,
        "category": "comparison",
        "difficulty": "easy",
        "prompt": "What is the difference between RAM and ROM?"
    },
    {
        "id": 87,
        "category": "comparison",
        "difficulty": "easy",
        "prompt": "What is the difference between a laptop and a desktop computer?"
    },
    {
        "id": 88,
        "category": "comparison",
        "difficulty": "easy",
        "prompt": "What is the difference between HTTP and HTTPS?"
    },
    {
        "id": 89,
        "category": "comparison",
        "difficulty": "easy",
        "prompt": "What is the difference between Python and JavaScript?"
    },
    {
        "id": 90,
        "category": "comparison",
        "difficulty": "easy",
        "prompt": "What is the difference between an SSD and an HDD?"
    },

    {
        "id": 91,
        "category": "comparison",
        "difficulty": "medium",
        "prompt": "Compare REST APIs and GraphQL."
    },
    {
        "id": 92,
        "category": "comparison",
        "difficulty": "medium",
        "prompt": "Compare SQL and NoSQL databases and explain when each is useful."
    },
    {
        "id": 93,
        "category": "comparison",
        "difficulty": "medium",
        "prompt": "Compare supervised and reinforcement learning."
    },
    {
        "id": 94,
        "category": "comparison",
        "difficulty": "medium",
        "prompt": "Compare monolithic and microservices architectures."
    },
    {
        "id": 95,
        "category": "comparison",
        "difficulty": "medium",
        "prompt": "Compare containers and virtual machines."
    },


    # ============================================================
    # ANALYSIS
    # ============================================================

    {
        "id": 96,
        "category": "analysis",
        "difficulty": "easy",
        "prompt": "What are two advantages of using solar energy?"
    },
    {
        "id": 97,
        "category": "analysis",
        "difficulty": "easy",
        "prompt": "What are the main benefits of exercise?"
    },
    {
        "id": 98,
        "category": "analysis",
        "difficulty": "easy",
        "prompt": "Why might someone choose a laptop instead of a desktop?"
    },
    {
        "id": 99,
        "category": "analysis",
        "difficulty": "easy",
        "prompt": "Why is data backup important?"
    },
    {
        "id": 100,
        "category": "analysis",
        "difficulty": "easy",
        "prompt": "Why is cybersecurity important for businesses?"
    },

    {
        "id": 101,
        "category": "analysis",
        "difficulty": "medium",
        "prompt": "Analyze the main advantages and disadvantages of electric vehicles."
    },
    {
        "id": 102,
        "category": "analysis",
        "difficulty": "medium",
        "prompt": "Explain why inflation can affect household spending."
    },
    {
        "id": 103,
        "category": "analysis",
        "difficulty": "medium",
        "prompt": "Analyze the main factors that affect software project success."
    },
    {
        "id": 104,
        "category": "analysis",
        "difficulty": "medium",
        "prompt": "Analyze the tradeoffs between cloud computing and on-device computing."
    },
    {
        "id": 105,
        "category": "analysis",
        "difficulty": "medium",
        "prompt": "Analyze why startups sometimes fail even when they have a good product."
    },


    # ============================================================
    # CREATIVE GENERATION
    # ============================================================

    {
        "id": 106,
        "category": "creative",
        "difficulty": "easy",
        "prompt": "Write a short story about a robot learning to cook."
    },
    {
        "id": 107,
        "category": "creative",
        "difficulty": "easy",
        "prompt": "Write a short poem about the ocean."
    },
    {
        "id": 108,
        "category": "creative",
        "difficulty": "easy",
        "prompt": "Create five creative names for a technology startup."
    },
    {
        "id": 109,
        "category": "creative",
        "difficulty": "easy",
        "prompt": "Write a short motivational paragraph for a student."
    },
    {
        "id": 110,
        "category": "creative",
        "difficulty": "easy",
        "prompt": "Create a short dialogue between a student and a teacher."
    },

    {
        "id": 111,
        "category": "creative",
        "difficulty": "medium",
        "prompt": "Write a 300-word science-fiction story about humans living on Mars."
    },
    {
        "id": 112,
        "category": "creative",
        "difficulty": "medium",
        "prompt": "Write a 500-word story about a dragon that cannot breathe fire."
    },
    {
        "id": 113,
        "category": "creative",
        "difficulty": "medium",
        "prompt": "Write a detailed fictional conversation between two astronauts."
    },
    {
        "id": 114,
        "category": "creative",
        "difficulty": "medium",
        "prompt": "Write a story with three characters where the ending contains a surprising twist."
    },
    {
        "id": 115,
        "category": "creative",
        "difficulty": "medium",
        "prompt": "Write a 500-word mystery story set in a university."
    },


    # ============================================================
    # LONG / COMPLEX GENERATION
    # ============================================================

    {
        "id": 116,
        "category": "complex_generation",
        "difficulty": "hard",
        "prompt": "Write a detailed 1000-word story about humans establishing the first colony on Mars."
    },
    {
        "id": 117,
        "category": "complex_generation",
        "difficulty": "hard",
        "prompt": "Write a detailed research-style report explaining the future of quantum computing."
    },
    {
        "id": 118,
        "category": "complex_generation",
        "difficulty": "hard",
        "prompt": "Write a detailed analysis of how artificial intelligence could affect the global economy."
    },
    {
        "id": 119,
        "category": "complex_generation",
        "difficulty": "hard",
        "prompt": "Develop a detailed business strategy for an AI startup entering a competitive market."
    },
    {
        "id": 120,
        "category": "complex_generation",
        "difficulty": "hard",
        "prompt": "Explain the possible technological, economic, and social consequences of achieving artificial general intelligence."
    }
]


def main():

    print("Loading SmolLM2...")
    slm = SLM()

    os.makedirs("data", exist_ok=True)

    output_file = "data/capability_dataset.jsonl"

    with open(output_file, "w", encoding="utf-8") as f:

        for item in QUERIES:

            print("\n" + "=" * 80)
            print(f"TEST {item['id']}")
            print(f"Category: {item['category']}")
            print(f"Difficulty: {item['difficulty']}")
            print(f"Prompt: {item['prompt']}")
            print("-" * 80)

            response = slm.generate(
                item["prompt"],
                max_new_tokens=250
            )

            print("Response:")
            print(response)

            record = {
                **item,
                "response": response
            }

            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()

    print("\nBenchmark complete.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()