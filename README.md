# vCSE_eem_webex_bot

# Building a custom app hosted on a cisco switch.  No external server needed.
This app will check for a config change and post the diff to a webex teams rooms.

## Setup Overview
This script requires:
  1.  Webex Teams
      - Communications and Messaging Application
  2.  EEM in IOS-XE
      - What is EEM?  Here's a Blog reference.
      - https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479#:~:text=The%20EEM(Embedded%20Event%20manager,minor%20enhancements%20and%20create%20workarounds.
  3.  Guestshell in IOS-XE
      - What's guestshell?  Here's a Blog reference.
      - https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394
  4.  Python Script to process and post the config diff
      - Our python script is in github
      - https://github.com/jtsu/vCSE_eem_webex_bot


## WebEx Teams Setup
Create a simple bot and write down the access token
  - version 1 of this bot is not interactive
  - just used to send messages to the WebEx Room
  - reference: https://developer.webex.com/docs/bots
Create a webex Teams room and get the Room ID
  - This is where the bot will be posting messages about the switch being monitored
  - reference: https://developer.cisco.com/learning/lab/collab-spark-chatops-bot-itp/step/2
Copy bot's access token and room id to the python module, 'mytokens.py'


## EEM Setup
Configure the EEM Applet on the switch
  '''
  event manager session cli username "developer"
  event manager applet test
  event syslog pattern "%SYS-5-CONFIG_I: Configured from" maxrun 200
  action 0.0 cli command "en"
  action 1.0 cli command "guestshell run python test.py"
  '''

## Guestshell setup
IOX needs to be enable for guestshell
  '''
  iox
  '''

Then enable guestshell
  '''
  guestshell enable
  '''

Enter guestsheel  to install python  modules and setup DNS
  '''
  guestshell
  '''

Config guestshell DNS
  '''
  echo "nameserver 208.67.222.222" | sudo tee --append /etc/resolv.conf
  '''

Install requests Module
  '''
  sudo pip install requests
  '''

Copy the python script to the EEM user policy directory.

**NOTE** You can copy the script to a directory in guestshell or you can create a
directory on the flash from the IOS-XE CLI.

You can type `exit` to return to IOS-XE.

**NOTE** The guestshell environment will persist across reboots.  It will not revert to the default
state unless you do a `guestshell destory` followed by another `guestshell enable`.

## Run the app
Make a configuration change on the switch.
EEM will run the script
The script will do a config diff and post a message to the teams room using your bot.
Log in to webex teams and check your teams room for the message.

**NOTE** Be sure to exit configuration mode since EEM is looking for a specific syslog message.
