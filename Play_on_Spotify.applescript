# Go to shortcuts, create a new shortcut rename the title to the name of this file Play on Spotify
# Search for Ask for Input in Search Actions 
# Ask for text with What song do you want to hear?
# Search for Run AppleScript in Search Actions

on run {input, parameters}
	set songName to input as string
	
	tell application "Spotify"
		activate
		-- Start playing search context
		play track ("spotify:search:" & songName)
		
		-- Wait for Spotify to actually start playing the track
		set counter to 0
		repeat until (player state is playing) or counter ≥ 20
			delay 0.2
			set counter to counter + 1
		end repeat
		
		delay 0.5
		
		-- Extract exact track URI and play it isolated
		try
			set exactTrackURI to spotify url of current track
			play track exactTrackURI
		end try
	end tell
	
	return input
end run
