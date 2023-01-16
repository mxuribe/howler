#!/usr/bin/env python3

"""
howler: a command line application that sends messages into a specified matrix room, and intended for use as a basic server notification system.


Copyright (C) 2020 Mauricio Uribe

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by 
the Free Software Foundation; either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program.  If not, see <https://www.gnu.org/licenses/>.


SPDX-License-Identifier: GPL-3.0-only


Howler - a python, command line application - is intended to be used as a basic server notification system. A set of custom http/REST api calls made to a matrix server (in this case the matrix.org homeserver) are used to send notification messages to a specified matrix room leveraging the the matrix protocol.

It is expected that a dedicated matrix room is established ahead of time in order to receive all notifications produced by this application. Then, as the need arises for notifications to be sent, this application is activated to send the messages to said, dedicated matrix room. Messages can be directed at another matrix user who has access to this same matrix room, or messages can simply be sent to the same matrix account as the sender. Ideally, server operators, system admins, or those new-fangled devops folks would be the traditional audience for this type of application, but pretty much anyone interested in viewing such notifications could leverage this application. I know, I know, not very sophisticated. It suits my needs, and hey I'm learning alot!

The default mode of the application sends a basic/default message, and it merely appends the hostname (of whatever machine it runs on). However, you can also use the -m parameter to append a custom message (within quotes of course). Sorry, attachments are not supported at this time.
"""

import datetime
import json
import argparse
import requests
import socket
import os
import uuid
import sys

__author__ = "Mauricio Uribe (aka mxu)"
__copyright__ = "Copyright 2020 Mauricio Uribe"
# __credits__ = "Mauricio Uribe (aka mxu)"
__maintainer__ = "Mauricio Uribe (aka mxu)"
__license__ = "GPLv3"
__status__ = "Development"
__version__ = "0.95"
__date__ = "2023-01-16"

# Default settings. 
# #################

# Get current date, timestamp. Only really using this during debug mode. 
current_datetime = str(datetime.datetime.now())

# Get hostname of local system (helps with reporting)
host_name = socket.gethostname()

# Establish the user agent string
user_agent_string = "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"

# Establishing text for the default message. 
# original message: msg_body_preamble = "Howler system notification for the following host: "
msg_body_preamble = "Howler notification for host: " + host_name + ". \n\n"
msg_custom_default = "(No custom message was added.)"

# Establishing defaults for matrix. 

# Define target homeserver url and room id (the latter obtained via 
# enviroment variable). 
homeserver_api_url = "https://matrix.org/_matrix/client/r0/rooms/"

try:
	matrix_bot_room_id = os.environ["MATRIX_BOT_ROOM_ID"]
except KeyError:
	print("\n-------------------------------------------------------------")
	print(" Error: could not obtain value for matrix bot room id!")
	print("-------------------------------------------------------------")
	sys.exit("\nSorry, exiting the app. because this is quite essential. 😢 \n")

# Credentials for matrix sending account, obtained via
# environment variables. 
try:
	matrix_bot_user_id = os.environ["MATRIX_BOT_USER_ID"]
except KeyError:
	print("\n-------------------------------------------------------------")
	print(" Error: could not obtain value for matrix (sender) user id!")
	print("-------------------------------------------------------------")
	sys.exit("\nSorry, exiting the app. because this is quite essential. 😢 \n")

try:
	matrix_bot_access_token = os.environ["MATRIX_BOT_ACCESS_TOKEN"]
except KeyError:
	print("\n-------------------------------------------------------------")
	print(" Error: could not obtain value for matrix (sender) access token!")
	print("-------------------------------------------------------------")
	sys.exit("\nSorry, exiting the app. because this is quite essential. 😢 \n")

# Define recipient values, such as short, full names, etc. 
try:
	recipient_short_username = os.environ["MATRIX_RECIPIENT_SHORT_USERNAME"]
except KeyError:
	print("\n-------------------------------------------------------------")
	print(" Error: could not obtain value for recipient short username!")
	print("-------------------------------------------------------------")
	sys.exit("\nSorry, exiting the app. because this is quite essential. 😢 \n")

try:
	recipient_full_username = os.environ["MATRIX_RECIPIENT_FULL_USERNAME"]
except KeyError:
	print("\n-------------------------------------------------------------")
	print(" Error: could not obtain value for recipient full username!")
	print("-------------------------------------------------------------")
	sys.exit("\nSorry, exiting the app. because this is quite essential. 😢 \n")

recipient_address = "<a href='https://matrix.to/#/" + recipient_full_username + "' rel='noopener'>" + recipient_short_username + "</a>"

# Generating the (pseudo-random transaction ID)
# But as of 2022-09-22 not using. I think only needed for newer room versions.
trans_id = uuid.uuid4().hex

# End Default settings. 
# #################


def cli_args(msg_custom=msg_custom_default):
	# The function to get any parameters from the command line. 
	parser = argparse.ArgumentParser(
		description="howler: application for sending system notifications via matrix. ",
		epilog="For questions, reach out to m.x.u. on matrix at @mxu:matrix.org and on the web at https://mxuribe.com. \n \n ")

	# Add a custom message with the m parameter, otherwise use a default one.
	parser.add_argument("-m", "--msg", default=msg_custom, help="The body of the message...which should be within quotes.")

	# Activate debug mode to print debugging information.
	parser.add_argument("-d", "--debug", action="store_true", help="Activates printing of debugging information.")

	# Show the version of this app.
	parser.add_argument("-v", "--version", action="version", version="version: " + __version__, help="Displays the version of this software/application.")
	captured_cli_args = parser.parse_args()
	cli_msg = captured_cli_args.msg
	cli_debug_mode = captured_cli_args.debug
	return cli_msg, cli_debug_mode
	# return msg_from_cli


def matrix_send():
	# The function to actually send the message. 
	
	# The url - including matrix command - where the messages will be sent. 
	target_url = homeserver_api_url + matrix_bot_room_id + "/send/m.room.message"

	# Bringing in of cli arguments (if any). 
	msg_from_cli, debug_mode_cli = cli_args()

	# Concatenation and mild formatting of the message elements.  
	body_contents = recipient_short_username + ": " + msg_body_preamble + "** " + msg_from_cli + " **"
	formatted_body_contents = recipient_address + ": " + msg_body_preamble + "<strong>" + msg_from_cli + "</strong>"

	# Define http headers, like user agent string, auth. credentials token. 
	headers = {
		"Authorization": "Bearer " + matrix_bot_access_token, 
		"User-Agent": user_agent_string
		}

	# Put together the parameters for the api query string, includ. auth. creds.
	querystring = {
		"user_id": matrix_bot_user_id,
		"body": body_contents,
		"format": "org.matrix.custom.html", 
		"formatted_body": formatted_body_contents, 
		"msgtype":"m.text", 
	}

	# Send the http POST request.
	matrix_response = requests.post(target_url, json=querystring, headers=headers)
	try:
		matrix_response.raise_for_status()
	except Exception as exc:
		print("There was a problem (initially) posting the data to matrix: %s" % (exc))

	# If we reach this point, then we are good. 
	print("\n Howler has successfully sent the message! 👍 \n")

	# Print out some debugging information (to be sure stuff works)...
	# But only do so if debug mode is activated. 
	#print(matrix_response.text)
	if debug_mode_cli: 
		print("\n========== Matrix Debugging/Validation Info ==============\n")
		print("date, timestamp (local): " + current_datetime)
		print("host name: " + host_name)
		print("target url: " + target_url)
		print("custom message sent (if any): " + msg_from_cli)
		print("matrix status code: " + str(matrix_response.status_code))
		print("matrix response json: " + str(matrix_response.json()))
		# print("debug mode activated? " + str(debug_mode_cli))
		print("\n==========================================================\n")
	
	return


def main():
	# The core, initial function to kick off the other functions.
	cli_args()
	matrix_send()


if __name__ == "__main__":
	main()

