# me - this DAT.
# webClientDAT - The connected Web Client DAT
# statusCode - The status code of the response, formatted as a dictionary with two key-value pairs: 'code', 'message'.
# headerDict - The header of the response from the server formatted as a dictionary. Only sent once when streaming.
# data - The data of the response
# id - The request's unique identifier

def onConnect(webClientDAT, id):
	return
	
def onDisconnect(webClientDAT, id):
	return

def onResponse(webClientDAT, statusCode, headerDict, data, id):
	# 204 can happen when nothing is playing
	if statusCode['code'] == 204:
		parent().Albumcover = ''
		parent().Artists = ''
		parent().Trackname = ''
	elif statusCode['code'] == 429:
		print('Rate limited.')

	# In case of authentification issue, data might be empty
	if len(data):
		data = parent().ResponseBytesAsJson(data)
		
		# Use objects keys to identify the asynchronous response, there is no clean and easy way to do that in TouchDesigner to my knowledge.
		idInQueue = False
		index = 0
		for queueObj in parent().RequestsQueue:
			if id == queueObj['id'] and not idInQueue:
				
				idInQueue = True
				if queueObj['type'] == 'access_token' and 'access_token' in data:
					parent().SaveAccessTokenAndConnect(data)
					break
				elif queueObj['type'] == 'currently_playing' and 'item' in data and data['currently_playing_type'] != 'unknown':
					parent().SetCurrentlyPlaying(data)
					break
				elif queueObj['type'] == 'analysis' and 'meta' in data and 'analyzer_version' in data['meta']:
					parent().SetCurrentAudioAnalysis(data)
					break
				elif queueObj['type'] == 'features' and 'danceability' in data:
					parent().SetCurrentAudioFeatures(data)
					break

				index += 1
		
		if not idInQueue:
			debug('Request ID was not found in queue.')
		else:
			if len(parent().RequestsQueue):
				parent().RequestsQueue.pop(index)
	return
	