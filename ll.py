import os
import google.generativeai as genai

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

print("--- 🔍 Modelos Disponibles para tu API Key ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"ID: {m.name} | Display Name: {m.display_name}")
except Exception as e:
    print(f"❌ Error: {e}")
