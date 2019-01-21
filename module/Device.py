from module import database

class Device:
	DEVICE_STATE_INACTIVE = 0
	DEVICE_STATE_ACTIVE = 1
	VEHICLE_STATE_SUSPECT_ACTIVITY = 3
	VEHICLE_STATE_STOLE = 4
	VEHICLE_STATE_OK = 5

	serialNumber = None
	device_status = None
	vehicle_status = None
	inDisabling = False
	triggeredTheftProcess = False

	def __init__(self, serialNumber):
		self.serialNumber = serialNumber

	def checkState(self):
		data = database.retrieveDeviceData(self.serialNumber)
		self.device_status = data['status_code']
		self.vehicle_status = data['vehicle_status']
		self.inDisabling = data['in_disabling']

		if self.vehicle_status == self.VEHICLE_STATE_STOLE:
			self.triggeredTheftProcess = True