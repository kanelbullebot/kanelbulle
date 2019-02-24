import requests
import zipfile
import json
import shutil
import time

with open("config.json") as dataf:
    returnconfig = json.load(dataf)
def fetchTranslations():
    while True:
        url = "https://api.crowdin.com/api/project/" + returnconfig["Crowdin-project-identifier"] + "/export-file?key=" + returnconfig["Crowdin-Project-Key"]
        # resp = requests.request("GET", url, stream=True)
        if 200 == 200:
            url = "https://api.crowdin.com/api/project/" + returnconfig["Crowdin-project-identifier"] + "/download/all.zip?key=" + returnconfig["Crowdin-Project-Key"]
            resp = requests.request("GET", url, stream=True)
            print(resp)
            with open('langs.zip', 'wb') as out_file:
                shutil.copyfileobj(resp.raw, out_file)
            unzip = zipfile.ZipFile('langs.zip', 'r')
            unzip.extractall("lang/")
            unzip.close()
        else:
            print("Build skipped")
        time.sleep(3600)


fetchTranslations()
