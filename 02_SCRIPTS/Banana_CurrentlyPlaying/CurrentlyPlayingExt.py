"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

import base64
import json
import webbrowser

class CurrentlyPlayingExt:
	"""
	CurrentlyPlayingExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.client = op('webclient1')
		self.userCode = ''
		self.clientId = ''
		self.clientSecret = ''

		TDF.createProperty(self, 'Artists', value='', dependable=True,
						   readOnly=False)
		TDF.createProperty(self, 'Trackname', value='', dependable=True,
						   readOnly=False)
		TDF.createProperty(self, 'Albumcover', value='', dependable=True,
						   readOnly=False)

		self.client.par.token = ''
		self.ownerComp.par.Token = ''
		self.ownerComp.par.Refreshtoken = ''
		self.ownerComp.par.Life = 3600

		if self.ownerComp.par.Clientsecret != '' and self.ownerComp.par.Clientid != '':
			self.GetIdentifiedAccess()
		else:
			self.ownerComp.addError('Your app settings Client ID and Client Secret are missing. You need to create a Spotify Developer App and input those settings on the component.')

	"""
	AUTH FUNCTIONS
	"""
	# Ask a Spotify user to login and forward him to the TouchDesigner endpoint after log. It will gives TouchDesigner access to the user code as a query parameter.
	# User code is later exchanged for Token, Refresh Token and Expiration time using GetAccessToken(...)
	def GetIdentifiedAccess(self):
		url = 'https://accounts.spotify.com/authorize'
		queryPar = 'client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'
		newString = queryPar.format(client_id=self.ownerComp.par.Clientid.eval(), redirect_uri=self.ownerComp.par.Redirecturi.eval(), scope='user-read-currently-playing')	
		webbrowser.open_new_tab(url + '?' + newString)

	# Query the Spotify API for final authentification by exchanging the user code for a token
	# When no code is passed, can be used to generate a public, unscopped token.
	def GetAccessToken(self, code=None):
		url = 'https://accounts.spotify.com/api/token'
		method = 'POST'
		byteArrayAsString = self.CredentialsToBase64().decode('ascii')
		header = {
			'Authorization': 'Basic ' + byteArrayAsString
		}
		data = {
			'grant_type': 'client_credentials' if not code else 'authorization_code',
			'code': code,
			'redirect_uri': self.ownerComp.par.Redirecturi.eval()
		}
		self.client.request(url, method, header=header, data=data)
	
	# An API request made when the current token is expired. We are using the refresh token to generate a new token from the Spotify API
	def OnTokenExpired(self):
		url = 'https://accounts.spotify.com/api/token'
		method = 'POST'
		byteArrayAsString = self.CredentialsToBase64().decode('ascii')
		header = {
			'Authorization': 'Basic ' + byteArrayAsString
		}
		data = {
			'grant_type': 'refresh_token',
			'refresh_token': self.ownerComp.par.Refreshtoken.eval()
		}
		self.client.request(url, method, header=header, data=data)				

	"""
	HELPERS
	"""
	# Convert developer application Clientid and Secret to base64
	def CredentialsToBase64(self):
		message = self.ownerComp.par.Clientid.eval() + ':' + self.ownerComp.par.Clientsecret.eval()
		messageBytes = message.encode('ascii')
		base64Bytes = base64.b64encode(messageBytes)
		return base64Bytes

	# Save the access token, refresh token, and expiration time after getting an answer from the Spotify API on the request for token by exchanging the user code
	def SaveAccessTokenAndConnect(self, data):
		self.client.par.token = data['access_token']
		self.ownerComp.par.Token = data['access_token']
		self.ownerComp.par.Refreshtoken = data['refresh_token']
		self.ownerComp.par.Life = data['expires_in']
		op('timer1').par.start.pulse()

	# Convert a byte array to JSON
	def ResponseBytesAsJson(self, bytesPayload):
		jsonString = bytesPayload.decode('utf8')
		return json.loads(jsonString)

	# Retrieve the user code server side after the user was redirected to TouchDesigner from the Spotify Login page
	# The code is stored in case it is needed later
	def ExtractResponseFromLogin(self, data):
		if 'error' not in data['pars'] and 'code' in data['pars']:
			self.userCode = data['pars']['code']
			self.GetAccessToken(self.userCode)

	"""
	SPOTIFY USER API
	"""
	# An API request used to retrieve the currently playing track of a user
	def GetCurrentlyPlaying(self):
		url = 'https://api.spotify.com/v1/me/player/currently-playing'
		method = 'GET'
		header = {
			'Authorization': 'Bearer ' + self.client.par.token.eval()
		}
		data = {}
		self.client.request(url, method, header=header, data=data)

	# Updates the dependable propreties after getting an answer from the Spotify API
	def SetCurrentlyPlaying(self, data):
		self.ownerComp.Artists = ', '.join([artist['name'] for artist in data['item']['artists']]) if data['is_playing'] and 'artists' in data['item'] else ''
		self.ownerComp.Trackname = data['item']['name'] if data['is_playing'] and 'name' in data['item'] else ''
		self.ownerComp.Albumcover = data['item']['album']['images'][0]['url'] if data['is_playing'] and 'album' in data['item'] else ''

	"""
	Tools
	"""
	# A function that convert the serialized component to a TOX
	def Build(self):
		# In version 0.1, there is no components within the component, we just have to de-externalized the python files
		for extFile in self.ownerComp.findChildren(parName='file', onlyNonDefaults=True):
			extFile.par.syncfile = False
			extFile.par.file = ''

		# Empty sensitive infos
		self.clientId = self.ownerComp.par.Clientid.eval()
		self.ownerComp.par.Clientid = ''
		self.clientSecret = self.ownerComp.par.Clientsecret.eval()
		self.ownerComp.par.Clientsecret = ''
		self.ownerComp.par.Token = ''
		self.ownerComp.par.Refreshtoken = ''

		# Once delinked, we save the tox to release folder
		filePath = './_RELEASE/' + self.ownerComp.name + '_Release_' + self.ownerComp.par.Version.eval() + '.tox'
		self.ownerComp.save(filePath)

		# Put back sensitive infos
		self.ownerComp.par.Clientid = self.clientId
		self.ownerComp.par.Clientsecret = self.clientSecret		

		# Then we reload the dev tox because we don't want to break everything
		self.ownerComp.par.reinitnet.pulse()

	# A function to save tox itself on Ctrl+s
	def PreSave(self):
		self.clientId = self.ownerComp.par.Clientid.eval()
		self.ownerComp.par.Clientid = ''
		self.clientSecret = self.ownerComp.par.Clientsecret.eval()
		self.ownerComp.par.Clientsecret = ''
		self.ownerComp.par.Token = ''
		self.ownerComp.par.Refreshtoken = ''

		self.ownerComp.save(self.ownerComp.par.externaltox.eval())

	def PostSave(self):
		self.ownerComp.par.Clientid = self.clientId
		self.ownerComp.par.Clientsecret = self.clientSecret
