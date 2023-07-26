import os
from dotenv import load_dotenv
from storage_timeline_client import Storage

load_dotenv()

uri = os.getenv("STORAGE_TIMELINE_URI")

storage = Storage(uri)
schema = storage.schema("bsc.light-node.pancake.1000-pair")
time_line = schema.time_line("0x0018f45E3f088F5b088E020160Fd8d2bc91B4A8d")
all_documents = time_line.all_documents()
print(all_documents)
