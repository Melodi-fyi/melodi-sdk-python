from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify that required environment variables are set
required_vars = ['AZURE_API_KEY', 'AZURE_ENDPOINT']
for var in required_vars:
    if not os.getenv(var):
        print(f"Warning: {var} is not set in .env file")
