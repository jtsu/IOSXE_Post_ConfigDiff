import cli
import requests
import json
import sys
import os
import mytokens

clients = {}

# incoming webhooks.  add your webhook url in mytokens.py.
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
# this is just an example if you don't plan to use webhooks
clients['WebEx Teams'] = {
    "url": "https://api.ciscospark.com/v1/messages/",
    "headers": {"Authorization": "Bearer %s" % mytokens.access_token, "Content-Type": "application/json"},
    "data": {"roomId": mytokens.teams_room, "text": ""}
}
'''

#set this to True if you use a HTTP Proxy.  Add the proxy url in mytokens.py.
use_proxy = True

http_proxy = mytokens.http_proxy
proxyDict = {
    "http"  : http_proxy
}

# Function for posting the message to the collaboration client
def post(message):

    for key, value in clients.items():
        clients[key]["data"]["text"] = message

        #Check if the default webhook url has been changed and skip the iteration if not changed.
    	if clients[key]["url"] == "https://your.webhook.url":
            print("Default %s Webhook URL unchanged in the mytokens.py module." % key)
            print("Replace the default with your %s webhook URL." % key)
            continue
        elif len(clients[key]["url"]) <= 0:
            print("%s Webhook URL needs to be added in the mytokens.py module." % key)
            continue

        if use_proxy:
        #Check if the default webhook url has been changed and skip the iteration if not changed.
        	if proxyDict["http"] == "http://proxy.your.server.com:port":
                sys.exit("SystemExit: Proxy enabled.  Change the Default proxy URL in the mytokens.py module.")
            else:
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
