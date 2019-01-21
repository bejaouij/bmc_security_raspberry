import json
import requests

BASE_API_URL = "http://localhost:100/bmc_security/public/api/"

def retrieveDeviceData(deviceSerialNunmber):
    requestUrl = BASE_API_URL + 'device/' + deviceSerialNunmber

    return json.loads(requests.get(requestUrl).text)