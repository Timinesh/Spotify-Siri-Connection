# Go to shortcuts, create a new shortcut rename the title to the name of this file Next Song
# Search for Run AppleScript in Search Actions

on run {input, parameters}
	tell application "Spotify"
		next track
	end tell
	return input
end run
