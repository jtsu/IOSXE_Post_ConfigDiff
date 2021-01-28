IOS-XE Post ConfigDiff
=====================================
Tracking IOS-XE config diffs with collaboration clients 

Some times it can be difficult to identify exactly what config changes were make on a Cisco switch or router. There are certainly applications on the market to help examine and identify configuration differences. But it would be better to see and track an audit trail of the differences.

We created a simple application that would track configuration changes and post those changes to a Webex Teams room. With all the changes now posted in a room, it is very easy to scroll back in time to see what changes were made.

Webex Teams isn't universally used by all our customers, so we also wanted to incorporate some options in our app to post to other collaboration clients. We included options to post messages to Microsoft Teams and Slack.

One of the limitations we have is that we do our diff to a baseline config. It would be great to have an option to see a diff to a prior version.

## White Papers and Helpful Blog Posts
Provide links to related white papers:
* Many thanks to Patrick Mosimann and the Cisco DevNet Team for sharing their scripts that was the basis for our app:  [eem_configdiff_to_spark](https://github.com/CiscoDevNet/python_code_samples_network/tree/master/eem_configdiff_to_spark)
* Thanks to Ashish (ashirkar) for his blog post shared on Cisco Community:
  [Cisco EEM Basic Overview and Sample Configurations](https://community.cisco.com/t5/networking-documents/cisco-eem-basic-overview-and-sample-configurations/ta-p/3148479)
* Thanks to Hank Preston for his blog post shared on Cisco Community:
  [Introducing Python and Guest Shell on IOS-XE 16.5](https://community.cisco.com/t5/developer-general-blogs/introducing-python-and-guest-shell-on-ios-xe-16-5/ba-p/3661394)

## Related Sandbox
Cisco IOS-XE related labs can be found on the DEVNET Sandbox.  You can search for "IOS XE on CSR" or "IOS XE on Catalyst 9000" Lab and try creating this project yourself.
* [Cisco DEVNET Sandbox Labs](https://devnetsandbox.cisco.com)

## Links to DevNet Learning Labs and Useful Guides
Here's are some Cisco DevNet and Developers links for additional learning and configuration.
* [Webex Teams Bot](https://developer.webex.com/docs/bots)
* [Chat-Ops with Webex and Python](https://developer.cisco.com/learning/lab/collab-spark-chatops-bot-itp/step/1)
* [Introduction to Guestshell on IOS XE](https://developer.cisco.com/learning/modules/net_app_hosting)
* [Incoming Webhooks Integration on Cisco Webex App Hub](https://apphub.webex.com/messaging/applications/incoming-webhooks-cisco-systems-38054)
* [Programmability Configuration Guide, Cisco IOS XE Fuji](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/167/b_167_programmability_cg/guest_shell.html)

