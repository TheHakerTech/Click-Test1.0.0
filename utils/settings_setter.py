import json
from typing import Any

settingsPath = 'settings.json'

def loadSettings() -> dict:
    with open(settingsPath, 'r', encoding='utf-8') as settingsFile:
        rawJson = settingsFile.read()
    return json.loads(rawJson)

def getSetting(name: str) -> Any:
    d = loadSettings()
    return d[name]

def writeSettings(settings: dict):
    with open(settingsPath, 'w', encoding='utf-8') as settingsFile:
        settingsFile.write(json.dumps(settings, skipkeys=True))

def changeSetting(name: str, value: Any) -> dict:
    d = loadSettings()
    d[name] = value
    writeSettings(d)
    return d
