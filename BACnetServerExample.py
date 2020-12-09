# CAS BACnet Stack Python Server Example 
# https://github.com/chipkin/BACnetServerExamplePython 
# 

import ctypes
import pathlib
import socket
import time # sleep function 
from CASBACnetStackAdapter import * # Contains all the Enumerations, and callback prototypes 

# Example database 
# -----------------------------------------------------------------------------
# This is an example database. Normaly this data would come from your sensor/database
db = { 
    "device": { 
        "instance": 389001,
        "objectName": "Device Rainbow"},
    "analogInput": {
        "instance": 0,
        "objectName": "AnalogInput Bronze",
        "presentValue": 99.6 },
    "binaryInput": {
        "instance": 3,
        "objectName": "BinaryInput Emerald",
        "presentValue": 1},
   "multiStateInput": {
        "instance": 13 , 
        "objectName": "MultiStateInput Hot Pink", 
        "presentValue": 3},
    "analogOutput": {
        "instance": 1,
        "objectName": "AnalogOutput Chartreuse",
        "presentValue": 1 
    },
    "analogValue": {
        "instance": 2,
        "objectName": "AnalogValue Diamond",
        "presentValue": 1 
    },
    "binaryOutput": {
        "instance": 4,
        "objectName": "BinaryOutput Fuchsia",
        "presentValue": 1 
    },
    "binaryValue": {
        "instance": 5,
        "objectName": "BinaryValue Gold",
        "presentValue": 1 
    },
    "multiStateOutput": {
        "instance": 14,
        "objectName": "MultiStateOutput Indigo",
        "presentValue": 1 
    },
    "multiStateValue": {
        "instance": 15,
        "objectName": "MultiStateValue Kiwi",
        "presentValue": 1 
    },
    "characterstringValue": {
        "instance": 40,
        "objectName": "CharacterstringValue Nickel",
        "presentValue": 1 
    },
    "integerValue": {
        "instance": 45,
        "objectName": "IntegerValue Purple",
        "presentValue": 1 
    },
    "largeAnalogValue": {
        "instance": 46,
        "objectName": "LargeAnalogValue Quartz",
        "presentValue": 1 
    },
    "positiveIntegerValue": {
        "instance": 48,
        "objectName": "PositiveIntegerValue Silver",
        "presentValue": 1 
    },
    "networkPort": {
        "BACnetIPUDPPort": 47808 
    }
}


# Globals 
# -----------------------------------------------------------------------------
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lastTimeValueWasUpdated = 0 

# Callbacks 
# -----------------------------------------------------------------------------
def CallbackReceiveMessage( message, maxMessageLength, receivedConnectionString, maxConnectionStringLength, receivedConnectionStringLength, networkType ):
    try: 
        data, addr = udpSocket.recvfrom(maxMessageLength)
        if not data: 
            print ("DEBUG: not data")

        # A message was recived. 
        # print ("DEBUG: CallbackReceiveMessage. Message Recived", addr, data, len(data) )

        # Convert the recived address to the CAS BACnet Stack connection string format. 
        ip_as_bytes = bytes(map(int, addr[0].split('.')))
        for i in range( len(ip_as_bytes) ):
            receivedConnectionString[i] = ip_as_bytes[i] 
        # UDP Port 
        receivedConnectionString[4] = int(addr[1] / 256)
        receivedConnectionString[5] = addr[1] % 256
        # New ConnectionString Length
        receivedConnectionStringLength[0] = 6

        # Convert the recived data to a format that CAS BACnet Stack can process.
        for i in range( len(data) ):
            message[i] = data[i] 

        # Set the network type 
        networkType[0] = ctypes.c_uint8(casbacnetstack_networkType["ip"])

        return len(data)
    except BlockingIOError:
        # No message, 
        # We are not waiting for a incoming message so our socket returns a BlockingIOError. This is normal. 
        return 0 
    
    # Catch all 
    return 0 

def CallbackSendMessage( message, messageLength, connectionString, connectionStringLength, networkType, broadcast ):
    print ("DEBUG: CallbackSendMessage messageLength:", messageLength ); 

    # Currently we are only supporting MSTP
    if networkType != casbacnetstack_networkType["ip"]:
        print ("Error: Unsupported network type. networkType:", networkType ); 
        return 0 

    # Extract the Connection String from CAS BACnet Stack into an IP address and port. 
    udpPort = connectionString[4] * 256 + connectionString[5] 
    if broadcast:        
        # Use broadcast IP address 
        # ToDo: Get the subnet mask and apply it to the IP address 
        print ("DEBUG:   ToDo: Broadcast this message. Local IP: ", socket.gethostbyname(socket.gethostname()), "Subnet: ????, Broadcast IP: ????" ); 
        ipAddress = '%d.%d.%d.%d' %(connectionString[0], connectionString[1], connectionString[2], connectionString[3])        
    else :
        ipAddress = '%d.%d.%d.%d' %(connectionString[0], connectionString[1], connectionString[2], connectionString[3])        
    
    print ("DEBUG:   connectionString: ", ipAddress, udpPort ); 

    # Extract the message from CAS BACnet Stack to a bytearray
    data = bytearray( messageLength )
    for i in range( len(data) ):
        data[i] = message[i]

    # Send the message 
    udpSocket.sendto( data, (ipAddress, udpPort) )
    return messageLength

def CallbackGetSystemTime( ):
    return int(time.time())

def CallbackGetPropertyReal(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print( "CallbackGetPropertyReal", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier['presentValue']:
            if objectType == bacnet_objectType["analogInput"] and objectInstance == db["analogInput"]["instance"]: 
                value[0] = ctypes.c_float(db["analogInput"]["presentValue"])
                return True 

    # Return false. The CAS BACnet Stack will use a default value. 
    return False

def CallbackGetPropertyCharString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount, encodingType, useArrayIndex, propertyArrayIndex):
    print( "CallbackGetPropertyCharString", deviceInstance, objectType, objectInstance, propertyIdentifier, maxElementCount, useArrayIndex, propertyArrayIndex )

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier['objectname']:
            if objectType == bacnet_objectType["analogInput"] and objectInstance == db["analogInput"]["instance"]: 
                objectName = db["analogInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process. 
                b_objectName = objectName.encode('utf-8')
                for i in range( len(b_objectName) ):
                    value[i] = b_objectName[i]
                # Define how long the Object name is 
                valueElementCount[0] = len(b_objectName) 
                return True 
            if objectType == bacnet_objectType["binaryInput"] and objectInstance == db["binaryInput"]["instance"]: 
                objectName = db["binaryInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process. 
                b_objectName = objectName.encode('utf-8')
                for i in range( len(b_objectName) ):
                    value[i] = b_objectName[i]
                # Define how long the Object name is 
                valueElementCount[0] = len(b_objectName) 
                return True 
            if objectType == bacnet_objectType["multiStateInput"] and objectInstance == db["multiStateInput"]["instance"]: 
                objectName = db["multiStateInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process. 
                b_objectName = objectName.encode('utf-8')
                for i in range( len(b_objectName) ):
                    value[i] = b_objectName[i]
                # Define how long the Object name is 
                valueElementCount[0] = len(b_objectName) 
                return True 

    # Return false. The CAS BACnet Stack will use a default value. 
    return False

def CallbackGetPropertyEnumerated(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print( "CallbackGetPropertyEnumerated", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier['presentValue']:
            if objectType == bacnet_objectType["binaryInput"] and objectInstance == db["binaryInput"]["instance"]: 
                value[0] = ctypes.c_uint32(db["binaryInput"]["presentValue"])
                return True 

    # Return false. The CAS BACnet Stack will use a default value. 
    return False

def CallbackGetPropertyBitString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyBitString", deviceInstance, objectType, objectInstance, propertyIdentifier, maxElementCount, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyBool(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyBool", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyDate(deviceInstance, objectType, objectInstance, propertyIdentifier, year, month, day, weekday, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyDate", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyDouble(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyDouble", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyOctetString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyOctetString", deviceInstance, objectType, objectInstance, propertyIdentifier, maxElementCount, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyInt", deviceInstance, objectType, objectInstance, propertyIdentifier,useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyTime(deviceInstance, objectType, objectInstance, propertyIdentifier, hour, minute, second, hundrethSeconds, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyTime", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )
    return False
def CallbackGetPropertyUInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyUInt", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex )
    return False

# Main application 
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print ("FYI: CAS BACnet Stack Python Server Example v0.0.1"); 
    print ("FYI: https://github.com/chipkin/BACnetServerExamplePython"); 

    # 1. Load the CAS BACnet stack functions
	# ---------------------------------------------------------------------------
    # Load the shared library into ctypes
    libpath = pathlib.Path().absolute() / libname
    CASBACnetStack = ctypes.CDLL(str(libpath), mode=ctypes.RTLD_GLOBAL)

    # Print the version information
    print( "FYI: CAS BACnet Stack version: %d.%d.%d.%d" %( CASBACnetStack.BACnetStack_GetAPIMajorVersion(), CASBACnetStack.BACnetStack_GetAPIMinorVersion(), CASBACnetStack.BACnetStack_GetAPIPatchVersion(), CASBACnetStack.BACnetStack_GetAPIBuildVersion() ))
    print( "FYI: CAS BACnet Stack python adapter version:", casbacnetstack_adapter_version )
    
    # 2. Connect the UDP resource to the BACnet Port
	# ---------------------------------------------------------------------------
    print( "FYI: Connecting UDP Resource to port=[%d]" %( db["networkPort"]["BACnetIPUDPPort"] ))
    HOST = ''	# Symbolic name meaning all available interfaces
    udpSocket.bind((HOST, db["networkPort"]["BACnetIPUDPPort"]))
    udpSocket.setblocking(False)
    print ("FYI: Local IP address: ", socket.gethostbyname(socket.gethostname()))

    # 3. Setup the callbacks
    # ---------------------------------------------------------------------------
    print( "FYI: Registering the Callback Functions with the CAS BACnet Stack" )

    # Note: 
    # Make sure you keep references to CFUNCTYPE() objects as long as they are used from C code. 
    # ctypes doesn't, and if you don't, they may be garbage collected, crashing your program when 
    # a callback is made
    #
    # Because of garbage collection. The pyCallback**** functions need to stay in scope. 
    pyCallbackReceiveMessage = fpCallbackReceiveMessage( CallbackReceiveMessage )
    CASBACnetStack.BACnetStack_RegisterCallbackReceiveMessage( pyCallbackReceiveMessage )    
    pyCallbackSendMessage = fpCallbackSendMessage( CallbackSendMessage )
    CASBACnetStack.BACnetStack_RegisterCallbackSendMessage( pyCallbackSendMessage )    
    pyCallbackGetSystemTime = fpCallbackGetSystemTime( CallbackGetSystemTime )
    CASBACnetStack.BACnetStack_RegisterCallbackGetSystemTime( pyCallbackGetSystemTime )
    pyCallbackGetPropertyBitString = fpCallbackGetPropertyBitString(CallbackGetPropertyBitString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBitString( pyCallbackGetPropertyBitString )
    pyCallbackGetPropertyBool = fpCallbackGetPropertyBool(CallbackGetPropertyBool)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBool( pyCallbackGetPropertyBool )
    pyCallbackGetPropertyCharString = fpCallbackGetPropertyCharString(CallbackGetPropertyCharString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyCharacterString( pyCallbackGetPropertyCharString )
    pyCallbackGetPropertyDate = fpCallbackGetPropertyDate(CallbackGetPropertyDate)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDate( pyCallbackGetPropertyDate )
    pyCallbackGetPropertyDouble = fpCallbackGetPropertyDouble(CallbackGetPropertyDouble)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDouble( pyCallbackGetPropertyDouble )
    pyCallbackGetPropertyEnum = fpCallbackGetPropertyEnum(CallbackGetPropertyEnumerated)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyEnumerated( pyCallbackGetPropertyEnum )
    pyCallbackGetPropertyOctetString = fpCallbackGetPropertyOctetString(CallbackGetPropertyOctetString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyOctetString( pyCallbackGetPropertyOctetString )
    pyCallbackGetPropertyInt = fpCallbackGetPropertyInt(CallbackGetPropertyInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertySignedInteger( pyCallbackGetPropertyInt )
    pyCallbackGetPropertyReal = fpCallbackGetPropertyReal(CallbackGetPropertyReal)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyReal( pyCallbackGetPropertyReal )
    pyCallbackGetPropertyTime = fpCallbackGetPropertyTime(CallbackGetPropertyTime)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyTime( pyCallbackGetPropertyTime )
    pyCallbackGetPropertyUInt = fpCallbackGetPropertyUInt(CallbackGetPropertyUInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyUnsignedInteger( pyCallbackGetPropertyUInt )
    



    # 4. Setup the BACnet device
	# ---------------------------------------------------------------------------
    print( "FYI: Setting up server Device. device.instance=[%d]" %( db["device"]["instance"] ))
    if( CASBACnetStack.BACnetStack_AddDevice(db["device"]["instance"]) == False ):
        print( "Error: Failed to add Device")
        exit() 

    # Enable optional BACnet services.
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"], casbacnetstack_service['readPropertyMultiple'], True )
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"], casbacnetstack_service['subscribeCov'], True )
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"], casbacnetstack_service['subscribeCovProperty'], True )
    
    # Add Objects
	# ---------------------------------------
    # AnalogInput (AI) 
    print( "FYI: Adding AnalogInput. AnalogInput.instance=[%d]" %(db["analogInput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogInput"], db["analogInput"]["instance"]) == False ):
        print( "Error: Failed to add analogInput")
        exit() 

    # BinaryInput (BI) 
    print( "FYI: Adding BinaryInput. BinaryInput.instance=[%d]" %(db["binaryInput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryInput"], db["binaryInput"]["instance"]) == False ):
        print( "Error: Failed to add BinaryInput")
        exit() 

    # MultiStateInput (MSI) 
    print( "FYI: Adding MultiStateInput. MultiStateInput.instance=[%d]" %(db["multiStateInput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateInput"], db["multiStateInput"]["instance"]) == False ):
        print( "Error: Failed to add MultiStateInput")
        exit() 

    # analogOutput
    print( "FYI: Adding analogOutput. analogOutput.instance=[%d]" %(db["analogOutput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogOutput"], db["analogOutput"]["instance"]) == False ):
        print( "Error: Failed to add analogOutput")
        exit() 
    
    # analogValue
    print( "FYI: Adding analogValue. analogValue.instance=[%d]" %(db["analogValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogValue"], db["analogValue"]["instance"]) == False ):
        print( "Error: Failed to add analogValue")
        exit() 

    # binaryOutput
    print( "FYI: Adding binaryOutput. binaryOutput.instance=[%d]" %(db["binaryOutput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryOutput"], db["binaryOutput"]["instance"]) == False ):
        print( "Error: Failed to add binaryOutput")
        exit() 

    # binaryValue
    print( "FYI: Adding binaryValue. binaryValue.instance=[%d]" %(db["binaryValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryValue"], db["binaryValue"]["instance"]) == False ):
        print( "Error: Failed to add binaryValue")
        exit() 

    # multiStateOutput
    print( "FYI: Adding multiStateOutput. multiStateOutput.instance=[%d]" %(db["multiStateOutput"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateOutput"], db["multiStateOutput"]["instance"]) == False ):
        print( "Error: Failed to add multiStateOutput")
        exit() 

    # multiStateValue
    print( "FYI: Adding multiStateOutput. multiStateValue.instance=[%d]" %(db["multiStateValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateValue"], db["multiStateValue"]["instance"]) == False ):
        print( "Error: Failed to add multiStateValue")
        exit()

    # characterstringValue
    print( "FYI: Adding characterstringValue. characterstringValue.instance=[%d]" %(db["characterstringValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["characterstringValue"], db["characterstringValue"]["instance"]) == False ):
        print( "Error: Failed to add characterstringValue")
        exit() 

    # integerValue
    print( "FYI: Adding integerValue. integerValue.instance=[%d]" %(db["integerValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["integerValue"], db["integerValue"]["instance"]) == False ):
        print( "Error: Failed to add integerValue")
        exit() 

    # largeAnalogValue
    print( "FYI: Adding largeAnalogValue. largeAnalogValue.instance=[%d]" %(db["largeAnalogValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["largeAnalogValue"], db["largeAnalogValue"]["instance"]) == False ):
        print( "Error: Failed to add largeAnalogValue")
        exit() 

    # positiveIntegerValue
    print( "FYI: Adding positiveIntegerValue. positiveIntegerValue.instance=[%d]" %(db["positiveIntegerValue"]["instance"]) )
    if( CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["positiveIntegerValue"], db["positiveIntegerValue"]["instance"]) == False ):
        print( "Error: Failed to add positiveIntegerValue")
        exit()
     
    # 5. Send I-Am of this device
	# ---------------------------------------------------------------------------
    print( "FYI: Sending I-AM broadcast" )
    print( "     WARN: TODO" )

    # 6. Start the main loop
    # ---------------------------------------------------------------------------
    print( "FYI: Entering main loop..." )
    while True:
        # Call the DLLs loop function which checks for messages and processes them.
        CASBACnetStack.BACnetStack_Tick()

        # Sleep between loops. Give some time to other application 
        time.sleep(0.1)

        # Every x seconds incurment the AnalogInput presentValue property by 0.1 
        if lastTimeValueWasUpdated + 1 < time.time():
            lastTimeValueWasUpdated = time.time()
            db["analogInput"]["presentValue"] += 0.1 
            print( "FYI: Updating AnalogInput (0) PresentValue: ", round( db["analogInput"]["presentValue"], 1) )


