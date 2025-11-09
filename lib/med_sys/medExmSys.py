from openai import *
from lib.jsonReader import *

class medExmSys:
    def __init__(self):
        self.checks = []

    def add(self, t : dict):
        self.checks.append(t)

    def post(self, client):
        print("The all examination you post")
        for p in self.checks:
            print(p[1][client.lang_id + "_name"])

        print("\nThe result of them:")
        for p in self.checks:
            print(p[1][client.lang_id + "_name"]  + "\n" + client.chat(connectStrings(p[1]['chat_prompt']), addHistory=False).content + "\n")

    def clear(self):
        self.checks = []