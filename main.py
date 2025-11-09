import os
import json
import sys
from lib.ai_chats import *
from lib.jsonReader import *
from lib.med_sys.medExmSys import *

config_path = "./config.txt"
disaster_path = "lib/jsonDatas/disasters/disaster.json"
medExamination_path = "lib/jsonDatas/medicalExamination/examinations.json"

def readInfo():
    configs = {}
    with open(config_path, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            configText = line.replace("$","").replace("\n","").split(" ")
            if len(configText) == 2:
                configs[configText[0]] = configText[1]
            else:
                print("the key of " + configText[0] + " is empty!")
                sys.exit()
            line = file.readline()

        return configs

if __name__ == "__main__":
    print("loading the configs and datas")
    print("trying to read the configs...")
    configs = readInfo() #Read the configs from config file
    langID = configs['CHAT_LANGUAGE_ID']
    disasters = readJson(disaster_path)
    examinationConfigs = readJson(medExamination_path) #Read the configs of examination from the json

    print("Read datas successful!")
    #init the chat model
    print("trying to start...")
    client = patientBuilder.build(configs=configs, disasterData=disasters)
    medExamSys = medExmSys()
    firstCommunication = client.init()

    print("Welcome... \n \n")
    print("patient >" , firstCommunication.content)
    #init

    #main thread
    while True:
        inputs = input("you > ")

        if inputs == "$post":
            medExamSys.post(client)
            medExamSys.clear()
            continue
        elif inputs.startswith("$tc"):
            tcs = inputs.split(" ")[1]
            searchResponse = search(json = examinationConfigs, name = tcs)
            if searchResponse == []:
                print("Sorry, we didn't find any thing that you probably needs")
                continue
            else:
                print("-----\t the all checks \t-----")
                for i in range(len(searchResponse)):
                    print(str(int(i)) + " : " + searchResponse[i][1][langID + '_name'])

                action = searchResponse[int(input("Please choice id>"))]
                #medExamSys.add(connectStrings(action[1]['chat_prompt']))
                medExamSys.add(action)
                continue

        response = client.chat(inputs, addHistory = True).content
        if response == "$correct":
            print("You win!")
            break
        else:
            print("patient > " + response)

