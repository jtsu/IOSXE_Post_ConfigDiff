# IOS-XE Post ConfigDiff
Tracking IOS-XE config diffs with collaboration clients 

## Use Case Statement
 
Some times it can be difficult to identify exactly what config changes were make on a Cisco switch or router.  There are certainly applications on the market to help examine and identify configuration differences.  But it would be nice to track those changes and see a history of that information in a single collaboration tool that you use on a daily basis.

We created a simple application that would track configuration changes and post those changes to a Webex Teams room.  With all the changes now posted in a room, it is very easy to scroll back to see what changes were made.  

Webex Teams isn't universally used by all our customers, so we decided to created a simple framework to support other collaboration clients.  Our app includes options to post messages to Microsoft Teams and Slack.

Many IT administrators have security policies that prohibit their network infrastructure from having direct access to the public cloud.  We also included an option to enable the use of an HTTP Proxy for those network environments that would need it.

One of the limitations we have is that we do our diff to a baseline config.  It would be great to have an option to see a diff to a prior versions, not to only a baseline config.


## White Papers and Helpful Blog Posts
These are some informative references that helped us with our project. 
* Many thanks to Patrick Mosimann and the Cisco DevNet Team for sharing their scripts that was the basis for our app:  [eem_configdiff_to_spark](https://github.com/CiscoDevNet/python_code_samples_network/tree/master/eem_configdiff_to_spark)
* Thanks to Ashish (ashirkar) for his blog post shared on Cisco Community:
  [Cisco EEM Basic Overview and Sample Configurations](https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479)
* Thanks to Hank Preston for his blog post shared on Cisco Community:
  [Introducing Python and Guest Shell on IOS-XE 16.5](https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394)

## Links to DevNet Learning Labs and Useful Guides
Here's are some Cisco DevNet and Developers links for additional learning and configuration.
* [Webex Teams Bot](https://developer.webex.com/docs/bots)
* [Chat-Ops with Webex and Python](https://developer.cisco.com/learning/lab/collab-spark-chatops-bot-itp/step/1)
* [Introduction to Guestshell on IOS XE](https://developer.cisco.com/learning/modules/net_app_hosting)
* [Incoming Webhooks Integration on Cisco Webex App Hub](https://apphub.webex.com/messaging/applications/incoming-webhooks-cisco-systems-38054)
* [Programmability Configuration Guide, Cisco IOS XE Fuji 16.7.x](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/167/b_167_programmability_cg/guest_shell.html)

## Related Sandbox
Cisco DevNet has some terffic resource you can use if you don't have access to a Cisco IOS XE platform. Try out the IOS XE Sandboxes and you can start exploring and testing things out yourself.  
* [Cisco IOS XE Sandboxes](https://developer.cisco.com/docs/ios-xe/#!sandboxes/reservation-based-sandboxes)
