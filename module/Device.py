class Device:
	DEVICE_STATE_INACTIVE = 0
	DEVICE_STATE_ACTIVE = 1
	DEVICE_STATE_SUSPECT_ACTIVITY = 2
	DEVICE_STATE_STOLE = 3

	serialNumber = ""
	state = 0
	inDisabling = False
	triggeredTheftProcess = False

	def __init__(self, serialNumber):
		self.serialNumber = serialNumber
