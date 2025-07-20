from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL_KEY=os.getenv("MONGODB_URL_KEY")
client = MongoClient(MONGODB_URL_KEY)

db = client["interview_db"]
resume_collection = db["resume"]