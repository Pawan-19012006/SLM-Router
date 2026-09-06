import torch
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


def get_default_device() -> torch.device:
    """Auto-detect CUDA, MPS, or fall back to CPU."""

    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


class SLM:
    def __init__(self, device: Optional[torch.device] = None):
        self.device = torch.device(device) if device is not None else get_default_device()
        print(f"Loading SLM on device: {self.device}...")

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        self.model.to(self.device)

        print(f"SLM loaded on {self.device}.")

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

        # Move all input tensors to the model's device
        inputs = {k: v.to(self.device) if hasattr(v, "to") else v for k, v in inputs.items()}

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