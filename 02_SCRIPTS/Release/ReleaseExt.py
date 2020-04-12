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

class ReleaseExt:
	"""
	ReleaseExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def GenerateRelease(self):
		if hasattr(op(self.ownerComp.par.Comptobuildforrelease.eval()), 'Build'):
			op(self.ownerComp.par.Comptobuildforrelease.eval()).Build()
		else:
			# Do some magic
			return

	def OnPreSave(self):
		rootComps = root.findChildren(type=COMP, parName='externaltox', onlyNonDefaults=True)
		for comp in rootComps:
			if hasattr(comp, 'PreSave'):
				comp.PreSave()
			else:
				comp.save(comp.par.externaltox.eval())
					