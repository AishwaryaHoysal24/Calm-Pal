import google.generativeai as genai

# Paste your correct MakerSuite API key here
genai.configure(api_key="_________")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
