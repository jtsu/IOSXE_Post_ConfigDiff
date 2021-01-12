# Building a custom app hosted on a Cisco Catalyst Switch.  
This app will check for a config change and post the diff to a webex teams rooms.

## Setup Overview
This script requires the following:
  1.  Webex Teams
      - A Cisco Communications and Messaging Application
  2.  EEM in IOS-XE
      - The Embedded Event manager (EEM) is a software component of cisco IOS-XE that can track and classify events that take place and can help you to automate tasks.
      - Here's a Blog reference: https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479#:~:text=The%20EEM(Embedded%20Event%20manager,minor%20enhancements%20and%20create%20workarounds
  3.  GuestShell in IOS-XE
      - The ability to execute Python code directly on a Cisco Switch is a part of the Application Hosting capabilities provided by GuestShell.  GuestShell is a containerized Linux runtime environment in which you can install and run applications, such as Python scripts.  From within Guest Shell you and your applications have access to the networks of the host platform, bootflash, and IOS CLI.  GuestShell is isolated from the underlying host software to prevent interference of the core network functions of the device.
      - Here's a Blog reference: https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394
  4.  Python Script 
      - process and post the config diff
      - Our python script is in github: https://github.com/jtsu/vCSE_eem_webex_bot


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
  ```
  event manager session cli username "developer"
  event manager applet test
  event syslog pattern "%SYS-5-CONFIG_I: Configured from" maxrun 200
  action 0.0 cli command "en"
  action 1.0 cli command "guestshell run python test.py"
  ```

## Guestshell setup
IOX needs to be enable for guestshell
  ```
  iox
  ```

Then enable guestshell
  ```
  guestshell enable
  ```

Enter guestsheel  to install python  modules and setup DNS
  ```
  guestshell
  ```

Config guestshell DNS
  ```
  echo "nameserver 208.67.222.222" | sudo tee --append /etc/resolv.conf
  ```

Install requests module
  ```
  sudo pip install requests
  ```

Copy the python script to the EEM user policy directory.

**NOTE:** You can copy the script to a directory in guestshell or you can create a
directory on the flash from the IOS-XE CLI.

You can type `exit` to return to IOS-XE.

**NOTE:** The guestshell environment will persist across reboots.  It will not revert to the default state unless you do a `guestshell destory` followed by another `guestshell enable`.

## Run the app
Time to run the app by making a configuration change on the switch. Log in to webex teams and check your teams room for the message.

**NOTE:** Be sure to exit configuration mode since EEM is looking for a specific syslog message.

###
Many thanks to Patrick Mosimann and the Cisco DevNet Team for sharing their scripts that was the basis for our app.  
You can find Patrick's original script here: https://github.com/CiscoDevNet/python_code_samples_network/tree/master/eem_configdiff_to_spark

