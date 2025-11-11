from app.llm.openai_client import OpenAIClient

client = OpenAIClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello!"}
]

response = client.generate_response(messages)
print("OpenAI Response:", response)