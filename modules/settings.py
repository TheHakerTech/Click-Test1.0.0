# -*- coding: utf-8 -*-
import json
def loadSettings(settingsPath='data/settings.json'):
    with open(settingsPath, 'r', encoding='utf-8') as settingsFile:
        rawJson = settingsFile.read()
    return json.loads(rawJson)

def writeSettings(settings: dict, settingsPath='data/settings.json'):
    with open(settingsPath, 'w', encoding='utf-8') as settingsFile:
        settingsFile.write(json.dumps(settings, skipkeys=True))

def resetSettings(settingsPath='data/settings.json', defSettingsPath='data/default-settings.json'):
    with open(defSettingsPath, 'r', encoding='utf-8') as defSettingsFile:
        rawJson = defSettingsFile.read()
        with open(settingsPath, 'w', encoding='utf-8') as settingsFile:
            settingsFile.write(rawJson)