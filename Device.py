from os import system
from module import mail
from module import database

class Device:
	DEVICE_STATE_INACTIVE = 0
	DEVICE_STATE_ACTIVE = 1
	DEVICE_STATE_SUSPECT_ACTIVITY = 2
	DEVICE_STATE_STOLE = 3

	serialNumber
	state = 0
	inDisabling = False
	triggeredTheftProcess = False

	def __init__(self, serialNumber):
		self.serialNumber = serialNumber

	def checkState():
		data = database.retrieveDeviceData(self.serialNumber)
		self.state = data['state']
		self.inDisabling = data['inDisabling']
		self.triggeredTheftProcess = data['triggeredTheftProcess']

	def changeState(self, newState):
		if self.state != self.DEVICE_STATE_SUSPECT_ACTIVITY and newState == self.DEVICE_STATE_SUSPECT_ACTIVITY:
			database.notifySuspectActivity(self.serialNumber)

		self.state = newState

	def inDisabling(self):
		database.notifyDisabling(self.serialNumber)
		self.inDisabling = True

	def triggerTheftProcess(self):
		self.triggeredTheftProcess = True

		system("sh /home/pi/script/theft_process.sh")

