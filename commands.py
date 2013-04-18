#executable commands

def checkWeather(parameters):
    if len(parameters) > 0:
        import httplib
        import json
        cityName = parameters[0]
        connection = httplib.HTTPConnection("api.openweathermap.org")
        connection.request("GET", "/data/2.1/find/name?q=" + cityName + "&units=imperial")
        response = connection.getresponse()
        responseText = json.load(response)
        connection.close()
        return "Current Temp: " + str(round(responseText["list"][0]["main"]["temp"],1)) + " degrees Farenheit"
    else:
        return "Incorrect numbers of arguments." + "\r\n" + "checkWeather [City Name]"

def ls(parameters):
    if len(parameters) > 0:
        import subprocess
        directory = parameters[0]
        return subprocess.check_output('ls ' + directory, shell=True)
    else:
        return "Incorrect numbers of arguments." + "\r\n" + "ls [directory]"