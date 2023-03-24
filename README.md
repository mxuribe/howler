# Howler


## Introduction

Howler is a command line application - built with python - that sends messages into a specified matrix room, and intended for use as a basic server notification system.

See the **Description** section below for more background information, or dive in and get started with the **Installation**.


## Installation

It is a python application; ok, ok, it is a glorified python script. But not a complex one. So, you will only need a couple of basic dependencies, such as the following:

1. Ensure that Python version 3.6 or higher is installed on the machine that will run this application.
2. Ensure that the Python Requests (HTTP library) is installed on the machine that will run this application.
3. Save a few values within the .bashrc file on the machine that will run this application.

...But, don't worry, just continue and the instructions will guide you along...

From a terminal emulator window:

```
# Clone the repo...so you have a copy of the code locally
$ git clone https://github.com/mxuribe/howler.git

# Change the working directory to howler
$ cd howler

# Install the python dependencies...well, its only Requests (for now)
pip3 install -r requirements.txt
```

After the Python dependencies have been installed, now go obtain and save some values within your .bashrc file.


## Environment Setup

In order to ensure the proper matrix account does the sending of the messages, and that the messages arrive at your specified matrix room, etc., you will need to obtain and save a few values - as environment variables - into your local machine's **~/.bashrc** file. You will need:

* The matrix **sender's** matrix ID - e.g. @theSenderAccount:matrix.org - saved as **MATRIX_BOT_USER_ID**.
* An **access token** for the matrix **sender** - e.g. abc123...fg246...yada...yada... - saved as **MATRIX_BOT_ACCESS_TOKEN**.
    * Here's how to obtain your access token via the Element matrix web client:
        1. Log into the matrix account that will be sending the messages (i.e. the account that will be used for this application).
        2. Navigate to that account's settings; such as by clicking on that account's avatar/profile image, then clicking "All settings" link.
        3. When the pop-up dialog appears, click the "Help & About" link on the left navigation.
        4. After the "Help & About" page loads, scroll all the way to the bottom.
        5. Click on the "Access Token" link in order to display it.
        6. Copy and store the value of the access token somewhere **secret and secure** for now. **You do not want anyone having access to this access token!**
* The specified target **matrix room's full ID** (html encoded, please) saved as **MATRIX_BOT_ROOM_ID**.
    * It **SHOULD** be something like this for example (where the exclamation mark is encoded): %21mzyx123abc123lmnop123:matrix.org
    * It should **NOT** be like this: !mzyx123abc123lmnop123:matrix.org
* The **full username** of the message **receipient's** matrix ID - e.g. @johnwick:matrix.org - saved as **MATRIX_RECIPIENT_FULL_USERNAME**.
    * **Note:** this could also be the same account as the sender, in case you simply wish to send yourself the messages (instead of someone else).
* The username ("short name") portion of the message receipient's matrix ID - e.g. johnwick - saved as **MATRIX_RECIPIENT_SHORT_USERNAME**.
    * **Note:** this could also be the same account as the sender, in case you simply wish to send yourself the messages (instead of someone else).


Once the above items have been gathered, you would simply add them to the end of your **.bashrc** file. Here's an **example** of what such an addition could look like:

```
...some existing stuff in your .bashrc file...
...etc...
export MATRIX_BOT_USER_ID="@@theSenderAccount:matrix.org"
export MATRIX_BOT_ACCESS_TOKEN="abc123...fg246...yada...yada..."
export MATRIX_BOT_ROOM_ID="%21mzyx123abc123lmnop123:matrix.org"
export MATRIX_RECIPIENT_SHORT_USERNAME="johnwick"
export MATRIX_RECIPIENT_FULL_USERNAME="@johnwick:matrix.org"
```

...Remember that after any changes to your .bashrc file, you would want to close and then restart any terminal sessions, or better yet "source" your .bashrc file. For example:

```
$ source ~/.bashrc
```


## Usage

This is an application that is intended to be run from the command line. So, usage is as follows:

### Using the default (non-custom) message
```
python3 ./howler.py
```

### Using a custom message

```
python3 ./howler.py -m "Uh oh, it appears that there is something amiss with this server."
```
...Or...
```
python3 ./howler.py --msg "Uh oh, it appears that there is something amiss with this server."
```

### Activating debug mode

```
python3 ./howler.py -d
```
...Or...
```
python3 ./howler.py --debug
```

### Getting Help (such as it is)

```
python3 ./howler.py -h
```
...Or...
```
python3 ./howler.py --help
```


## Description

Howler - a python, command line application - is intended to be used as a basic server notification system. A set of custom http/REST api calls made to a matrix server (in this case the matrix.org homeserver) are used to send notification messages to a specified matrix room leveraging the the matrix protocol.

It is expected that a dedicated matrix room is established ahead of time in order to receive all notifications produced by this application. Then, as the need arises for notifications to be sent, this application is activated to send the messages to said, dedicated matrix room. Messages can be directed at another matrix user who has access to this same matrix room, or messages can simply be sent to the same matrix account as the sender. Ideally, server operators, system admins, or those new-fangled devops folks would be the traditional audience for this type of application, but pretty much anyone interested in viewing such notifications could leverage this application. I know, I know, not very sophisticated. It suits my needs, and hey I'm learning alot!

The default mode of the application sends a basic/default message, and it merely appends the hostname (of whatever machine it runs on). However, you can also use the **-m** parameter to append a custom message (within quotes of course). Sorry, attachments are not supported at this time.


## Common/Expected Use-Cases:

It is all about sending notifications using this application - if or when something happens on your machine(s). So, think about scenarios like:

* Server health cron job, where a troubled server will trigger this application to send notice (about its health) to the user via matrix.
* Automated reporting system that would send a link to some report or file.
* Bot automation, such as for sending word about the completion of tasks/jobs.
* Etc.


## FAQs and Whys


### Q: What Is the Origin of the Name?

**A:** Howler...As in, howling to the moon, or howling into the ether (to get attention)...You know, like a wolf or coyote, or...Bah, nevermind! 🐺 😉


### Q: Why Do This? Can't You Use Email Instead?

**A:** Absolutely! System admins have been using email successfully as a server notification system for years and years. Other than leveraging the matrix protocol, there's nothing novel, new or unprecedented with my approach here or even this application. If you are happy using simple email notifications, then use that! However you find comfort and utility in using other notification systems - e.g. email, XMPP, sms/text, etc. - please use them!

I chose to do this for a few reasons:

* I wanted to learn more about the matrix protocol and associated APIs.
* I wanted to expand my knowledge of python for prototyping applications.
* I wanted a server notification system that is easy to use, setup, and deploy.
* By leveraging matrix, I avoid vendor or platform lock-in, and am not beholden to a central authority.
* I already use matrix as the basis for my personal chats, so this way I can leverage a server notification system **without installing yet another application (on my phone, laptop, etc.)**! Matrix for the double win!

Furthermore, it is conceivable that this notification system could become part of a bigger, more comprehensive status (like a status page) or monitoring system - either for system admin purposes, or for task automation completion purposes. The concept of playing around with matrix (and by extension rooms, notices to rooms, etc.) is very compelling for use-cases that have less to do with typical chat, and more to do with what other folks might leverage, say, bots in IRC for!


### Q: Why Use Environment Variables Instead of a Config File?

**A:** Because: security best-practice. I know that the variables could have been saved in a config file, or maybe one of those "fancy" **.env** files (and maybe with the file's permissions set to lock down mode or something). But, nothing seemed as secure as adding the variables to a user's .bashrc file. Also leveraging the .bashrc file approach felt like it struck a nice balance of security with ease of migrating the files for this application around to numerous other machines. By all means, if there is a better, easier, and more secure method, I'm open to suggestions!

### Q: Are There any Limitations and/or Constraints?

**A:** The only limits are your imagination! Sorry, I love stating that!

More seriously, yes, there are some limits:

* Sorry, this application is only expected to work on linux and linux-like operating systems. But, hey, you are free to fork this project, and adjust it to suit your systems.
* If the server that will be using this application is somehow blocked (such as via a firewall) from making outbound HTTP calls (via Python Requests library), then this might not be the solution for you! This application expects to be able to make such outbound network connections - even if only briefly.
* Being a python application, I suppose there could be performance limits as opposed to, say, if this application was written in languages like Go, Erlang, C/C++, Rust, etc. Then, again, if your system is generating so many notifications that you will be encountering limits due to leveraging Python...maybe you have bigger challenges than basic server notifications. More seriously, if you legitimately have such conditions, please get in touch, because I wish to learn your use-case!



### Q: Seems Like Alot of Environment Setup for Simply Sending Messages, No?

**A:** This is my matrix-based server notification system. There are many like it. But, this one is mine.

I am of course open to receiving any suggestions for improvement.


### Q: Yeah, But Why All This?

**A:** I spent too much time actually creating this application and drafting this README file...You know, people like me get so ["preoccupied that they could, that they didn't stop to think if they should"](https://youtu.be/4PLvdmifDSk?t=94).  😄

...And, in this case, that's ok.


## Deployment

More info coming soon...

I mean, it is just a python application, so maybe drop it in a place where it would be easy for you to run it from (assuming dependencies are met), ensure you have your environment variables saved in the .bashrc file...and that's it basically.

Veteran admins and experienced script users will have their own ideas and preferences for how to deploy a python application like Howler. But for tech novices, more instructions on suggested deployment will be coming soon.



## License

Howler is released under the GPL v3 (or later) license, see the [LICENSE](LICENSE.md) file.

