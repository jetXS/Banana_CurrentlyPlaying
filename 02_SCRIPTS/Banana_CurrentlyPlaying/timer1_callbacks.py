# me - this DAT.
# timerOp - the connected Timer CHOP
# cycle - the cycle index
# segment - the segment index
# fraction - the time in fractional form
#
# interrupt - True if the user initiated a premature
# interrupt, False if a result of a normal timeout.
#
# onInitialize(): if return value > 0, it will be
# called again after the returned number of frames.

def onInitialize(timerOp):
	return 0

def onReady(timerOp):
	return
	
def onStart(timerOp):
	return
	
def onTimerPulse(timerOp, segment):
	return

def whileTimerActive(timerOp, segment, cycle, fraction):
	return

def onSegmentEnter(timerOp, segment, interrupt):
	return
	
def onSegmentExit(timerOp, segment, interrupt):
	return

def onCycleStart(timerOp, segment, cycle):
	return

def onCycleEndAlert(timerOp, segment, cycle, alertSegment, alertDone, interrupt):
	return
	
def onCycle(timerOp, segment, cycle):
	return

def onDone(timerOp, segment, interrupt):
	parent().OnTokenExpired()
	return
	