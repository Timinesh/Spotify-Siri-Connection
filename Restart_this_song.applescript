# Go to shortcuts, create a new shortcut rename the title to the name of this file Restart this song
# Search for Run AppleScript in Search Actions

on run {input, parameters}
	tell application "Spotify"
		set player position to 0
	end tell
	return input
end run
