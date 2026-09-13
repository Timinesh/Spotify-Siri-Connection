# Go to shortcuts, create a new shortcut rename the title to the name of this file Play on Spotify
# Search for Ask for Input in Search Actions 
# Ask for text with What song do you want to hear?
# Search for Run AppleScript in Search Actions

on run {input, parameters}
	set songName to input as text
	
	set pythonPath to "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"
	set scriptPath to (POSIX path of (path to home folder)) & "spotify-siri/spotify_siri.py"
	
	do shell script quoted form of pythonPath & " " & quoted form of scriptPath & " " & quoted form of songName
	
	return
end run
