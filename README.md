# Building a custom app hosted on a Cisco Catalyst Switch.  
This app will check for a config change and post the diff to a WebEx Teams Rooms.

## Setup Overview
This script requires the following:
- WebEx Teams
  - A Cisco Communications and Messaging Application
- EEM in IOS-XE
  - The Embedded Event manager (EEM) is a software component of cisco IOS-XE that can track and classify events that take place and can help you to automate tasks.
- GuestShell in IOS-XE
  - The ability to execute Python code directly on a Cisco Switch is a part of the Application Hosting capabilities provided by GuestShell.  GuestShell is a containerized Linux runtime environment in which you can install and run applications, such as Python scripts.  From within GuestShell, you have access to the networks of the host platform, bootflash and IOS CLI.  GuestShell is isolated from the underlying host software to prevent interference of the core network functions of the device.
- Python Script 
  - process and post the config diff
  - Our python script is in github: https://github.com/jtsu/vCSE_eem_webex_bot


## WebEx Teams Setup
- Create a simple bot and write down the access token.
  - Version 1 of this bot is not interactive.  The bot is only used to post messages to the WebEx Teams Room.
  - Copy the bot's Access Token to the python module, 'mytokens.py'.
  - See references below for information on creating a bot.
- Create a webex Teams room and get the Room Id.
  - This is where the bot will be posting messages about the config diff on the switch.
  - Copy room id to the python module, 'mytokens.py'.
  - See references below for information on getting the Room Id.

## EEM Setup
Configure the EEM Applet on the switch.
  ```
  event manager session cli username "developer"
  event manager applet test
  event syslog pattern "%SYS-5-CONFIG_I: Configured from" maxrun 200
  action 0.0 cli command "en"
  action 1.0 cli command "guestshell run python test.py"
  ```

## GuestShell Setup
- IOX needs to be enable for guestshell.
  ```
  Type 'iox' in the IOS-XE CLI.
  ```

- Enable guestshell.
  ```
  Type 'guestshell enable' in the IOS-XE CLI.
  ```

- Enter guestshell to install python  modules and setup DNS.
  ```
  Type 'guestshell' in the IOS-XE CLI.
  ```

- You should now be in GuestShell and will then configuring the DNS Name Server.
  ```
  echo "nameserver 208.67.222.222" | sudo tee --append /etc/resolv.conf
  ```

- From within GuestShell, install the python requests module.
  ```
  sudo pip install requests
  ```

- Copy the python script to the EEM user policy directory.  
  - You can copy the script to a directory in guestshell or you can create a directory on the flash from the IOS-XE CLI.

- Exit GuestShell and return to IOS-XE
  ```
  type `exit`
  ```
 
**NOTE:** The guestshell environment will persist across reboots.  It will not revert to the default state unless you do a `guestshell destory` and enable guestshell again.

## Run the app
Time to run the app by making a configuration change on the switch. Login to WebEx Teams and check your Teams room for the message.

**NOTE:** Be sure to exit configuration mode since EEM is looking for a specific syslog pattern.

## References
Many thanks to Patrick Mosimann and the Cisco DevNet Team for sharing their scripts that was the basis for our app:  
https://github.com/CiscoDevNet/python_code_samples_network/tree/master/eem_configdiff_to_spark

Thanks to Ashish (ashirkar) for his blog post on EEM:
https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479#:~:text=The%20EEM(Embedded%20Event%20manager,minor%20enhancements%20and%20create%20workarounds

Thanks to Hank Preston for his blog post on GuestShell:
https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394

Cisco Reference link to create a WebEx Teams Bot:
https://developer.webex.com/docs/bots

Cisco DevNet Learning Lab reference for getting the Webex Room Id: 
https://developer.cisco.com/learning/lab/collab-spark-chatops-bot-itp/step/2
