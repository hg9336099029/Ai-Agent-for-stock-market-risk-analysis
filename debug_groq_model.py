
import os
import sys

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

print(f"GROQ_MODEL env var: {os.getenv('GROQ_MODEL')}")

from app.ai.explanation import generate_with_groq
import inspect
print(inspect.getsource(generate_with_groq))
