#!/bin/bash

HOST="elijah@208.68.36.163"

# The path to the notifications log on the server.
NOTIFICATION_PATH="/tmp/notifications.txt"

function notifier {
	while read message; do
		notify-send "$message"
	done
}

ssh $HOST "tail -f $NOTIFICATION_PATH" | notifier

