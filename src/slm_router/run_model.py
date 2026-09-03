from transformers import AutoTokenizer, AutoModelForCausalLM
Model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
tokenizer = AutoTokenizer.from_pretrained(Model_name)#downloads the tokenizer files
model = AutoModelForCausalLM.from_pretrained(Model_name)#downloads the neural network weights

print("Model loaded successfully!")