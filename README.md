# IOS-XE Post ConfigDiff
This application uses the features and resources on the Cisco IOS-XE platforms.  The app will check for a config change and post the diff to a collaboration platform.  Currently the app will post messages to Webex Teams, Microsoft Teams, and Slack.  The app will also run directly on a Cisco IOS-XE switch or router, so no additional server resources are needed.

## Use Case Description
Some times it can be difficult to identify exactly what config changes were make on a Cisco switch or router.  There are certainly applications on the market to help examine and identify configuration differences.  But it would be nice to track those changes and see a history of that information in a single collaboration tool that you use on a daily basis.

We created a simple application that would track configuration changes and post those changes to a Webex Teams room.  With all the changes now posted in a room, it is very easy to scroll back to see what changes were made.  

Webex Teams isn't universally used by all our customers, so we decided to created a simple framework to support other collaboration clients.  Our app includes options to post messages to Microsoft Teams and Slack.

Many IT administrators have security policies that prohibit their network infrastructure from having direct access to the public cloud.  We also included an option to enable the use of an HTTP Proxy for those network environments that would need it.

One of the limitations we have is that we do our diff to a baseline config.  It would be great to have an option to see a diff to a prior versions, not to only a baseline config.

## Configuration Overview
This app uses the following:
- Webex Teams  
  - A Cisco Communications and Messaging Application.
  - Microsoft Teams or Slack can also be configured.
- EEM in IOS-XE
  - The Embedded Event manager (EEM) is a software component of cisco IOS-XE that can track and classify events that take place and can help you to automate tasks.
- GuestShell in IOS-XE
  - The ability to execute Python code directly on a Cisco Switch is a part of the Application Hosting capabilities provided by GuestShell.  GuestShell is a containerized Linux runtime environment in which you can install and run applications, such as Python scripts.  From within GuestShell, you have access to the networks of the host platform, bootflash and IOS CLI.  GuestShell is isolated from the underlying host software to prevent interference of the core network functions of the device.
- Python Script
  - This is the part of the app that will process and post the config diff to Webex Teams.

## Collaboration Clients Configuration  
- In our app, we're going to post message to the following platforms:
  - Webex Teams
  - Microsoft Teams
  - Slack
- We're going to use *Incoming Webhooks* to post the config diffs to each client.  Incoming webhooks let you post messages when an event occurs in another service.
- The steps to configure Incoming Webhooks are very similar for each of our three clients.
  - Create a room/team/channel in each client where our app will post the config diffs
  - Connect the *Incoming Webhook(s)* App in each client.
  - Name and select the room/team/channel you created.
  - Copy each webhook URL to the python module, 'mytokens.py'.

## EEM Configuration
This is the IOS-XE Configuration for EEM Applet.
  ```
  csr1000v# conf t
  csr1000v(config)# event manager applet test
  csr1000v(config-applet)# event syslog pattern "%SYS-5-CONFIG_I: Configured from" maxrun 200
  csr1000v(config-applet)# action 0.0 cli command "en"
  csr1000v(config-applet)# action 1.0 cli command "guestshell run python3 configDiff.py"
  csr1000v(config-applet)# end
  ```

## GuestShell Configuration
- IOX needs to be enable on the IOX-XE platform for GuestShell.
  ```
  csr1000v# conf t
  Enter configuration commands, one per line.  End with CNTL/Z.
  csr1000v(config)# iox
  csr1000v(config)# end
  ```

- A VirtualPortGroup is used to enable the communication between IOS XE and the GuestShell container.
  ```
  csr1000v# conf t
  csr1000v(config)# interface VirtualPortGroup 0
  csr1000v(config-if)# ip address 192.168.1.1 255.255.255.0
  csr1000v(config-if)# end
  ```

- Configure the network settings that will get passed to GuestShell when it's enabled.  
  ```
  csr1000v# conf t
  csr1000v(config)# app-hosting appid guestshell
  csr1000v(config-app-hosting)# vnic gateway1 virtualportgroup 0 guest-interface 0 guest-ipaddress 192.168.1.2 netmask 255.255.255.0 gateway 192.168.1.1 name-server 208.67.222.222
  csr1000v(config-app-hosting)# end
  ```

- Configure NAT if an access from the container to the outside world is needed.
  ```
  csr1000v# conf t
  csr1000v(config)# interface VirtualPortGroup0
  csr1000v(config-if)#  ip nat inside
  !
  csr1000v(config-if)# interface GigabitEthernet1
  csr1000v(config-if)#  ip nat outside
  csr1000v(config-if)# exit
  !
  csr1000v(config)# ip access-list extended NAT-ACL
  csr1000v(config-ext-nacl)# permit ip 192.168.1.0 0.0.0.255 any
  !
  csr1000v(config-if)# exit
  csr1000v(config)# ip nat inside source list NAT-ACL interface GigabitEthernet1 overload
  csr1000v(config)# end
  ```

- Enable GuestShell on the IOX-XE platform.
  ```
  csr1000v# guestshell enable
  ```

- Enter GuestShell to install python and some needed modules.
  ```
  csr1000v# guestshell
  ```

- Optional: We have already defined a DNS Name Server in the app-hosting config for GuestShell, so this step isn't needed. But if you didn't want to configure DNS from IOX-XE, you could configure it directly in the GuestShell environment.  
  ```
  [guestshell@guestshell ~]$ echo "nameserver 208.67.222.222" | sudo tee --append /etc/resolv.conf
  ```

- Depending on the IOS-XE platform and version, you may need to install python and some additional utilities.
  ```
  [guestshell@guestshell ~]$ sudo yum update -y
  [guestshell@guestshell ~]$ sudo yum install -y nano python3 epel-release
  [guestshell@guestshell ~]$ sudo yum search pip | grep python3
  [guestshell@guestshell ~]$ sudo yum install -y python3-pip
  ```

- Install the python requests module, and use the optional proxy, if needed. Be sure to use the proxy url and port for your environment.
  ```
  [guestshell@guestshell ~]$ sudo pip3 install --proxy your.proxy-server.com:8080 requests
  ```

- Copy the python script to the EEM user policy directory.  
  - You can copy the script to a directory in GuestShell or you can create a directory on the flash from the IOS-XE CLI.
  - In the EEM config above, the script is located in the home path on GuestShell.
  - If you would like to copy the script to the bootflash, use the absolute path in the EEM config.

- Exit GuestShell and return to IOS-XE
  ```
  [guestshell@guestshell ~]$ exit
  ```

**NOTE:** The guestshell environment will persist across reboots.  To return to a default state, destory the guestshell and enable guestshell again.


## Optional Configuration - System Proxy Settings for GuestShell
If a proxy server is needed in your enviroment, you'll need to configure the following proxy settings in GuestShell.

- Create a proxy.sh shell script to add the proxy settings to the system profile.
  ```
  [guestshell@guestshell ~]$ sudo nano /etc/profile.d/proxy.sh
  ```

- Add the following parameters in to proxy.sh shell script.  Be sure to use the proxy url and port for your environment.
  ```  
  PROXY_URL="http://your.proxy-server.com:8080/"
  export http_proxy="$PROXY_URL"
  export https_proxy="$PROXY_URL"
  export ftp_proxy="$PROXY_URL"
  export no_proxy="127.0.0.1,localhost"
  export HTTP_PROXY="$PROXY_URL"
  export HTTPS_PROXY="$PROXY_URL"
  export FTP_PROXY="$PROXY_URL"
  export NO_PROXY="127.0.0.1,localhost"
  ```

- Source the profile to activate the proxy settings.
  ```
  [guestshell@guestshell ~]$ source /etc/profile
  [guestshell@guestshell ~]$ env | grep -i proxy
  ```

-  Configure the proxy server for the Yum package manager.  Be sure to use the proxy url and port for your environment.
  ```
  [guestshell@guestshell ~]$ echo "proxy=your.proxy-server.com:8080" | sudo tee --append /etc/yum.conf

  ```

## Usage
To see the app in action, simply make a configuration change on the switch on your Cisco switch or router.  For example, you can change the description of an interface.
  ```
  csr1000v# conf t
  csr1000v(config)# interface GigabitEthernet3 
  csr1000v(config-if)# description Test Interface
  csr1000v(config-if)# end
  ```
Then you just need to login to WebEx Teams, or your preferred collaboration client, and check your room for the diff message.

**NOTE:** Be sure to exit configuration mode since EEM is looking for a specific syslog pattern.


## References 

Here's are some references for information more about the features used in our app.

* Many thanks to Patrick Mosimann and the Cisco DevNet Team for sharing their scripts that was the basis for our app:  [eem_configdiff_to_spark](https://github.com/CiscoDevNet/python_code_samples_network/tree/master/eem_configdiff_to_spark)
* Thanks to Ashish (ashirkar) for his blog post shared on Cisco Community:
  [Cisco EEM Basic Overview and Sample Configurations](https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479)
* Thanks to Hank Preston for his blog post shared on Cisco Community:
  [Introducing Python and Guest Shell on IOS-XE 16.5](https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394)
* [Incoming Webhooks Integration on Cisco Webex App Hub](https://apphub.webex.com/messaging/applications/incoming-webhooks-cisco-systems-38054)

## Getting Help

Here's are some Cisco DevNet and Developers links for additional learning and configuration.
* [Webex Teams Bot](https://developer.webex.com/docs/bots)
* [Chat-Ops with Webex and Python](https://developer.cisco.com/learning/lab/collab-spark-chatops-bot-itp/step/1)
* [Introduction to Guestshell on IOS XE](https://developer.cisco.com/learning/modules/net_app_hosting)

  
  
## Author(s)
  
This project was written and is maintained by the following individuals:
* Jason Su <jtsu@cisco.com>
* Dennis Tran <dentran@cisco.com>
* Matt Jennings <matjenni@cisco.com>
* Steven Tanti <stanti@cisco.com>




