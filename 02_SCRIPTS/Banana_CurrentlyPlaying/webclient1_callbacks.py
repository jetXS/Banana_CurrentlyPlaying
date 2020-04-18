# me - this DAT.
# webClientDAT - The connected Web Client DAT
# statusCode - The status code of the response, formatted as a dictionary with two key-value pairs: 'code', 'message'.
# headerDict - The header of the response from the server formatted as a dictionary. Only sent once when streaming.
# data - The data of the response

def onConnect(webClientDAT):
	return
	
def onDisconnect(webClientDAT):
	return

def onResponse(webClientDAT, statusCode, headerDict, data):
	# 204 can happen when nothing is playing
	if statusCode['code'] == 204:
		parent().Albumcover = ''
		parent().Artists = ''
		parent().Trackname = ''
	elif statusCode['code'] == 429:
		print('Rate limited.')

	# In case if authentification issue, data might be empty
	if len(data):
		data = parent().ResponseBytesAsJson(data)
		
		# Use objects keys to identify the asynchronous response, there is no clean and easy way to do that in TouchDesigner to my knowledge.
		if 'access_token' in data:
			parent().SaveAccessTokenAndConnect(data)
		elif 'item' in data and data['currently_playing_type'] != 'unknown':
			parent().SetCurrentlyPlaying(data)
		elif 'meta' in data and 'analyzer_version' in data['meta']:
			parent().SetCurrentAudioAnalysis(data)
			print('Setting analysis')
		elif 'danceability' in data:
			parent().SetCurrentAudioFeatures(data)
			print('Setting features')
	return
	