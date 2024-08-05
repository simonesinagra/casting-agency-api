from dotenv import load_dotenv 
import os 

load_dotenv()

DB_NAME = os.environ.get("DB_NAME") 
DB_USER=os.environ.get("DB_USER") 
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")

CASTING_ASSISTANT_TOKEN = os.getenv('CASTING_ASSISTANT_TOKEN')
CASTING_DIRECTOR_TOKEN = os.getenv('CASTING_DIRECTOR_TOKEN')
EXECUTIVE_PRODUCER_TOKEN = os.getenv('EXECUTIVE_PRODUCER_TOKEN')