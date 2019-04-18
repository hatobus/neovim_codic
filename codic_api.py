import requests
import json
import os


class Codic():
    def __init__(self, dictid=None):
        self.Dictionary_ID = dictid
        self.URLHOST = "https://api.codic.jp"
        self.ACCESSTOKEN = os.getenv("CODIC_API_TOKEN")
        self.HEADER = {"Authorization": "Bearer "+self.ACCESSTOKEN}
        self.Casing = ["camel", "pascal", "lower underscore", "upper underscore", "hyphen"]


    def Translate(self, srcstr):
        PATH = "/v1/engine/translate.json"

        translated = {"original": srcstr}
        for cast in self.Casing:
            params = {
                "text": srcstr,
                "project_id": self.Dictionary_ID,
                "casing": cast
            }
            resp = requests.get(self.URLHOST + PATH, params=params, headers=self.HEADER)

            resjson = resp.json()
            translated[cast] = resjson[0]["translated_text"]

        return translated


    def GetDictID(self):
        PATH = "/v1/user_projects.json"
        resp = requests.get(self.URLHOST + PATH, headers=self.HEADER)
        resjson = resp.json()

        pjname = {rj["id"]:rj["name"] for rj in resjson}
        
        return pjname


    def GetProject(self, pjid):
        PATH = "/v1/user_projects/" + pjid + ".json"
        
        resp = requests.get(self.URLHOST + PATH, headers=self.HEADER)
        resjson = resp.json()

        return resjson


if __name__ == "__main__":
    CD = Codic()
    dic = CD.GetDictID()
    print(dic)
    print(CD.Translate("こんにちは世界"))
    key = dic.keys()
    for k in key:
        print(CD.GetProject(str(k)))