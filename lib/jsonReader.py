import json

def readJson(path):
    data = {}
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def connectStrings(list):
    p = ""
    for i in list:
        p = p + i
    return p

def search(json : dict, name):
    l = list(json.items())
    p = []
    for i in l:
        if name in i[1]['abbr'] or name in i[1]["en_name"] or name in i[1]["zh_name"]:
            p.append(i)

    return p
