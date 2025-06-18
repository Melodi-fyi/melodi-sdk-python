import os
import sys

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("MELODI_PROJECT_ID", "12074")
try:
    from melodi.utils.openai import AzureOpenAI
except ImportError as e:
    print("Melodi not installed:", e)
    sys.exit(1)
client = AzureOpenAI(
    api_key=os.getenv("AZURE"),
    api_version="2025-03-01-preview",
    azure_endpoint="https://melodi.openai.azure.com/",
)
try:
    response = client.responses.create(
        model="gpt-4.1-mini", input="This is on the responses api with a longer message"
    )
    print("Response text:", response.output_text)
except Exception as e:
    print("Error while calling API:", e)
