import cli
import requests
import json
import sys
import os
import mytokens

#  Function for passing a message to the WebEx Teams 


def send_it(token, room_id, message):
    header = {"Authorization": "Bearer %s" % token,
              "Content-Type": "application/json"}
    data = {"roomId": room_id,
            "text": message} 
    
    http_proxy = mytokens.http_proxy
    proxyDict = { 
                "http"  : http_proxy
               }
   
   #return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, data=json.dumps(data), verify=True)
   return requests.post("https://api.ciscospark.com/v1/messages/", headers=header, proxies=proxyDict, data=json.dumps(data), verify=True)

# Post mesages to WebEx Teams 
def post(message):
    res = send_it(token, teams_room, message)
    if res.status_code == 200:
        print("your message was successfully posted to Webex Teams")
    else:
        print("failed with statusCode: %d" % res.status_code)
        if res.status_code == 404:
            print ("please check the bot is in the room you're attempting to post to...")
        elif res.status_code == 400:
            print ("please check the identifier of the room you're attempting to post to...")
        elif res.status_code == 401:
            print ("please check if the access token is correct...")


if __name__ == '__main__':

    access_token = mytokens.access_token
    teams_room = mytokens.teams_room

    # Check access token
    teams_access_token = os.environ.get("TEAMS_ACCESS_TOKEN")
    token = access_token if access_token else teams_access_token
    if not token:
        error_message = "You must provide a Webex Teams API access token."
        print(error_message)
        sys.exit(2)


    # The sandbox doesn't have startup config and blocks you from create it, so just get a running config
    #create baseline config file if none exist
    if os.path.isfile("startup.cfg") == False:
        startCfg = cli.execute("show run")
        with open("startup.cfg", "w") as f:
            f.write(startCfg)

    #write current running config to file
    runCfg = cli.execute("show run")
    with open("running.cfg", "w") as f:
        f.write(runCfg)

    #diff the files
    #diffCfg = os.popen("diff startup.cfg running.cfg")
    diffCfg = os.popen("sdiff -l startup.cfg running.cfg | cat -n | grep -v -e '($'")
    diff = diffCfg.read()

    #post the diff as a message to the webex team's room
    post("Diff between baseline config and current running-config. \n\n" + diff)
