import json
import os

from django.http import JsonResponse
from dotenv import load_dotenv
from sasctl import Session
from sasctl.services import microanalytic_score as mas

load_dotenv()  # loads the configs from .env

SERVER = str(os.getenv("SERVER"))
USERNAME = str(os.getenv("USERNAME"))
PASSWORD = str(os.getenv("PASSWORD"))
CERTIFICATE = str(os.getenv("CERTIFICATE"))

print(SERVER, USERNAME, PASSWORD, CERTIFICATE)


def score_data(data, module_name):
    with Session(SERVER, USERNAME, PASSWORD, verify_ssl=CERTIFICATE) as session:
        result = mas.execute_module_step(module_name, "score", **data)
        return result
