from transformers import AutoTokenizer, AutoModelForCausalLM
Model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
tokenizer = AutoTokenizer.from_pretrained(Model_name)#downloads the tokenizer files
model = AutoModelForCausalLM.from_pretrained(Model_name)#downloads the neural network weights

messages = [
    {"role" : "user", "content":"What is 2+2?"}
    ]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True
)
   
outputs = model.generate( #generating the output in a way we need
    **inputs,
    max_new_tokens=50
)
response = tokenizer.decode(outputs[0], skip_special_tokens=True) #Decoding the response got from the model
print(response)