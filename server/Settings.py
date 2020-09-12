from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
mongo_uri = os.getenv("MONGO_URI")