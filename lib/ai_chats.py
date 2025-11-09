from openai import OpenAI
import random

class patient:
    def __init__(self, disaster, api_key, base_url, model, lang_id, lang):
        self.model = model
        self.lang = lang
        self.lang_id = lang_id
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.chatHistory = [
            {"role" : "system", "content" : "You are a patient, you have " + disaster[1]["en_name"] + ", please chat with me as a Medical consultation. You should act as a real patient, please response in " + lang + ". If I answer the correct disaster you have, please response me '$correct' directly without other things"},
            {"role" : "user", "content" : "Hello, Please describe your symptom"}
        ]

        print(self.chatHistory)

    def init(self):
        response = self.client.chat.completions.create(
            model = self.model,
            messages = self.chatHistory
        )

        self.chatHistory.append(response.choices[0].message)
        return response.choices[0].message

    def post(self, model, input, addHistory):
        self.chatHistory.append(
            {"role" : "user", "content" : input}
        )
        response = self.client.chat.completions.create(
            model = model,
            messages = self.chatHistory
        )

        if addHistory:
            self.chatHistory.append(response.choices[0].message)
        else:
            self.chatHistory.pop()

        #print(self.chatHistory)
        return response.choices[0].message

    def chat(self, input, addHistory):
        return self.post(self.model, input, addHistory)

class patientBuilder:
    def build(configs : dict, disasterData : dict):
        disasterList = disasterData.items()
        disaster = list(disasterList)[random.randint(0, len(list(disasterList)) - 1)]

        client = patient(disaster = disaster,
                         api_key = configs['API_KEY'] ,
                         base_url = configs['API_BASE_URL'],
                         model = configs['CHAT_MODEL'],
                         lang_id = configs['CHAT_LANGUAGE_ID'],
                         lang = configs['CHAT_LANGUAGE']
                         )

        return client

