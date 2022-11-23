#If vs code doesn't chill with importing random stuff I'm going to lose it
from time import sleep
import requests
import config
import webhook


#SENSITIVE DATA DO NOT SHARE!!!! 
CID = config.CID
CS = config.CS

#Less sensitive data

CHANNELS = ["Miwu","Miumi"] #Put the channel names you want in here
CHANNELS_READABLE = " & ".join(CHANNELS)
CHANNELS = [x.lower() for x  in CHANNELS]
CHANNEL_REQ_LIST = ""

for i in CHANNELS:
    CHANNEL_REQ_LIST = CHANNEL_REQ_LIST + "login=" + i + "&"
CHANNEL_REQ_LIST = CHANNEL_REQ_LIST.rstrip(CHANNEL_REQ_LIST[-1]) #Get rid of trailling &


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

    print(CHANNEL_REQ_LIST)
    r = requests.get('https://api.twitch.tv/helix/users?' + CHANNEL_REQ_LIST, headers=headers)

    print(r.json())
    print(len(r.json()['data']))

    #raise Exception("Testing!")

    if r.status_code == 401:
        
        #Reup token. retry and exit if still failing
        revokeToken(CID)
        genToken(CID,CS)

        r = requests.get('https://api.twitch.tv/helix/users?login=' + CHANNEL_REQ_LIST, headers=headers)
        if r.status_code == 401:
            print("Issue with token")
            webhook.pushDiscordMessage("Issue with twitch token!")
            revokeToken(CID)
            exit()

    

    elif r.status_code != 200:
        #idk what is wrong so quit
        webhook.pushDiscordMessage("Something has gone terribly wrong, check the console output.")
        print("Bad response: " + str(r.status_code))
        revokeToken(CID)
        exit()


    if (len(r.json()['data'])) < len(CHANNELS) :

        CHECKCHANNELS = CHANNELS

        for i in (r.json()['data']):

            if i['login'] in CHECKCHANNELS:
                CHECKCHANNELS.remove(i['login'])
        print(CHECKCHANNELS)

        for i in CHECKCHANNELS:
            r = requests.get("https://passport.twitch.tv/usernames/" + i) #This request will ONLY accept 1 username at a time!!!

            if r.text == '' and r.status_code == 204:
                print("I am very confident that the name " +  i + " is not currently in use")
                webhook.pushDiscordMessage("<@User> I am very confident that the name " +  i + " is not currently in use!!!!!!!!!")
            else:
                print("I am pretty sure that the name " +  i + " is not currently in use")
                webhook.pushDiscordMessage("<@User> I am pretty sure that the name " +  i + " is not currently in use!!!")

        return True #A specified channel does not exist!
    else:
        print("They still exist :(")
        webhook.pushDiscordMessage("The names " + CHANNELS_READABLE + " are currently in use")
        return False #The specified channels do exist!


def validateToken():
    global TOKEN

    headers = {
    'Authorization': 'OAuth ' + TOKEN,
}

    r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers) 

    if r.status_code == 401:
        #Reup and retry...
        try:
            revokeToken(CID)
        except:
            print("Couldn't revoke token, likely because it is already invalid")
        genToken(CID,CS)
        r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)
        if r.status_code == 401:
            print("Token cannot be validated. Exiting.....")
            webhook.pushDiscordMessage("Issue with token validation.\nShutting down....")
            revokeToken(CID)
            exit(1)
    else:
        print("Validation succesful!")


def genToken(CID,CS):
    global TOKEN
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
    }

    data = "client_id=" + CID +"&client_secret=" + CS + "&grant_type=client_credentials"

    resp = requests.post("https://id.twitch.tv/oauth2/token", headers=headers, data=data)

    print(resp.json())

    TOKEN = resp.json()["access_token"]

    validateToken()

    return TOKEN

#End functions

global TOKEN
genToken(CID,CS)

#existCheck(CID,CS)

global checkCount
checkCount = 0

webhook.pushDiscordMessage("Startup: :white_check_mark:" + "\nƐ>--------------------------<3")
try:
    while(existCheck(CID,CS) == False) :
        checkCount = checkCount + 1
        print("Rechecking in a half hour")
        webhook.pushDiscordMessage("Rechecking in a half hour.\nCurrently checking the names: " + CHANNELS_READABLE + "\nTotal # of checks so far: " + str(checkCount) + "\nƐ>--------------------------<3")
        sleep(1800)
        #You can check more frequently than this if you want, but a half hour is really all that's needed.

        # Validation is not required since this is for an app
        #If we want to run this on a twitch account validation is required...
        validateToken()

    revokeToken(CID)

    webhook.pushDiscordMessage("Tokens revoked: :white_check_mark: \nShutting down....")
except:
    revokeToken(CID)

    webhook.pushDiscordMessage("Tokens revoked: :white_check_mark: \nShutting down....")