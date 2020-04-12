# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# If Client ID is changing, it is better to go thru the whole authentification flow again, same for Client secret.
	if par.name == 'Clientid' or par.name == 'Clientsecret':
		if parent().par.Clientid.eval() != '' and parent().par.Clientsecret.eval() != '':
			parent().GetIdentifiedAccess()
	return

def onPulse(par):
	if par.name == 'Forcereauth':
		parent().GetIdentifiedAccess()
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	