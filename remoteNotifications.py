# Based on https://github.com/sindresorhus/weechat-notification-center

import os
import weechat

# The path to log the messages to -- This will be monitored on the
		# client (remote or local) to send messages to notify-send
LOG_PATH = "/tmp/notifications.txt"

# Register the script.
weechat.register(
	'RemoteNotifications',                 # Script name 
	'Elijah Mirecki <elimirks@gmail.com>', # Author
	'0.2',                                 # Version
	'GPL',                                 # License
	'Pass notifications to ' + LOG_PATH,   # Description
	'',
	''
)

# Set the plugins for showing private and directed messages.
for key, val in [('show_highlights', 'on'), ('show_private_message', 'on')]:
	if not weechat.config_is_set_plugin(key):
		weechat.config_set_plugin(key, val)

# Hook on to the notification events.
weechat.hook_print('', 'irc_privmsg', '', 1, 'notify', '')

def logNotification(message, title):
	# Output the message to the log. Each line is a message.
	f = open(LOG_PATH, 'a')
	f.write(title + ': ' + message + '\n')
	f.close()

def notify(data, buffer, date, tags, displayed, highlight, prefix, message):
	# If the message is from a public channel.
	if weechat.config_get_plugin('show_highlights') == 'on' and highlight == '1':
		channel = weechat.buffer_get_string(buffer, 'localvar_channel')
		logNotification(message, title='%s %s' % (prefix, channel))
	# If the message is from a private message.
	elif weechat.config_get_plugin('show_private_message') == 'on' and 'notify_private' in tags:
		logNotification(message, title='%s [private]' % prefix)
	return weechat.WEECHAT_RC_OK

