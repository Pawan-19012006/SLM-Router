from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct" #model name from huggingface


class SLM:
    def __init__(self):
        print("Loading SLM...") #just a smaall loading template

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) #importing the tokenizer
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME) #importing the model

        print("SLM loaded.")

    def generate(self, prompt=None, messages=None, max_new_tokens=100, do_sample=False, **kwargs):
        if messages is None:
            if prompt is None:
                raise ValueError("Either prompt or messages must be provided.")
            messages = [
                {"role": "user", "content": prompt}
            ]

        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            **kwargs
        )

        input_length = inputs["input_ids"].shape[1]

        generated_tokens = outputs[0][input_length:]

        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return response.strip()