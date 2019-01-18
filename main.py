import time
import random
import string
from module import component
from module import database
from module import grovepi
from module import GPIO
from module import I2C

#Partie Accelerometre 

address = 0x6a #On renseigne l'adresse de l'accelerometre que l'on recupere avec la commande i2cdetect -y -1

class LSM6DS3:
    i2c = None
    tempvar = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0

    
    def __init__(self, address=0x6a, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        dataToWrite = 0 #Start Fresh!
        dataToWrite |= 0x03 # set at 50hz, bandwidth
        dataToWrite |= 0x00  # 2g accel range
        dataToWrite |= 0x10 # 13hz ODR
        self.i2c.write8(0X10, dataToWrite) #writeRegister(LSM6DS3_ACC_GYRO_CTRL2_G, dataToWrite);
        
        accel_center_x = self.i2c.readS16(0X28)
        accel_center_y = self.i2c.readS16(0x2A)
        accel_center_z = self.i2c.readS16(0x2C)
    
    def readRawAccelX(self):
    	output = self.i2c.readS16(0X28)
    	return output;
    
    def readRawAccelY(self):
    	output = self.i2c.readS16(0x2A)
    	return output;
    
    def readRawAccelZ(self):
    	output = self.i2c.readS16(0x2C)
    	return output;
    	
    def calcAnglesXY(self):
        #Using x y and z from accelerometer, calculate x and y angles
        x_val = 0
        y_val = 0
        z_val = 0
        result = 0
        
        x2 = 0
        y2 = 0
        z2 = 0
        x_val = self.readRawAccelX() - accel_center_x
        y_val = self.readRawAccelY() - accel_center_y
        z_val = self.readRawAccelZ() - accel_center_z
        
        x2 = x_val*x_val
        y2 = y_val*y_val
        z2 = z_val*z_val
        result = math.sqrt(y2+z2)
        
        if (result != 0):
            result = x_val/result
            accel_angle_x = math.atan(result)
            return accel_angle_x;



    def readRawGyroX(self):
        output = self.i2c.readS16(0X22)
        return output;

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output;

    def calcGyroXAngle(self):
        temp = 0
        temp += self.readFloatGyroX()
        if (temp > 3 or temp < 0):
            self.tempvar += temp
        return self.tempvar;

    def calcGyro(self, rawInput):
        gyroRangeDivisor = 245 / 125; #500 is the gyro range (DPS)
        output = rawInput * 4.375 * (gyroRangeDivisor) / 1000;
        return output;

    #ruche_enMouvement : lsm -> Bool
    #Renvoi True si l'accelerometre est en mouvement, False sinon
    #On verifie que la difference entre deux prises de valeurs ne consitue pas un ecart trop important
    def ruche_enMouvement(self):
        enMouvement = False
        xdebut = self.readRawAccelX()
        ydebut = self.readRawAccelY()
        zdebut = self.readRawAccelZ()
        time.sleep(0.2)
        xfin = self.readRawAccelX()
        yfin = self.readRawAccelY()
        zfin = self.readRawAccelZ()
        if (abs(xdebut - xfin) > 1300 or abs(ydebut - yfin) > 1300 or abs(zdebut - zfin) > 1300):
            enMouvement = True
        return enMouvement
    
#################################################################

DEVICE_ID = 1

port_button = 3
previous_button_state = 0
deviceState = database.getDeviceState(DEVICE_ID)
mvtDetecte = True
photoPrise = False



#database.addConfirmationCode("ABCDE")
#database.codeConfirmed("ABCDE",DEVICE_ID)



grovepi.pinMode(port_button, "INPUT")

while True :
    try :
        if(grovepi.digitalRead(port_button) != previous_button_state):
            previous_button_state = grovepi.digitalRead(port_button)
            if (grovepi.digitalRead(port_button) == 1):
                if(deviceState == 0):
                    database.updateDeviceState(DEVICE_ID, 1)
                    deviceState = 1
                else :
                    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                    database.addConfirmationCode(code)
                    confirm = input('Entrez le code de confirmation : ')
                    database.codeConfirmed(confirm, DEVICE_ID)
                    database.updateDeviceState(DEVICE_ID, 0)
                    deviceState = database.getDeviceState(DEVICE_ID)
                    
                    
                    
        
        if(deviceState > 0):
            if(mvtDetecte and deviceState == 1 and not photoPrise):
                etatSuspect = True
                component.takePhotos("photos/photo_",5)
                photoPrise = True
                print("photo prises !")
                
            else :
                print("Je ne fais rien")
        
        time.sleep(0.5)
        
    except IOError:
        print("Error")
