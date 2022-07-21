#If vs code doesn't chill with importing random stuff I'm going to lose it
from time import sleep
import requests
import config


#SENSITIVE DATA DO NOT SHARE!!!! 
CID = config.CID
CS = config.CS

#Less sensitive data
CHANNEL = "WhimsicalDragon1337"
 
def revokeToken(CID):
    global TOKEN

    #cleanup tokens
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",

    }


    data = "client_id=" + CID +"&token=" + TOKEN

    resp = requests.post("https://id.twitch.tv/oauth2/revoke", headers=headers, data=data)



    if resp.status_code != 200:
        print("Failed to revoke token:" + TOKEN)
        print(resp.status_code)
    else:
        print("Succesfully revoked:" + TOKEN)

def existCheck(CID,CS):
    global TOKEN

    headers = {
    'Authorization':"Bearer " + TOKEN,
    'Client-Id': CID,
    }

    r = requests.get('https://api.twitch.tv/helix/users?login=' + CHANNEL, headers=headers)

    if r.status_code == 401:
        
        #Reup token. retry and exit if still failing
        revokeToken(CID)
        genToken(CID,CS)

        r = requests.get('https://api.twitch.tv/helix/users?login=' + CHANNEL, headers=headers)
        if r.status_code == 401:
            print("Issue with token")
            revokeToken(CID)
            exit()

    

    elif r.status_code != 200:
        #idk what is wrong so quit
        print("Bad response: " + str(r.status_code))
        revokeToken(CID)
        exit()


    if (r.json()['data']) == [] :

        r = requests.get("https://passport.twitch.tv/usernames/" + CHANNEL)

        if r.text == '' and r.status_code == 204:
            print("I am very confident that that they do not exist!")
        else:
            print("I am pretty sure they don't exist.")

        return True #The specified channel does not exist!
    else:
        print("They still exist :(")
        return False #The specified channel does exist!


def genToken(CID,CS):
    global TOKEN
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
    }

    data = "client_id=" + CID +"&client_secret=" + CS + "&grant_type=client_credentials"

    resp = requests.post("https://id.twitch.tv/oauth2/token", headers=headers, data=data)

    print(resp.json())

    TOKEN = resp.json()["access_token"]
    return TOKEN

#End functions

global TOKEN
genToken(CID,CS)

existCheck(CID,CS)

while(existCheck(CID,CS) == False) :
    print("Rechecking in a half hour")
    sleep(1800)

    # Validation is not required since this is for an app
    #If we want to run this on a twitch account validation is required...
    """
    r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers) 

    if r.status_code == 401:
        #Reup and retry...
        genToken(CID,CS)
        r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
        if r.status_code == 401:
            print("Token cannot be validated. Exiting")
            revokeToken(CID)
            exit(1)
    """



revokeToken(CID)
