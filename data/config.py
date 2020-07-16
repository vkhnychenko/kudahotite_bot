import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DB_HOST = str(os.getenv("DB_HOST"))
DB_NAME = str(os.getenv("DB_NAME"))

admins = [
    309275950
]

ip = os.getenv("ip")

