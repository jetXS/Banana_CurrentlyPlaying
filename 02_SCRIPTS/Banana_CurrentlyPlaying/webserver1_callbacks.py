# me - this DAT.
# webServerDAT - the connected Web Server DAT
# request - A dictionary of the request fields. The dictionary will always contain the below entries, plus any additional entries dependent on the contents of the request
# 		'method' - The HTTP method of the request (ie. 'GET', 'PUT').
# 		'uri' - The client's requested URI path. If there are parameters in the URI then they will be located under the 'pars' key in the request dictionary.
#		'pars' - The query parameters.
# 		'clientAddress' - The client's address.
# 		'serverAddress' - The server's address.
# 		'data' - The data of the HTTP request.
# response - A dictionary defining the response, to be filled in during the request method. Additional fields not specified below can be added (eg. response['content-type'] = 'application/json').
# 		'statusCode' - A valid HTTP status code integer (ie. 200, 401, 404). Default is 404.
# 		'statusReason' - The reason for the above status code being returned (ie. 'Not Found.').
# 		'data' - The data to send back to the client. If displaying a web-page, any HTML would be put here.

# return the response dictionary
def onHTTPRequest(webServerDAT, request, response):
	response['statusCode'] = 200 # OK
	response['statusReason'] = 'OK'
	response['data'] = '<b>TouchDesigner: </b>' + 'The link between your Spotify user account and Banana_CurrentlyPlaying was a success.'
	parent().ExtractResponseFromLogin(request)
	return response

def onWebSocketOpen(webServerDAT, client, uri):
	return

def onWebSocketClose(webServerDAT, client):
	return

def onWebSocketReceiveText(webServerDAT, client, data):
	webServerDAT.webSocketSendText(client, data)
	return

def onWebSocketReceiveBinary(webServerDAT, client, data):
	webServerDAT.webSocketSendBinary(client, data)
	return

def onWebSocketReceivePing(webServerDAT, client, data):
	return

def onWebSocketReceivePong(webServerDAT, client, data):
	return

def onServerStart(webServerDAT):
	return

def onServerStop(webServerDAT):
	return
	