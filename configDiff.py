import cli
import requests
import json
import sys
import os
import mytokens

clients = {}

# webhooks
clients['WebEx'] = {
    "url": mytokens.webex_webhook_url,
    "headers": {"Content-Type": "application/json"},
    "data": {"text": ""}
}

clients['Slack'] = {
    "url": mytokens.slack_webhook_url,
    "headers": {"Content-Type": "application/json"},
    "data": {"text": ""}
}

clients['Microsoft Teams'] = {
    "url": mytokens.microsoft_webhook_url,
    "headers": {"Content-Type": "application/json"},
    "data": {"text": ""}
}

'''
# example if you don't plan to use webhooks
clients['WebEx Teams'] = {
    "url": "https://api.ciscospark.com/v1/messages/",
    "headers": {"Authorization": "Bearer %s" % mytokens.access_token, "Content-Type": "application/json"},
    "data": {"roomId": mytokens.teams_room, "text": ""}
}
'''

use_proxy = True

http_proxy = mytokens.http_proxy
proxyDict = {
    "http"  : http_proxy
}

# Function for posting the message to the collaboration client
def post(message):

    for key, value in clients.items():
        clients[key]["data"]["text"] = message

        if use_proxy:
            response = requests.post(clients[key]["url"], \
            headers=clients[key]["headers"], \
            proxies=proxyDict, \
            data=json.dumps(clients[key]["data"]), \
            verify=True)
        else:
            response = requests.post(clients[key]["url"], \
            headers=clients[key]["headers"], \
            data=json.dumps(clients[key]["data"]), \
            verify=True)

        if response.status_code == 200 or response.status_code == 204:
            print("Successfully posted to %s." % key)
            print("  Status Code: %d" % response.status_code)
        else:
            print("Failed to post to %s." % key)
            print("  Status Code: %d" % response.status_code)

if __name__ == '__main__':

    #creates baseline config using the current running-config, if it doesn't exist.
    if os.path.isfile("startup.cfg") == False:
        startCfg = cli.execute("show run")
        with open("startup.cfg", "w") as f:
            f.write(startCfg)

    #write current running-config to file
    runCfg = cli.execute("show run")
    with open("running.cfg", "w") as f:
        f.write(runCfg)

    #diff the files
    #diffCfg = os.popen("diff startup.cfg running.cfg")
    diffCfg = os.popen("sdiff -l startup.cfg running.cfg | cat -n | grep -v -e '($'")
    diff = diffCfg.read()

    #post the diff as a message to the WebEx Teams room
    post("Diff between baseline switch config and current running-config. \n\n" + diff)
