from dotenv import load_dotenv
import os

load_dotenv()  # lädt .env Datei

api_key = os.getenv("OMDB_API_KEY")

print(api_key)  # nur zum testen