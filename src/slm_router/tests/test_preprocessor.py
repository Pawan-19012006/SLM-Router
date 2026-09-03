from slm_router.preprocessor import Preprocessor


preprocessor = Preprocessor()

tests = [
    "  Turn on the light  ",
    "What is 2 + 2?",
    "Write a detailed story about Mars.",
]

for query in tests:
    result = preprocessor.process(query)

    print("\nINPUT:", query)
    print("OUTPUT:", result)