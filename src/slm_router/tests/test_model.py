from slm_router.model import SLM #class slm

slm = SLM()
response = slm.generate("What is 2+2?")
print("Response:", response)