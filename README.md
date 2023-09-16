# course-slot-checker
Script for checking whether an online waterloo course has space.

In order to send emails from a gmail account, an [App Password](https://support.google.com/accounts/answer/185833?hl=en) must be created and used here.
This can be hosted on free tier AWS t2.micro ec2 instance, using the [nohup](https://en.wikipedia.org/wiki/Nohup) command to run it forever.

There is a bug / feature in this script, where if there is an open spot, an email will be sent every tick (10 seconds). Didn't care enough to fix it when using.
