# CAS BACnet Stack Python Server Example 
# https://github.com/chipkin/BACnetServerExamplePython 
#
import ctypes
import pathlib
import netifaces
import dns.resolver     # Package name: dnspython
import socket
import time  # Sleep function
from CASBACnetStackAdapter import *  # Contains all the Enumerations, and callback prototypes

# Example database
# -----------------------------------------------------------------------------
# This is an example database. Normally this data would come from your sensor/database
#
# Units.
# no_units (95),
# degreescelsius (62)
# ...
#
# Reliability
# no-fault-detected (0),
# no-sensor (1)
# ...

db = {
    "device": {
        "instance": 389001,
        "objectName": "Device Rainbow",
        "vendorname": "Example Chipkin Automation Systems",
        "vendoridentifier": 0},
    "analogInput": {
        "instance": 0,
        "objectName": "AnalogInput Bronze",
        "presentValue": 99.6,
        "units": 62,
        "reliability": 1},
    "binaryInput": {
        "instance": 3,
        "objectName": "BinaryInput Emerald",
        "presentValue": 1,
        "reliability": 1},
    "multiStateInput": {
        "instance": 13,
        "objectName": "MultiStateInput Hot Pink",
        "presentValue": 3},
    "analogOutput": {
        "instance": 1,
        "objectName": "AnalogOutput Chartreuse",
        "presentValue": 1},
    "analogValue": {
        "instance": 2,
        "objectName": "AnalogValue Diamond",
        "presentValue": 1},
    "binaryOutput": {
        "instance": 4,
        "objectName": "BinaryOutput Fuchsia",
        "presentValue": 1},
    "binaryValue": {
        "instance": 5,
        "objectName": "BinaryValue Gold",
        "presentValue": 1},
    "multiStateOutput": {
        "instance": 14,
        "objectName": "MultiStateOutput Indigo",
        "presentValue": 1},
    "multiStateValue": {
        "instance": 15,
        "objectName": "MultiStateValue Kiwi",
        "presentValue": 1},
    "characterstringValue": {
        "instance": 40,
        "objectName": "CharacterstringValue Nickel",
        "presentValue": 1},
    "integerValue": {
        "instance": 45,
        "objectName": "IntegerValue Purple",
        "presentValue": 1},
    "largeAnalogValue": {
        "instance": 46,
        "objectName": "LargeAnalogValue Quartz",
        "presentValue": 1},
    "positiveIntegerValue": {
        "instance": 48,
        "objectName": "PositiveIntegerValue Silver",
        "presentValue": 1},
    "networkPort": {
        "instance": 50,
        "objectName": "NetworkPort Vermillion",
        "BACnetIPUDPPort": 47808,
        "ipLength": 4,
        "ipAddress": [192, 168, 1, 199],
        "ipDefaultGateway": [192, 168, 1, 99],
        "ipDnsServer": [1, 2, 3, 4, 5],
        "ipNumOfDns": 1,
        "ipSubnetMask": [255, 255, 255, 0],
        "FdBbmdAddressHostIp": [192, 168, 1, 4],
        "FdBbmdAddressHostType": 1,  # 0 = None, 1 = IpAddress, 2 = Name
        "FdBbmdAddressPort": 47808,
        "FdSubscriptionLifetime": 3000,
        "changesPending": False}
}

# Globals
# -----------------------------------------------------------------------------
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lastTimeValueWasUpdated = 0


def octetStringCopy(source, destination, length, offset=0):
    for i in range(length):
        destination[i + offset] = source[i]


# Rebuilds password string from ctype.c_uint_8 arrray
def rebuildPassword(passwordPointer, length):
    password = ""
    for i in range(0, length):
        password = password + chr(passwordPointer[i])
    return password


# Callbacks
# -----------------------------------------------------------------------------
def CallbackReceiveMessage(message, maxMessageLength, receivedConnectionString, maxConnectionStringLength,
                           receivedConnectionStringLength, networkType):
    try:
        data, addr = udpSocket.recvfrom(maxMessageLength)
        # if not data:
        #     print("DEBUG: not data")
        # A message was received.
        # print ("DEBUG: CallbackReceiveMessage. Message Received", addr, data, len(data) )

        # Convert the received address to the CAS BACnet Stack connection string format.
        ip_as_bytes = bytes(map(int, addr[0].split(".")))
        for i in range(len(ip_as_bytes)):
            receivedConnectionString[i] = ip_as_bytes[i]
        # UDP Port
        receivedConnectionString[4] = int(addr[1] / 256)
        receivedConnectionString[5] = addr[1] % 256
        # New ConnectionString Length
        receivedConnectionStringLength[0] = 6

        # Convert the received data to a format that CAS BACnet Stack can process.
        for i in range(len(data)):
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


def CallbackSendMessage(message, messageLength, connectionString, connectionStringLength, networkType, broadcast):
    # Currently we are only supporting IP
    if networkType != casbacnetstack_networkType["ip"]:
        print("Error: Unsupported network type. networkType:", networkType)
        return 0

    # Extract the Connection String from CAS BACnet Stack into an IP address and port.
    udpPort = connectionString[4] * 256 + connectionString[5]
    if broadcast:
        # Use broadcast IP address
        # ToDo: Get the subnet mask and apply it to the IP address
        print("DEBUG:   ToDo: Broadcast this message. Local IP: ", db["networkPort"]["ipAddress"],
              "Subnet: ", db["networkPort"]["ipSubnetMask"], "Broadcast IP: ????")
        ipAddress = f"{connectionString[0]:.0f}.{connectionString[1]:.0f}." \
                    f"{connectionString[2]:.0f}.{connectionString[3]:.0f}"
    else:
        ipAddress = f"{connectionString[0]:.0f}.{connectionString[1]:.0f}." \
                    f"{connectionString[2]:.0f}.{connectionString[3]:.0f}"

    # Extract the message from CAS BACnet Stack to a bytearray
    data = bytearray(messageLength)
    for i in range(len(data)):
        data[i] = message[i]

    # Send the message
    udpSocket.sendto(data, (ipAddress, udpPort))
    return messageLength


def CallbackGetSystemTime():
    return int(time.time())


def CallbackGetPropertyReal(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                            propertyArrayIndex):
    print("CallbackGetPropertyReal", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["presentValue"]:
            if objectType == bacnet_objectType["analogInput"] and objectInstance == db["analogInput"]["instance"]:
                value[0] = ctypes.c_float(db["analogInput"]["presentValue"])
                return True

    # Return false. The CAS BACnet Stack will use a default value.
    return False


def CallbackGetPropertyCharString(deviceInstance, objectType, objectInstance, propertyIdentifier, value,
                                  valueElementCount, maxElementCount, encodingType, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyCharString", deviceInstance, objectType, objectInstance, propertyIdentifier,
          maxElementCount, useArrayIndex, propertyArrayIndex)

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["vendorname"] and objectType == bacnet_objectType["device"]:
            vendorname = db["device"]["vendorname"]
            # Convert the vendorname from a string to a format that CAS BACnet Stack can process.
            b_vendorname = vendorname.encode("utf-8")
            for i in range(len(b_vendorname)):
                value[i] = b_vendorname[i]
            # Define how long the vendorname is
            valueElementCount[0] = len(b_vendorname)
            return True
        elif propertyIdentifier == bacnet_propertyIdentifier["objectname"]:
            if objectType == bacnet_objectType["analogInput"] and objectInstance == db["analogInput"]["instance"]:
                objectName = db["analogInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process.
                b_objectName = objectName.encode("utf-8")
                for i in range(len(b_objectName)):
                    value[i] = b_objectName[i]
                # Define how long the Object name is
                valueElementCount[0] = len(b_objectName)
                return True
            elif objectType == bacnet_objectType["binaryInput"] and objectInstance == db["binaryInput"]["instance"]:
                objectName = db["binaryInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process.
                b_objectName = objectName.encode("utf-8")
                for i in range(len(b_objectName)):
                    value[i] = b_objectName[i]
                # Define how long the Object name is
                valueElementCount[0] = len(b_objectName)
                return True
            elif objectType == bacnet_objectType["multiStateInput"] \
                    and objectInstance == db["multiStateInput"]["instance"]:
                objectName = db["multiStateInput"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process.
                b_objectName = objectName.encode("utf-8")
                for i in range(len(b_objectName)):
                    value[i] = b_objectName[i]
                # Define how long the Object name is
                valueElementCount[0] = len(b_objectName)
                return True
            elif objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                objectName = db["networkPort"]["objectName"]
                # Convert the Object Name from a string to a format that CAS BACnet Stack can process.
                b_objectName = objectName.encode("utf-8")
                for i in range(len(b_objectName)):
                    value[i] = b_objectName[i]
                # Define how long the Object Name  is
                valueElementCount[0] = len(b_objectName)
                return True

    # Return false. The CAS BACnet Stack will use a default value.
    return False


def ValueToKey(enumeration, searchValue):
    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    for key, value in enumeration.items():
        if value == searchValue:
            return key
    return "key doesn't exist"


def CallbackGetPropertyEnumerated(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                                  propertyArrayIndex):
    print("CallbackGetPropertyEnumerated", deviceInstance, objectType, objectInstance, propertyIdentifier,
          propertyArrayIndex)

    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["presentValue"]:
            if objectType == bacnet_objectType["binaryInput"] and objectInstance == db["binaryInput"]["instance"]:
                value[0] = ctypes.c_uint32(db["binaryInput"]["presentValue"])
                return True
        elif propertyIdentifier == bacnet_propertyIdentifier["units"]:
            if ValueToKey(bacnet_objectType, objectType) in db:
                if "units" in db[ValueToKey(bacnet_objectType, objectType)]:
                    value[0] = ctypes.c_uint32(db[ValueToKey(bacnet_objectType, objectType)]["units"])
                    return True
        elif propertyIdentifier == bacnet_propertyIdentifier["reliability"]:
            if ValueToKey(bacnet_objectType, objectType) in db:
                if "units" in db[ValueToKey(bacnet_objectType, objectType)]:
                    value[0] = ctypes.c_uint32(db[ValueToKey(bacnet_objectType, objectType)]["reliability"])
                    return True

            # Undefined reliability. Assume no-fault-detected (0)
            value[0] = ctypes.c_uint32(0)
            return True
        elif propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                value[0] = db["networkPort"]["FdBbmdAddressHostType"]
                return True

    # Return false. The CAS BACnet Stack will use a default value.
    return False


def CallbackGetPropertyBitString(deviceInstance, objectType, objectInstance, propertyIdentifier, value,
                                 valueElementCount, maxElementCount, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyBitString", deviceInstance, objectType, objectInstance, propertyIdentifier,
          maxElementCount, useArrayIndex, propertyArrayIndex)
    return False


def CallbackGetPropertyBool(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                            propertyArrayIndex):
    print("CallbackGetPropertyBool", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["changespending"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                value[0] = db["networkPort"]["changesPending"]
                return True
    return False


def CallbackGetPropertyDate(deviceInstance, objectType, objectInstance, propertyIdentifier, year, month, day, weekday,
                            useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyDate", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    return False


def CallbackGetPropertyDouble(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                              propertyArrayIndex):
    print("CallbackGetPropertyDouble", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    return False


def CallbackGetPropertyOctetString(deviceInstance, objectType, objectInstance, propertyIdentifier, value,
                                   valueElementCount, maxElementCount, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyOctetString", deviceInstance, objectInstance, propertyIdentifier, maxElementCount,
          useArrayIndex, propertyArrayIndex)
    if propertyIdentifier == bacnet_propertyIdentifier["ipaddress"]:
        if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
            valueElementCount[0] = db["networkPort"]["ipLength"]
            octetStringCopy(db["networkPort"]["ipAddress"], value, valueElementCount[0])
            print(f"DEBUG: IN GET IP: output = {value[0]}.{value[1]}.{value[2]}.{value[3]}")
            return True
    elif propertyIdentifier == bacnet_propertyIdentifier["ipdefaultgateway"]:
        if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
            valueElementCount[0] = db["networkPort"]["ipLength"]
            octetStringCopy(db["networkPort"]["ipDefaultGateway"], value, valueElementCount[0])
            return True
    elif propertyIdentifier == bacnet_propertyIdentifier["ipsubnetmask"]:
        if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
            valueElementCount[0] = db["networkPort"]["ipLength"]
            octetStringCopy(db["networkPort"]["ipSubnetMask"], value, valueElementCount[0])
            return True
    elif propertyIdentifier == bacnet_propertyIdentifier["ipdnsserver"]:
        if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
            valueElementCount[0] = db["networkPort"]["ipNumOfDns"] * 4
            for i in range(db["networkPort"]["ipNumOfDns"]):
                octetStringCopy(db["networkPort"]["ipDnsServer"][i], value, 4, i * 4)
            return True
    elif propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
        if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
            valueElementCount[0] = db["networkPort"]["ipLength"]
            octetStringCopy(db["networkPort"]["FdBbmdAddressHostIp"], value, valueElementCount[0])
            return True
    return False


def CallbackGetPropertyInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                           propertyArrayIndex):
    print("CallbackGetPropertyInt", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    return False


def CallbackGetPropertyTime(deviceInstance, objectType, objectInstance, propertyIdentifier, hour, minute, second,
                            hundrethSeconds, useArrayIndex, propertyArrayIndex):
    print("CallbackGetPropertyTime", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    return False


def CallbackGetPropertyUInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                            propertyArrayIndex):
    print("CallbackGetPropertyUInt", deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex,
          propertyArrayIndex)
    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["vendoridentifier"]:
            if objectType == bacnet_objectType["device"]:
                value[0] = ctypes.c_uint32(db["device"]["vendoridentifier"])
                return True
        elif propertyIdentifier == bacnet_propertyIdentifier["bacnetipudpport"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                value[0] = db["networkPort"]["BACnetIPUDPPort"]
                return True
        # Network Port Object IP DNS Server Array Size property
        elif propertyIdentifier == bacnet_propertyIdentifier["ipdnsserver"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                if useArrayIndex and propertyArrayIndex == 0:
                    value[0] = db["networkPort"]["ipNumOfDns"]
                    return True
        elif propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                if useArrayIndex and propertyArrayIndex == casbacnetstack_fdBbmdAddressOffset["port"]:
                    value[0] = db["networkPort"]["FdBbmdAddressPort"]
                    return True
        elif propertyIdentifier == bacnet_propertyIdentifier["fdsubscriptionlifetime"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                value[0] = db["networkPort"]["FdSubscriptionLifetime"]
                return True
    return False


def CallbackSetPropertyUInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex,
                            propertyArrayIndex, priority, errorCode):
    print("CallbackSetPropertyUInt", deviceInstance, objectType, objectInstance, propertyIdentifier, value,
          useArrayIndex, propertyArrayIndex, priority, errorCode)
    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                db["networkPort"]["FdBbmdAddressPort"] = value
                db["networkPort"]["changesPending"] = True
                return True

        elif propertyIdentifier == bacnet_propertyIdentifier["fdsubscriptionlifetime"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                db["networkPort"]["FdSubscriptionLifetime"] = value
                db["networkPort"]["changesPending"] = True
                return True
    return False


def CallbackSetPropertyOctetString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, length,
                                   useArrayIndex, propertyArray, priority, errorCode):
    print("CallbackSetPropertyOctetString", deviceInstance, objectType, objectInstance, propertyIdentifier, value,
          length, useArrayIndex, propertyArray, priority, errorCode)
    if deviceInstance == db["device"]["instance"]:
        if propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == db["networkPort"]["instance"]:
                db["networkPort"]["FdBbmdAddressHostIp"][0] = value[0]
                db["networkPort"]["FdBbmdAddressHostIp"][1] = value[1]
                db["networkPort"]["FdBbmdAddressHostIp"][2] = value[2]
                db["networkPort"]["FdBbmdAddressHostIp"][3] = value[3]
                db["networkPort"]["changesPending"] = False
                return True
    return False


def CallbackReinitializeDevice(deviceInstance, reinitializedState, password, passwordLength, errorCode):
    # Rebuild password from pointer reference
    derefedPassword = rebuildPassword(password, passwordLength)

    print("CallbackReinitializeDevice", deviceInstance, reinitializedState, derefedPassword, passwordLength,
          errorCode[0])

    # This callback is called when this BACnet Server device receives a ReinitializeDevice message
    # In this callback, you will handle the reinitializedState
    # If reinitializedState = ACTIVATE_CHANGES (7) then you will apply any network port changes and store the values in
    #   non-volatile memory
    # If reinitializedState = WARM_START(1) then you will apply any network port changes, store the values in
    #   non-volatile memory, and restart the device

    # Before handling the reinitializedState, first check the password.
    # If your device does not require a password, then ignore any password passed in.
    # Otherwise, validate the password.
    #       If password invalid: set errorCode to PasswordInvalid (26)
    #       If password is required, but no password was provided: set errorCode to MissingRequiredParameter (16)
    # In this example, a password of 12345 is required

    # Check password before handling reinitialization
    if derefedPassword == "" or passwordLength == 0:
        errorCode[0] = bacnet_errorCode["missing-required-parameter"]
        return False
    # Require password to be 12345 for the example
    if derefedPassword != "12345":
        errorCode[0] = bacnet_errorCode["password-failure"]
        return False

    # In this example, only the NetworkPort Object FdBbmdAddress and FdSubscriptionLifetime properties are writable and
    #   need to be stored in non-volatile memory.  For the purpose of this example, we will not storing these values in
    #   non-volatile memory.

    # 1. Store values that must be stored in non-volatile memory (i.e. must survive a reboot)

    # 2. Apply any Network Port values that have been written to
    # If any validation on the Network Port values fails, set errorCode to INVALID_CONFIGURATION_DATA (46)

    # 3. Set Network Port ChangesPending property to false

    # 4. Handle ReinitializedState. If ACTIVATE_CHANGES, no other action, return true
    #                               If WARM_START, prepare device for reboot, return true. and reboot
    # NOTE: Must return True first before rebooting so the stack sends the SimpleAck
    if reinitializedState == casbacnetstack_reinitializeState["state-activate-changes"]:
        db["networkPort"]["changesPending"] = False
        return True
    elif reinitializedState == casbacnetstack_reinitializeState["state-warm-start"]:
        # Flag for reboot and handle reboot after stack responds with SimpleAck
        db["networkPort"]["changesPending"] = False
        errorCode[0] = 2
        return True
    else:
        # All other states are not supported in this example
        errorCode[0] = bacnet_errorCode["optional-functionality-not-supported"]
        return False


def CallbackDeviceCommunicationControl(deviceInstance, enableDisable, password, passwordLength, useTimeDuration,
                                       timeDuration, errorCode):
    # Rebuild password from pointer reference
    derefedPassword = rebuildPassword(password, passwordLength)

    print("CallbackDeviceCommunicationControl", deviceInstance, enableDisable, derefedPassword, passwordLength,
          useTimeDuration, timeDuration, errorCode[0])

    # This callback is called when this BACnet Server device receives a DeviceCommunicationControl message
    # In this callback, you will handle the password. All other parameters are purely for logging to know
    # what parameters the DeviceCommunicationControl request had

    # To handle the password:
    # If your device does not require a password, then ignore any password passed in
    # Otherwise, validate the password
    #       If password invalid: set errorCode to PasswordInvalid (26)
    #       If password is required, but no password was provided: set errorCode to MissingRequiredParameter (16)
    # In this example, a password of 12345 is required

    # Check password
    if derefedPassword == "" or passwordLength == 0:
        errorCode[0] = bacnet_errorCode["missing-required-parameter"]
        return False
    # Require password to be 12345 for the example
    if derefedPassword != "12345":
        errorCode[0] = bacnet_errorCode["password-failure"]
        return False

    # Return true to allow DeviceCommunicationControl logic to continue
    return True


# Main application
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("FYI: CAS BACnet Stack Python Server Example v0.0.4")
    print("FYI: https://github.com/chipkin/BACnetServerExamplePython")

    # 1. Load the CAS BACnet stack functions
    # ---------------------------------------------------------------------------
    # Load the shared library into ctypes
    libpath = pathlib.Path().absolute() / libname
    CASBACnetStack = ctypes.CDLL(str(libpath), mode=ctypes.RTLD_GLOBAL)

    # Print the version information
    print(f"FYI: CAS BACnet Stack version: "
          f"{CASBACnetStack.BACnetStack_GetAPIMajorVersion():.0f}."
          f"{CASBACnetStack.BACnetStack_GetAPIMinorVersion():.0f}."
          f"{CASBACnetStack.BACnetStack_GetAPIPatchVersion():.0f}."
          f"{CASBACnetStack.BACnetStack_GetAPIBuildVersion():.0f}")
    print(f"FYI: CAS BACnet Stack python adapter version: {casbacnetstack_adapter_version}")

    # 2. Connect the UDP resource to the BACnet Port and get network info
    # ---------------------------------------------------------------------------
    print(f"FYI: Connecting UDP Resource to port=[{db['networkPort']['BACnetIPUDPPort']:.0f}]")
    HOST = ""  # Symbolic name meaning all available interfaces
    udpSocket.bind((HOST, db["networkPort"]["BACnetIPUDPPort"]))
    udpSocket.setblocking(False)

    # Load network information into database
    db["networkPort"]["ipAddress"] = [int(octet) for octet in netifaces.ifaddresses(netifaces.interfaces()[0])[netifaces.AF_INET][0]["addr"].split(".")]
    db["networkPort"]["ipSubnetMask"] = [int(octet) for octet in netifaces.ifaddresses(netifaces.interfaces()[0])[netifaces.AF_INET][0]["netmask"].split(".")]
    db["networkPort"]["ipDefaultGateway"] = [int(octet) for octet in netifaces.gateways()["default"][netifaces.AF_INET][0].split(".")]
    dnsServerOctetList = []
    for dnsServer in dns.resolver.Resolver().nameservers:
        dnsServerOctetList.append([int(octet) for octet in dnsServer.split(".")])
    db["networkPort"]["ipNumOfDns"] = len(dnsServerOctetList)
    db["networkPort"]["ipDnsServer"] = dnsServerOctetList

    print("FYI: Local IP address: ", db["networkPort"]["ipAddress"])

    # 3. Setup the callbacks
    # ---------------------------------------------------------------------------
    print("FYI: Registering the Callback Functions with the CAS BACnet Stack")

    # Note:
    # Make sure you keep references to CFUNCTYPE() objects as long as they are used from C code.
    # ctypes doesn't, and if you don"t, they may be garbage collected, crashing your program when
    # a callback is made
    #
    # Because of garbage collection, the pyCallback**** functions need to stay in scope.
    pyCallbackReceiveMessage = fpCallbackReceiveMessage(CallbackReceiveMessage)
    CASBACnetStack.BACnetStack_RegisterCallbackReceiveMessage(pyCallbackReceiveMessage)
    pyCallbackSendMessage = fpCallbackSendMessage(CallbackSendMessage)
    CASBACnetStack.BACnetStack_RegisterCallbackSendMessage(pyCallbackSendMessage)
    pyCallbackGetSystemTime = fpCallbackGetSystemTime(CallbackGetSystemTime)
    CASBACnetStack.BACnetStack_RegisterCallbackGetSystemTime(pyCallbackGetSystemTime)
    pyCallbackGetPropertyBitString = fpCallbackGetPropertyBitString(CallbackGetPropertyBitString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBitString(pyCallbackGetPropertyBitString)
    pyCallbackGetPropertyBool = fpCallbackGetPropertyBool(CallbackGetPropertyBool)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBool(pyCallbackGetPropertyBool)
    pyCallbackGetPropertyCharString = fpCallbackGetPropertyCharString(CallbackGetPropertyCharString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyCharacterString(pyCallbackGetPropertyCharString)
    pyCallbackGetPropertyDate = fpCallbackGetPropertyDate(CallbackGetPropertyDate)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDate(pyCallbackGetPropertyDate)
    pyCallbackGetPropertyDouble = fpCallbackGetPropertyDouble(CallbackGetPropertyDouble)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDouble(pyCallbackGetPropertyDouble)
    pyCallbackGetPropertyEnum = fpCallbackGetPropertyEnum(CallbackGetPropertyEnumerated)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyEnumerated(pyCallbackGetPropertyEnum)
    pyCallbackGetPropertyOctetString = fpCallbackGetPropertyOctetString(CallbackGetPropertyOctetString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyOctetString(pyCallbackGetPropertyOctetString)
    pyCallbackGetPropertyInt = fpCallbackGetPropertyInt(CallbackGetPropertyInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertySignedInteger(pyCallbackGetPropertyInt)
    pyCallbackGetPropertyReal = fpCallbackGetPropertyReal(CallbackGetPropertyReal)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyReal(pyCallbackGetPropertyReal)
    pyCallbackGetPropertyTime = fpCallbackGetPropertyTime(CallbackGetPropertyTime)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyTime(pyCallbackGetPropertyTime)
    pyCallbackGetPropertyUInt = fpCallbackGetPropertyUInt(CallbackGetPropertyUInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyUnsignedInteger(pyCallbackGetPropertyUInt)
    pyCallbackSetPropertyUInt = fpCallbackSetPropertyUInt(CallbackSetPropertyUInt)
    CASBACnetStack.BACnetStack_RegisterCallbackSetPropertyUnsignedInteger(pyCallbackSetPropertyUInt)
    pyCallbackSetPropertyOctetString = fpCallbackSetPropertyOctetString(CallbackSetPropertyOctetString)
    CASBACnetStack.BACnetStack_RegisterCallbackSetPropertyOctetString(pyCallbackSetPropertyOctetString)
    pyCallbackReinitializeDevice = fpCallbackReinitializeDevice(CallbackReinitializeDevice)
    CASBACnetStack.BACnetStack_RegisterCallbackReinitializeDevice(pyCallbackReinitializeDevice)
    pyCallbackDeviceCommunicationControl = fpCallbackDeviceCommunicationControl(CallbackDeviceCommunicationControl)
    CASBACnetStack.BACnetStack_RegisterCallbackDeviceCommunicationControl(pyCallbackDeviceCommunicationControl)

    # 4. Setup the BACnet device
    # ---------------------------------------------------------------------------
    print(f"FYI: Setting up server Device. device.instance=[{db['device']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddDevice(db["device"]["instance"]):
        print("Error: Failed to add Device")
        exit()

    # Enable optional BACnet services.
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["readPropertyMultiple"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["writeProperty"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["writePropertyMultiple"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["subscribeCov"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["subscribeCovProperty"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["reinitializeDevice"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["deviceCommunicationControl"], True)
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["iAm"])
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["confirmedTextMessage"])
    CASBACnetStack.BACnetStack_SetServiceEnabled(db["device"]["instance"],
                                                 casbacnetstack_service["unconfirmedTextMessage"])

    # Add Objects
    # ---------------------------------------
    # AnalogInput (AI)
    print(f"FYI: Adding AnalogInput. AnalogInput.instance=[{db['analogInput']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogInput"],
                                                db["analogInput"]["instance"]):
        print("Error: Failed to add analogInput")
        exit()

    # Enable optional properties
    CASBACnetStack.BACnetStack_SetPropertyEnabled(db["device"]["instance"], bacnet_objectType["analogInput"],
                                                  db["analogInput"]["instance"],
                                                  bacnet_propertyIdentifier["reliability"], True)

    # BinaryInput (BI)
    print(f"FYI: Adding BinaryInput. BinaryInput.instance=[{(db['binaryInput']['instance']):.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryInput"],
                                                db["binaryInput"]["instance"]):
        print("Error: Failed to add BinaryInput")
        exit()

    # MultiStateInput (MSI)
    print(f"FYI: Adding MultiStateInput. MultiStateInput.instance=[{(db['multiStateInput']['instance']):.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateInput"],
                                                db["multiStateInput"]["instance"]):
        print("Error: Failed to add MultiStateInput")
        exit()

    # analogOutput
    print(f"FYI: Adding analogOutput. analogOutput.instance=[{db['analogOutput']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogOutput"],
                                                db["analogOutput"]["instance"]):
        print("Error: Failed to add analogOutput")
        exit()

    # analogValue
    print(f"FYI: Adding analogValue. analogValue.instance=[{db['analogValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["analogValue"],
                                                db["analogValue"]["instance"]):
        print("Error: Failed to add analogValue")
        exit()

    # binaryOutput
    print(f"FYI: Adding binaryOutput. binaryOutput.instance=[{db['binaryOutput']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryOutput"],
                                                db["binaryOutput"]["instance"]):
        print("Error: Failed to add binaryOutput")
        exit()

    # binaryValue
    print(f"FYI: Adding binaryValue. binaryValue.instance=[{db['binaryValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["binaryValue"],
                                                db["binaryValue"]["instance"]):
        print("Error: Failed to add binaryValue")
        exit()

    # multiStateOutput
    print(f"FYI: Adding multiStateOutput. multiStateOutput.instance=[{db['multiStateOutput']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateOutput"],
                                                db["multiStateOutput"]["instance"]):
        print("Error: Failed to add multiStateOutput")
        exit()

    # multiStateValue
    print(f"FYI: Adding multiStateOutput. multiStateValue.instance=[{db['multiStateValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["multiStateValue"],
                                                db["multiStateValue"]["instance"]):
        print("Error: Failed to add multiStateValue")
        exit()

    # characterstringValue
    print(f"FYI: Adding characterstringValue. characterstringValue.instance="
          f"[{db['characterstringValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["characterstringValue"],
                                                db["characterstringValue"]["instance"]):
        print("Error: Failed to add characterstringValue")
        exit()

    # integerValue
    print(f"FYI: Adding integerValue. integerValue.instance=[{db['integerValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["integerValue"],
                                                db["integerValue"]["instance"]):
        print("Error: Failed to add integerValue")
        exit()

    # largeAnalogValue
    print(f"FYI: Adding largeAnalogValue. largeAnalogValue.instance=[{db['largeAnalogValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["largeAnalogValue"],
                                                db["largeAnalogValue"]["instance"]):
        print("Error: Failed to add largeAnalogValue")
        exit()

    # positiveIntegerValue
    print(f"FYI: Adding positiveIntegerValue. positiveIntegerValue.instance="
          f"[{db['positiveIntegerValue']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddObject(db["device"]["instance"], bacnet_objectType["positiveIntegerValue"],
                                                db["positiveIntegerValue"]["instance"]):
        print("Error: Failed to add positiveIntegerValue")
        exit()

    # networkPort
    print(f"FYI: Adding networkPort. networkPort.instance="
          f"[{db['networkPort']['instance']:.0f}]")
    if not CASBACnetStack.BACnetStack_AddNetworkPortObject(db["device"]["instance"], db["networkPort"]["instance"],
                                                           casbacnetstack_networkType["ipv4"],
                                                           casbacnetstack_protocolLevel["bacnet-application"],
                                                           casbacnetstack_network_port_lowest_protocol_level):
        print("Error: Failed to add networkPort")
        exit()
    if not CASBACnetStack.BACnetStack_SetPropertyEnabled(db["device"]["instance"],
                                                         bacnet_objectType["networkPort"],
                                                         db["networkPort"]["instance"],
                                                         bacnet_propertyIdentifier["fdbbmdaddress"], True):
        print("Error: Failed to enable fdBbmdAddress")
    if not CASBACnetStack.BACnetStack_SetPropertyEnabled(db["device"]["instance"],
                                                         bacnet_objectType["networkPort"],
                                                         db["networkPort"]["instance"],
                                                         bacnet_propertyIdentifier["fdsubscriptionlifetime"],
                                                         True):
        print("Error: Failed to enable fdSubscriptionLifetime")
    if not CASBACnetStack.BACnetStack_SetPropertyWritable(db["device"]["instance"], bacnet_objectType["networkPort"],
                                                          db["networkPort"]["instance"],
                                                          bacnet_propertyIdentifier["fdbbmdaddress"], True):
        print("Error: Failed to set fdBbmdAddress to writable")
    if not CASBACnetStack.BACnetStack_SetPropertyWritable(db["device"]["instance"], bacnet_objectType["networkPort"],
                                                          db["networkPort"]["instance"],
                                                          bacnet_propertyIdentifier["fdsubscriptionlifetime"], True):
        print("Error: Failed to set fdSubscriptionLifetime to writable")

    # 5. Send I-Am of this device
    # ---------------------------------------------------------------------------
    print("FYI: Sending I-AM broadcast")
    addressString = (ctypes.c_uint8 * 6)()
    octetStringCopy(db["networkPort"]["ipAddress"], addressString, 4)
    addressString[4] = int(db["networkPort"]["BACnetIPUDPPort"] / 256)
    addressString[5] = db["networkPort"]["BACnetIPUDPPort"] % 256

    if not CASBACnetStack.BACnetStack_SendIAm(ctypes.c_uint32(db["device"]["instance"]), ctypes.cast(addressString,
                                              ctypes.POINTER( ctypes.c_uint8)), ctypes.c_uint8(6),
                                              ctypes.c_uint8(casbacnetstack_networkType["ip"]), ctypes.c_bool(True),
                                              ctypes.c_uint16(65535), None, ctypes.c_uint8(0)):
        print("Error: Failed to send I-Am")

    # 6. Start the main loop
    # ---------------------------------------------------------------------------
    print("FYI: Entering main loop...")
    while True:
        # Call the DLLs loop function which checks for messages and processes them.
        CASBACnetStack.BACnetStack_Tick()

        # Sleep between loops. Give some time to other application
        time.sleep(0.1)

        # Every x seconds increment the AnalogInput presentValue property by 0.1
        if lastTimeValueWasUpdated + 1 < time.time():
            lastTimeValueWasUpdated = time.time()
            db["analogInput"]["presentValue"] += 0.1
            print("FYI: Updating AnalogInput (0) PresentValue: ", round(db["analogInput"]["presentValue"], 1))
