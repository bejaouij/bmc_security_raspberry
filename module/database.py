import pymysql

def getConnector():
    connection = pymysql.connect(host = "localhost",
                             user = "pi",
                             password = "nikleta69",
                             db = "bmc_security")
    return connection

def updateDeviceState(device_id, device_state):
    connection = getConnector()
    
    try :
        with connection.cursor() as cursor:
            sql = "UPDATE device SET device_state = "+str(device_state)+" WHERE device_id = "+str(device_id)+""
            cursor.execute(sql)
            connection.commit()
                
    finally:
        connection.close()
        
        
def getDeviceState(device_id):
    connection = getConnector()
    
    try :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM device WHERE device_id = "+str(device_id)+""
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[2]
                
    finally:
        connection.close()
        
        
def addConfirmationCode(code):
    connection = getConnector()
    
    try :
        with connection.cursor() as cursor:
            sql = "INSERT INTO activationcode(activationcode_code, activationcode_expiration_date, activationcode_used, device_id) VALUES('"+code+"',NULL, false, 1 )"
            cursor.execute(sql)
            connection.commit()
                
    finally:
        connection.close()
        
def codeConfirmed(code, device_id):
    connection = getConnector()
    
    try :
        with connection.cursor() as cursor:
            sql = "SELECT * FROM activationcode WHERE activationcode_code = '"+code+"'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if(result[3] == 0):
                sql = "UPDATE activationcode SET activationcode_used = 1 WHERE activationcode_code = '"+code+"'"
                cursor.execute(sql)
                sql = "UPDATE device SET device_state = 0 WHERE device_id = "+str(device_id)+""
                cursor.execute(sql)
                connection.commit()
                return True
                
            else :
                print("Code déjà activé !")
                return False
            
    finally:
        connection.close()
    
    
    
    
    
    