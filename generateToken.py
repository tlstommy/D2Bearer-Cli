import requests,json,urllib.request
from os import system, name
from requests.structures import CaseInsensitiveDict

def clearConsole():
    #if on windows
    if name == "nt":
        system("cls")
    #on a diffrent system
    else:
        system("clear")



class main:
    def __init__(self,clientID,clientSecret):
        self.apiUrl = "https://www.bungie.net/Platform/App/OAuth/Token/"
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.oAuthCode = None
        self.apiJsonResponse = None
        self.bearerToken = None

    def genAuthURL(self):
        print("\nPlease open this link in a browser and sign in to your Bungie account.")
        print(f"https://www.bungie.net/en/OAuth/Authorize?client_id={self.clientID}&response_type=code")
        print("\n\nWhen you have done that, please paste the redirected Url below.")
        self.processRedirectURL(input("Redirected url: "))

    def processRedirectURL(self,redirectURL):
        self.oAuthCode = redirectURL.split("code=")[-1]
        print(f"\n[OAuth Code] {self.oAuthCode}")
        self.grabNewBearerToken()
    
    def grabNewBearerToken(self):
        
        #format the oAuthDataString with client id and secret and append the oauth code
        oAuthDataString = f"client_id={self.clientID}&client_secret={self.clientSecret}&Authorization%3A%20Basic%20%7Bbase64encoded(client-id%3Aclient-secret)%7D=&Content-Type%3A%20application%2Fx-www-form-urlencoded=&grant_type=authorization_code&code={self.oAuthCode}"

        #setup headers content type
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        #send a POST request to the api 
        resp = requests.post(self.apiUrl, headers=headers, data=oAuthDataString)

        #pull out the access token
        self.apiJsonResponse = jsonResponse = json.loads(resp.content)
        self.bearerToken = jsonResponse["access_token"]
        self.tokenOutput()
    def tokenOutput(self):
        clearConsole()
        print(f"[Full API JSON Response]\n{self.apiJsonResponse}\n\n[Bearer Token]\n{self.bearerToken}\n")

        while True:
            userInput = input("Would you like to save the bearer token to a textfile in the current directory? (Y/n)")
            if userInput == "Y":
                self.saveToFile()
                break
            elif userInput == "n":
                break
            else:
                print("\nInvalid option! Please enter 'Y' or 'n'\n")

 


    def saveToFile(self):
        with open('bearer_token.txt', 'w') as f:
            f.write(self.bearerToken)
            f.close()


clearConsole()
print("Welcome to D2Bearer-Cli!\n\n\nThis tool provides and easy and secure way to generate a bearer token for Bungie.net's Destiny 2 api.\n\nYou can access the Bungie developer portal here: https://www.bungie.net/en/Application")
print("\n\nTo begin please enter your applications client ID and secret below. These can be found under you application as \"OAuth client_id\" and \"OAuth client_secret\" respectively\n")

cliID = input("Client ID:{:5}".format(" "))

cliSecret = input("\nClient Secret: ")

clearConsole()
print("[Client ID]{:7}{cliID}".format(" ",cliID=cliID))
print("[Client Secret]{:3}{cliSecret}".format(" ",cliSecret=cliSecret))



Generator = main(cliID,cliSecret)

Generator.genAuthURL()

print("Thank you for using D2Bearer-Cli!")