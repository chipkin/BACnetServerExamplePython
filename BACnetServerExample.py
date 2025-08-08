# CAS BACnet Stack Python Server Example
# https://github.com/chipkin/BACnetServerExamplePython
#
import BACnetServerExampleDatabase as db_module
import ctypes
import logging
import os
import pathlib
import sys
import netifaces
import dns.resolver  # Package name: dnspython
import socket
import time  # Sleep function
# Contains all the Enumerations, and callback prototypes
from CASBACnetStackAdapter import *

# Globals
# -----------------------------------------------------------------------------
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lastTimeValueWasUpdated = 0

BACnetDatabase = db_module.ExampleDatabase()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Example database
# -------------------------------------------------------------------------------------------------
# This is an example database. Normally this data would come from your
# sensor/database

DEVICE_INSTANCE = 389001
ANALOG_INPUT_BRONZE_INSTANCE = 0
ANALOG_OUTPUT_CHARTREUSE_INSTANCE = 1
ANALOG_VALUE_DIAMOND_INSTANCE = 2
BINARY_INPUT_EMERALD_INSTANCE = 3
BINARY_OUTPUT_FUCHSIA_INSTANCE = 4
BINARY_VALUE_GOLD_INSTANCE = 5
MULTISTATE_INPUT_HOTPINK_INSTANCE = 13
MULTISTATE_OUTPUT_INDIGO_INSTANCE = 14
MULTISTATE_VALUE_KIWI_INSTANCE = 15
CHARACTERSTRING_VALUE_NICKEL_INSTANCE = 40
INTEGER_VALUE_PURPLE_INSTANCE = 45
LARGE_ANALOG_VALUE_QUARTZ_INSTANCE = 46
POSITIVE_INTEGER_VALUE_SILVER_INSTANCE = 48
NETWORK_PORT_VERMILLION_INSTANCE = 56
MAX_BACNET_PRIORITY = 16

BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["device"], DEVICE_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "Device Rainbow")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["device"], DEVICE_INSTANCE,
                   bacnet_propertyIdentifier["vendorname"], "Example Chipkin Automation Systems")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["device"],
                   DEVICE_INSTANCE, bacnet_propertyIdentifier["vendoridentifier"], 0)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogInput"],
                   ANALOG_INPUT_BRONZE_INSTANCE, bacnet_propertyIdentifier["objectname"], "AnalogInput Bronze")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogInput"],
                   ANALOG_INPUT_BRONZE_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 99.6)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogInput"], ANALOG_INPUT_BRONZE_INSTANCE,
                   bacnet_propertyIdentifier["units"], bacnet_engineeringUnits["degreescelsius"])
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryInput"], BINARY_INPUT_EMERALD_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "BinaryInput Emerald")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryInput"],
                   BINARY_INPUT_EMERALD_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateInput"], MULTISTATE_INPUT_HOTPINK_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "MultiStateInput Hot Pink")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateInput"],
                   MULTISTATE_INPUT_HOTPINK_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 3)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogOutput"], ANALOG_OUTPUT_CHARTREUSE_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "AnalogOutput Chartreuse")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogOutput"], ANALOG_OUTPUT_CHARTREUSE_INSTANCE,
                   bacnet_propertyIdentifier["relinquishdefault"], "0.0")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogOutput"], ANALOG_OUTPUT_CHARTREUSE_INSTANCE,
                   bacnet_propertyIdentifier["priorityarray"], [None] * MAX_BACNET_PRIORITY)
# Set one of the priority array elements
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogOutput"], ANALOG_OUTPUT_CHARTREUSE_INSTANCE,
                   bacnet_propertyIdentifier["priorityarray"], "1.11",True, 14)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogValue"], ANALOG_VALUE_DIAMOND_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "AnalogValue Diamond")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogValue"],
                   ANALOG_VALUE_DIAMOND_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryOutput"], BINARY_OUTPUT_FUCHSIA_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "BinaryOutput Fuchsia")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryOutput"], BINARY_OUTPUT_FUCHSIA_INSTANCE,
                   bacnet_propertyIdentifier["priorityarray"], [None] * MAX_BACNET_PRIORITY)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryOutput"],
                   BINARY_OUTPUT_FUCHSIA_INSTANCE, bacnet_propertyIdentifier["relinquishdefault"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryValue"],
                   BINARY_VALUE_GOLD_INSTANCE, bacnet_propertyIdentifier["objectname"], "BinaryValue Gold")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["binaryValue"],
                   BINARY_VALUE_GOLD_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateOutput"],
                   MULTISTATE_OUTPUT_INDIGO_INSTANCE, bacnet_propertyIdentifier["objectname"], "MultiStateOutput Indigo")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateOutput"], MULTISTATE_OUTPUT_INDIGO_INSTANCE,
                   bacnet_propertyIdentifier["priorityarray"], [None] * MAX_BACNET_PRIORITY)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateOutput"],
                   MULTISTATE_OUTPUT_INDIGO_INSTANCE, bacnet_propertyIdentifier["relinquishdefault"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateValue"],
                   MULTISTATE_VALUE_KIWI_INSTANCE, bacnet_propertyIdentifier["objectname"], "MultiStateValue Kiwi")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["multiStateValue"],
                   MULTISTATE_VALUE_KIWI_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["characterstringValue"],
                   CHARACTERSTRING_VALUE_NICKEL_INSTANCE, bacnet_propertyIdentifier["objectname"], "CharacterstringValue Nickel")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["characterstringValue"],
                   CHARACTERSTRING_VALUE_NICKEL_INSTANCE, bacnet_propertyIdentifier["presentvalue"], "hello world")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["integerValue"],
                   INTEGER_VALUE_PURPLE_INSTANCE, bacnet_propertyIdentifier["objectname"], "IntegerValue Purple")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["integerValue"],
                   INTEGER_VALUE_PURPLE_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["largeAnalogValue"],
                   LARGE_ANALOG_VALUE_QUARTZ_INSTANCE, bacnet_propertyIdentifier["objectname"], "LargeAnalogValue Quartz")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["largeAnalogValue"],
                   LARGE_ANALOG_VALUE_QUARTZ_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["positiveIntegerValue"],
                   POSITIVE_INTEGER_VALUE_SILVER_INSTANCE, bacnet_propertyIdentifier["objectname"], "PositiveIntegerValue Silver")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["positiveIntegerValue"],
                   POSITIVE_INTEGER_VALUE_SILVER_INSTANCE, bacnet_propertyIdentifier["presentvalue"], 1)
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE,
                   bacnet_propertyIdentifier["objectname"], "NetworkPort Vermillion")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                   NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["bacnetipudpport"], 47808)
BACnetDatabase.Save('db.json')

def octetStringCopy(source, destination, length, offset=0):
    for i in range(length):
        destination[i + offset] = source[i]

# Rebuilds string from ctype.c_uint_8 arrray


def rebuildString(strPointer, length):
    rebuiltStr = ""
    for i in range(0, length):
        rebuiltStr = rebuiltStr + chr(strPointer[i])
    return rebuiltStr


def ValueToKey(enumeration, searchValue):
    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    for key, value in enumeration.items():
        if value == searchValue:
            return key
    return "key doesn't exist"


# Callbacks
# -----------------------------------------------------------------------------
def CallbackReceiveMessage(message, maxMessageLength, receivedConnectionString, maxConnectionStringLength, receivedConnectionStringLength,
                           networkType):
    try:
        data, addr = udpSocket.recvfrom(maxMessageLength)
        # if not data:
        #     logger.debug("not data")
        # A message was received.
        logger.debug(
            "CallbackReceiveMessage. Message Received %s %s %s", addr, data, len(data))

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
        # No message, We are not waiting for a incoming message so our socket returns a BlockingIOError. This is normal.
        return 0

    # Catch all
    return 0


def CallbackSendMessage(message, messageLength, connectionString, connectionStringLength, networkType, broadcast):
    # Currently we are only supporting IP
    if networkType != casbacnetstack_networkType["ip"]:
        logger.error("Unsupported network type. networkType: %s", networkType)
        return 0

    # Extract the Connection String from CAS BACnet Stack into an IP address and port.
    udpPort = connectionString[4] * 256 + connectionString[5]
    ipAddress = f"{connectionString[0]:.0f}.{connectionString[1]:.0f}." f"{connectionString[2]:.0f}.{connectionString[3]:.0f}"
    if broadcast:
        # Use broadcast IP address
        ipAddress_list = GetBroadcastIPAddress()
        if ipAddress_list:
            ipAddress = f"{ipAddress_list[0]}.{ipAddress_list[1]}.{ipAddress_list[2]}.{ipAddress_list[3]}"
        logger.debug("Broadcast this message. Broadcast IP: %s", ipAddress)

    # Extract the message from CAS BACnet Stack to a bytearray
    data = bytearray(messageLength)
    for i in range(len(data)):
        data[i] = message[i]

    # Send the message
    udpSocket.sendto(data, (ipAddress, udpPort))
    return messageLength

def GetBroadcastIPAddress():
    ipaddress = BACnetDatabase.Get(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["ipaddress"])
    ipsubnetmask = BACnetDatabase.Get(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["ipsubnetmask"])

    if ipaddress is None or ipsubnetmask is None:
        logger.error("Failed to get IP address or subnet mask.")
        return None


    # The broadcast address is the IP address OR ipsubnetmask
    # IP Address: [169, 254, 83, 107], Subnet Mask: [255, 255, 0, 0]
    # Inverted mask: [0, 0, 255, 255], then OR with IP
    broadcast_address = [ipaddress[i] | ((~ipsubnetmask[i]) & 0xFF) for i in range(4)]

    # logger.debug("IP Address: %s, Subnet Mask: %s, Broadcast Address: %s", ipaddress, ipsubnetmask, broadcast_address)
    return broadcast_address


def CallbackGetSystemTime():
    return int(time.time())


def CallbackGetPropertyReal(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyReal deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False

    value[0] = ctypes.c_float(float(raw_value))
    return True


def CallbackGetPropertyCharString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount,
                                  encodingType, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyCharString deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False

    raw_value_encoded = raw_value.encode("utf-8")
    for i in range(len(raw_value_encoded)):
        value[i] = raw_value_encoded[i]
    valueElementCount[0] = len(raw_value_encoded)
    return True



def CallbackGetPropertyEnumerated(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyEnumerated deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False
    
    if propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
        value[0] = ctypes.c_uint32(int(1)) # 0 = None, 1 = IpAddress, 2 = Name
        return True

    value[0] = ctypes.c_uint32(int(raw_value))
    return True


def CallbackGetPropertyBitString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount,
                                 useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyBitString deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    return False


def CallbackGetPropertyBool(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyBool deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False
    
    # priorityarray is unique. What we are asking here is if
    # the value at the offset isNull.
    if useArrayIndex == True and propertyArrayIndex > 0 and propertyIdentifier == bacnet_propertyIdentifier["priorityarray"]:
        if raw_value == "None":
            # This indicates that the priority is not set
            value[0] = True 
            return True
        else:
            # This indicates that the priority is set as it has a value
            value[0] = False
            return True

    value[0] = bool(raw_value)
    return True


def CallbackGetPropertyDate(deviceInstance, objectType, objectInstance, propertyIdentifier, year, month, day, weekday, useArrayIndex,
                            propertyArrayIndex):
    logger.debug("CallbackGetPropertyDate deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    return False


def CallbackGetPropertyDouble(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyDouble deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False

    value[0] = ctypes.c_double(float(raw_value))
    return True


def CallbackGetPropertyOctetString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, valueElementCount, maxElementCount,
                                   useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyOctetString deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    
    SIZE_OF_IP_ADDRESS = 4

    if objectType == bacnet_objectType["networkPort"] and objectInstance == NETWORK_PORT_VERMILLION_INSTANCE:
        if propertyIdentifier == bacnet_propertyIdentifier["ipaddress"]:
            ip_addr = BACnetDatabase.Get(
                deviceInstance, objectType, objectInstance, bacnet_propertyIdentifier["ipaddress"])
            
            if ip_addr is not None:
                valueElementCount[0] = int(SIZE_OF_IP_ADDRESS)
                octetStringCopy(ip_addr, value, int(SIZE_OF_IP_ADDRESS))
                logger.debug("IN GET IP: output = %s.%s.%s.%s",
                             value[0], value[1], value[2], value[3])
                return True
        elif propertyIdentifier == bacnet_propertyIdentifier["ipdefaultgateway"]:
            ip_default_gateway = BACnetDatabase.Get(
                deviceInstance, objectType, objectInstance, bacnet_propertyIdentifier["ipdefaultgateway"])
            if ip_default_gateway is not None:
                valueElementCount[0] = int(SIZE_OF_IP_ADDRESS)
                octetStringCopy(ip_default_gateway, value, int(SIZE_OF_IP_ADDRESS))
                return True
        elif propertyIdentifier == bacnet_propertyIdentifier["ipsubnetmask"]:
            ip_subnet_mask = BACnetDatabase.Get(
                deviceInstance, objectType, objectInstance, bacnet_propertyIdentifier["ipsubnetmask"])
            if ip_subnet_mask is not None:
                valueElementCount[0] = int(SIZE_OF_IP_ADDRESS)
                octetStringCopy(ip_subnet_mask, value, int(SIZE_OF_IP_ADDRESS))
                return True
        elif propertyIdentifier == bacnet_propertyIdentifier["ipdnsserver"]:
            ip_dns_server = BACnetDatabase.Get(
                deviceInstance, objectType, objectInstance, bacnet_propertyIdentifier["ipdnsserver"])
            logger.debug("IP DNS Server: %s, ip_dns_server_size=%d", ip_dns_server, len(ip_dns_server))
            logger.debug("\n\n\n\n")
            
            # Example: [[1, 1, 1, 1], [192, 168, 3, 1]]
            # There are two DNS servers 
            # We need to copy each DNS server's IP address into the value array
            
            if ip_dns_server is not None:
                for i in range(len(ip_dns_server)):
                    logger.debug("Copying DNS server %d: %s", i, ip_dns_server[i])
                    octetStringCopy(ip_dns_server[i], value, SIZE_OF_IP_ADDRESS, i * SIZE_OF_IP_ADDRESS)
                return True

            
        elif propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            fdbbmd_address_host_ip = BACnetDatabase.Get(
                deviceInstance, objectType, objectInstance, bacnet_propertyIdentifier["fdbbmdaddress"])
            
            if fdbbmd_address_host_ip is not None:
                valueElementCount[0] = int(SIZE_OF_IP_ADDRESS)
                octetStringCopy(fdbbmd_address_host_ip, value, int(SIZE_OF_IP_ADDRESS))
                return True
    return False


def CallbackGetPropertyInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyInt deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False

    value[0] = ctypes.c_int32(int(raw_value))
    return True


def CallbackGetPropertyTime(deviceInstance, objectType, objectInstance, propertyIdentifier, hour, minute, second, hundrethSeconds, useArrayIndex,
                            propertyArrayIndex):
    logger.debug("CallbackGetPropertyTime deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    return False


def CallbackGetPropertyUInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex):
    logger.debug("CallbackGetPropertyUInt deviceInstance=%s objectType=%s objectInstance=%s propertyIdentifier=%s useArrayIndex=%s propertyArrayIndex=%s", deviceInstance, objectType,
                 objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)

    raw_value = BACnetDatabase.Get(
        deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex, propertyArrayIndex)
    if raw_value is None:
        logger.debug("Value not found in database. PropertyIdentifier: %s (%s)", ValueToKey(bacnet_propertyIdentifier, propertyIdentifier), propertyIdentifier)
        return False

    value[0] = ctypes.c_uint32(int(raw_value))
    return True


def CallbackSetPropertyUInt(deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex, priority,
                            errorCode):
    logger.debug("CallbackSetPropertyUInt %s %s %s %s %s %s %s %s %s", deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex, propertyArrayIndex,
                 priority, errorCode)

    return BACnetDatabase.Set(deviceInstance, objectType, deviceInstance, propertyIdentifier, value)


def CallbackSetPropertyOctetString(deviceInstance, objectType, objectInstance, propertyIdentifier, value, length, useArrayIndex, propertyArray,
                                   priority, errorCode):
    logger.debug("CallbackSetPropertyOctetString %s %s %s %s %s %s %s %s %s %s", deviceInstance, objectType, objectInstance, propertyIdentifier, value, length, useArrayIndex,
                 propertyArray, priority, errorCode)
    if deviceInstance == int(BACnetDatabase.Get(deviceInstance, bacnet_objectType["device"], deviceInstance, bacnet_propertyIdentifier["instance"])):
        if propertyIdentifier == bacnet_propertyIdentifier["fdbbmdaddress"]:
            if objectType == bacnet_objectType["networkPort"] and objectInstance == NETWORK_PORT_VERMILLION_INSTANCE:
                BACnetDatabase.Set(deviceInstance, objectType, objectInstance, "FdBbmdAddressHostIp", [
                                   value[0], value[1], value[2], value[3]])
                BACnetDatabase.Set(deviceInstance, objectType,
                                   objectInstance, "changesPending", False)
                return True
    return False


def CallbackReinitializeDevice(deviceInstance, reinitializedState, password, passwordLength, errorCode):
    # Rebuild password from pointer reference
    derefedPassword = rebuildString(password, passwordLength)

    logger.debug("CallbackReinitializeDevice %s %s %s %s %s", deviceInstance,
                 reinitializedState, derefedPassword, passwordLength, errorCode[0])

    # This callback is called when this BACnet Server device receives a ReinitializeDevice message
    # In this callback, you will handle the reinitializedState
    # If reinitializedState = ACTIVATE_CHANGES (7) then you will apply any network port changes and store the values in
    #   non-volatile memory
    # If reinitializedState = WARM_START(1) then you will apply any network port changes, store the values in
    #   non-volatile memory, and restart the device

    # Before handling the reinitializedState, first check the password.
    # If your device does not require a password, then ignore any password passed in.
    # Otherwise, validate the password.
    #       If password invalid, missing, or incorrect: set errorCode to PasswordInvalid (26)
    # In this example, a password of 12345 is required

    # Check password before handling reinitialization
    if passwordLength == 0 or derefedPassword != "12345":
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


def CallbackDeviceCommunicationControl(deviceInstance, enableDisable, password, passwordLength, useTimeDuration, timeDuration, errorCode):
    # Rebuild password from pointer reference
    derefedPassword = rebuildString(password, passwordLength)

    logger.debug("CallbackDeviceCommunicationControl %s %s %s %s %s %s %s", deviceInstance, enableDisable, derefedPassword, passwordLength, useTimeDuration, timeDuration,
                 errorCode[0])

    # This callback is called when this BACnet Server device receives a DeviceCommunicationControl message
    # In this callback, you will handle the password. All other parameters are purely for logging to know
    # what parameters the DeviceCommunicationControl request had

    # To handle the password:
    # If your device does not require a password, then ignore any password passed in
    # Otherwise, validate the password
    #       If password invalid, missing, or incorrect: set errorCode to PasswordInvalid (26)
    # In this example, a password of 12345 is required

    # Check password
    if passwordLength == 0 or derefedPassword != "12345":
        errorCode[0] = bacnet_errorCode["password-failure"]
        return False

    # Return true to allow DeviceCommunicationControl logic to continue
    return True


def CallbackLogDebugMessage(message, messageLength, messageType):
    # Rebuild message from pointer reference
    derefedMessage = rebuildString(message, messageLength)
    # logger.debug("CallbackLogDebugMessage %s %s %s", derefedMessage, messageLength, messageType)
    #
    # if derefedMessage != "" and messageLength != 0:
    #     logger.debug("CAS BACnet Stack DEBUG MESSAGE: %s", derefedMessage)


def AddAndConfigureNetworkPort(device_instance):
    logger.info("Adding networkPort. networkPort.instance=%s",
                NETWORK_PORT_VERMILLION_INSTANCE)
    if not CASBACnetStack.BACnetStack_AddNetworkPortObject(
        device_instance, 
        NETWORK_PORT_VERMILLION_INSTANCE,
        casbacnetstack_networkType["ipv4"],
        casbacnetstack_protocolLevel["bacnet-application"],
        casbacnetstack_network_port_lowest_protocol_level
    ):
        logger.error("Failed to add networkPort")
        exit()

    # Get the primary ethernet interface (filter out virtual adapters)
    def get_primary_interface():
        interfaces = netifaces.interfaces()
        logger.debug("Available interfaces: %s", interfaces)
        
        for interface in interfaces:
            # Skip common virtual interfaces
            interface_lower = interface.lower()
            if any(skip_name in interface_lower for skip_name in [
                'tailscale', 'loopback', 'vmware', 'virtualbox', 'vbox',
                'docker', 'wsl', 'hyper-v', 'bluetooth', 'teredo'
            ]):
                logger.debug("Skipping virtual interface: %s", interface)
                continue
            
            # Check if interface has IPv4 address
            try:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET not in addrs:
                    continue
                    
                ipv4_info = addrs[netifaces.AF_INET][0]
                ip_addr = ipv4_info.get('addr')
                
                if not ip_addr:
                    continue
                
                # Skip loopback addresses
                if ip_addr.startswith('127.'):
                    continue
                    
                # Skip Tailscale IP range (100.64.0.0/10)
                ip_parts = [int(x) for x in ip_addr.split('.')]
                if ip_parts[0] == 100 and 64 <= ip_parts[1] <= 127:
                    logger.debug("Skipping Tailscale IP range: %s", ip_addr)
                    continue
                
                # Skip other common virtual IP ranges
                if (ip_parts[0] == 169 and ip_parts[1] == 254):  # APIPA
                    logger.debug("Skipping APIPA address: %s", ip_addr)
                    continue
                
                logger.info("Selected primary interface: %s with IP: %s", interface, ip_addr)
                return interface
                
            except Exception as e:
                logger.debug("Error checking interface %s: %s", interface, e)
                continue
        
        # Fallback to first available interface if no suitable one found
        logger.warning("No suitable primary interface found, using first available")
        return interfaces[0] if interfaces else None

    primary_interface = get_primary_interface()
    if not primary_interface:
        logger.error("No network interface available")
        exit()

    # Load network information from the primary interface
    try:
        interface_info = netifaces.ifaddresses(primary_interface)
        ipv4_info = interface_info[netifaces.AF_INET][0]
        
        ip_address = [int(octet) for octet in ipv4_info["addr"].split(".")]
        subnet_mask = [int(octet) for octet in ipv4_info["netmask"].split(".")]
        
        # Get default gateway
        default_gateway = [int(octet) for octet in netifaces.gateways()[
            "default"][netifaces.AF_INET][0].split(".")]
        
        logger.info("Using interface: %s", primary_interface)
        logger.info("IP Address: %s", ".".join(map(str, ip_address)))
        logger.info("Subnet Mask: %s", ".".join(map(str, subnet_mask)))
        logger.info("Default Gateway: %s", ".".join(map(str, default_gateway)))
        
    except Exception as e:
        logger.error("Failed to get network information from interface %s: %s", primary_interface, e)
        exit()
    
    dnsServerOctetList = []
    for dnsServer in dns.resolver.Resolver().nameservers:
        dnsServerOctetList.append([int(octet)
                                  for octet in dnsServer.split(".")])
    logger.info("DNS Servers: %s", dnsServerOctetList)
        

    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["ipaddress"], ip_address)
    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["ipsubnetmask"], subnet_mask)
    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE,
                       bacnet_propertyIdentifier["ipdefaultgateway"], default_gateway)
    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["ipdnsserver"], dnsServerOctetList)
    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"],
                       NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["fdbbmdaddress"], [0,0,0,0])

    logger.info("Local IP address: %s", ip_address)
    
def SendIAmBroadcast():
    ipAddress = GetBroadcastIPAddress()
    udpPort = int(BACnetDatabase.Get(
        DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["bacnetipudpport"]))
    if ipAddress is None or udpPort is None:
        logger.error(
            "Missing IP address or UDP port. Can not send I-AM broadcast")
        return

    logger.info("Sending I-AM broadcast ipAddress: %s, udpPort: %s", ipAddress, udpPort)

    # Convert the IP Address and UDP Port to a byte string that can be used by the CAS BACnet Stack
    addressString = (ctypes.c_uint8 * 6)()
    octetStringCopy(ipAddress, addressString, 4)
    addressString[4] = int(udpPort / 256)
    addressString[5] = int(udpPort % 256)

    if not CASBACnetStack.BACnetStack_SendIAm(
            ctypes.c_uint32(DEVICE_INSTANCE),
            ctypes.cast(addressString, ctypes.POINTER(ctypes.c_uint8)),
            ctypes.c_uint8(6),
            ctypes.c_uint8(casbacnetstack_networkType["ip"]),
            ctypes.c_bool(True),
            ctypes.c_uint16(65535),
            None,
            ctypes.c_uint8(0)):
        logger.error("Failed to send I-Am")


def AddObjectsFromDatabase(objectList):
    for obj in objectList:
        objectType, objectInstance = obj
        if objectType == bacnet_objectType["device"] or objectType == bacnet_objectType["networkPort"]:
            # Network port object already added above
            continue

        # Add the object to the BACnet stack
        if not CASBACnetStack.BACnetStack_AddObject(DEVICE_INSTANCE, objectType, objectInstance):
            logger.error("Failed to add object. Type=%s Instance=%s",
                         objectType, objectInstance)
            exit()

        # Print a message to the log
        # Look up the object type by the id in the bacnet_objectType dictionary
        if objectType in bacnet_objectType.values():
            objectTypeName = [
                name for name, value in bacnet_objectType.items() if value == objectType][0]
            logger.info("Added object. %s (%s)",
                        objectTypeName, objectInstance)


def ConnectToSocket(udp_port):
    logger.info("Connecting UDP Resource to port=%s", udp_port)
    HOST = ""  # Symbolic name meaning all available interfaces
    udpSocket.bind((HOST, udp_port))
    udpSocket.setblocking(False)


def updateValues():
    presentValue = float(BACnetDatabase.Get(
        DEVICE_INSTANCE, bacnet_objectType["analogInput"], ANALOG_INPUT_BRONZE_INSTANCE, bacnet_propertyIdentifier["presentvalue"]))
    presentValue += 0.1
    BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["analogInput"],
                       ANALOG_INPUT_BRONZE_INSTANCE, bacnet_propertyIdentifier["presentvalue"], presentValue)
    # Notify the stack that this data point was updated so the stack can check for logic
    # 		that may need to run on the data.  Example: check if COV (change of value) occurred.
    if CASBACnetStack.BACnetStack_ValueUpdated is not None:
        CASBACnetStack.BACnetStack_ValueUpdated(
            DEVICE_INSTANCE, bacnet_objectType["analogValue"], ANALOG_INPUT_BRONZE_INSTANCE, bacnet_propertyIdentifier["presentvalue"])
    logger.info("Updating AnalogInput (0) PresentValue: %s",
                round(presentValue, 1))


    # Main application
    # -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("FYI: CAS BACnet Stack Python Server Example v0.1.0")
    print("FYI: https://github.com/chipkin/BACnetServerExamplePython")

    # 0. Check for required dependencies: Python version, BACnet Stack DLL and required packages
    #    for this example
    # ---------------------------------------------------------------------------------------------
    # Check Python version
    if sys.version_info < (3, 7):
        logging.error("Python 3.7 or higher is required.")
        sys.exit(1)

    # Check for CASBACnetStack_x64_Release.dll
    dll_path = os.path.join(os.path.dirname(__file__),
                            'CASBACnetStack_x64_Release.dll')
    if not os.path.isfile(dll_path):
        logging.error(f"Missing required DLL: {dll_path}")
        sys.exit(1)

    # Check for required packages
    try:
        import ctypes
        import json
    except ImportError as e:
        logging.error(f"Missing required package: {e.name}")
        sys.exit(1)

    # 1. Load the CAS BACnet stack functions
    # ---------------------------------------------------------------------------------------------
    # Load the shared library into ctypes
    libpath = pathlib.Path().absolute() / libname
    logger.info("Library path: %s", libpath)
    CASBACnetStack = ctypes.CDLL(str(libpath), mode=ctypes.RTLD_GLOBAL)
    if not CASBACnetStack:
        logger.error("Failed to load CAS BACnet Stack library")
        sys.exit(1)

    # Print the version information
    logger.info("CAS BACnet Stack version: %s.%s.%s.%s",
                CASBACnetStack.BACnetStack_GetAPIMajorVersion(),
                CASBACnetStack.BACnetStack_GetAPIMinorVersion(),
                CASBACnetStack.BACnetStack_GetAPIPatchVersion(),
                CASBACnetStack.BACnetStack_GetAPIBuildVersion())
    logger.info("CAS BACnet Stack python adapter version: %s",
                casbacnetstack_adapter_version)

    # 2. Setup the callbacks
    # ---------------------------------------------------------------------------------------------
    logger.info("Registering the Callback Functions with the CAS BACnet Stack")
    
    # Note:
    # Make sure you keep references to CFUNCTYPE() objects as long as they are used from C code.
    # ctypes doesn't, and if you don"t, they may be garbage collected, crashing your program when
    # a callback is made
    #
    # Because of garbage collection, the pyCallback**** functions need to stay in scope.
    pyCallbackReceiveMessage = fpCallbackReceiveMessage(CallbackReceiveMessage)
    CASBACnetStack.BACnetStack_RegisterCallbackReceiveMessage(
        pyCallbackReceiveMessage)
    pyCallbackSendMessage = fpCallbackSendMessage(CallbackSendMessage)
    CASBACnetStack.BACnetStack_RegisterCallbackSendMessage(
        pyCallbackSendMessage)
    pyCallbackGetSystemTime = fpCallbackGetSystemTime(CallbackGetSystemTime)
    CASBACnetStack.BACnetStack_RegisterCallbackGetSystemTime(
        pyCallbackGetSystemTime)
    pyCallbackGetPropertyBitString = fpCallbackGetPropertyBitString(
        CallbackGetPropertyBitString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBitString(
        pyCallbackGetPropertyBitString)
    pyCallbackGetPropertyBool = fpCallbackGetPropertyBool(
        CallbackGetPropertyBool)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyBool(
        pyCallbackGetPropertyBool)
    pyCallbackGetPropertyCharString = fpCallbackGetPropertyCharString(
        CallbackGetPropertyCharString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyCharacterString(
        pyCallbackGetPropertyCharString)
    pyCallbackGetPropertyDate = fpCallbackGetPropertyDate(
        CallbackGetPropertyDate)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDate(
        pyCallbackGetPropertyDate)
    pyCallbackGetPropertyDouble = fpCallbackGetPropertyDouble(
        CallbackGetPropertyDouble)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyDouble(
        pyCallbackGetPropertyDouble)
    pyCallbackGetPropertyEnum = fpCallbackGetPropertyEnum(
        CallbackGetPropertyEnumerated)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyEnumerated(
        pyCallbackGetPropertyEnum)
    pyCallbackGetPropertyOctetString = fpCallbackGetPropertyOctetString(
        CallbackGetPropertyOctetString)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyOctetString(
        pyCallbackGetPropertyOctetString)
    pyCallbackGetPropertyInt = fpCallbackGetPropertyInt(CallbackGetPropertyInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertySignedInteger(
        pyCallbackGetPropertyInt)
    pyCallbackGetPropertyReal = fpCallbackGetPropertyReal(
        CallbackGetPropertyReal)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyReal(
        pyCallbackGetPropertyReal)
    pyCallbackGetPropertyTime = fpCallbackGetPropertyTime(
        CallbackGetPropertyTime)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyTime(
        pyCallbackGetPropertyTime)
    pyCallbackGetPropertyUInt = fpCallbackGetPropertyUInt(
        CallbackGetPropertyUInt)
    CASBACnetStack.BACnetStack_RegisterCallbackGetPropertyUnsignedInteger(
        pyCallbackGetPropertyUInt)
    pyCallbackSetPropertyUInt = fpCallbackSetPropertyUInt(
        CallbackSetPropertyUInt)
    CASBACnetStack.BACnetStack_RegisterCallbackSetPropertyUnsignedInteger(
        pyCallbackSetPropertyUInt)
    pyCallbackSetPropertyOctetString = fpCallbackSetPropertyOctetString(
        CallbackSetPropertyOctetString)
    CASBACnetStack.BACnetStack_RegisterCallbackSetPropertyOctetString(
        pyCallbackSetPropertyOctetString)
    pyCallbackReinitializeDevice = fpCallbackReinitializeDevice(
        CallbackReinitializeDevice)
    CASBACnetStack.BACnetStack_RegisterCallbackReinitializeDevice(
        pyCallbackReinitializeDevice)
    # pyCallbackDeviceCommunicationControl = fpCallbackDeviceCommunicationControl(CallbackDeviceCommunicationControl)
    # CASBACnetStack.BACnetStack_RegisterCallbackDeviceCommunicationControl(pyCallbackDeviceCommunicationControl)
    # pyCallbackLogDebugMessage = fpCallbackLogDebugMessage(CallbackLogDebugMessage)
    # CASBACnetStack.BACnetStack_RegisterCallbackLogDebugMessage(pyCallbackLogDebugMessage)

    # 3. Setup the BACnet device
    # ---------------------------------------------------------------------------------------------
    logger.info("Setting up server Device. device.instance=%s",
                DEVICE_INSTANCE)
    if not CASBACnetStack.BACnetStack_AddDevice(DEVICE_INSTANCE):
        logger.error("Failed to add Device")
        exit()

    # 4. Enable optional BACnet services.
    # ---------------------------------------------------------------------------------------------
    for service in ["readPropertyMultiple", "writeProperty", "writePropertyMultiple", "subscribeCov", "subscribeCovProperty", "reinitializeDevice", "deviceCommunicationControl", "iAm", "confirmedTextMessage", "unconfirmedTextMessage"]:
        logger.info("Enabling service: %s (%s)", service, casbacnetstack_service[service])
        CASBACnetStack.BACnetStack_SetServiceEnabled(
            DEVICE_INSTANCE, casbacnetstack_service[service], True)

    # 5. Add objects to the device
    # ---------------------------------------------------------------------------------------------
    objectList = BACnetDatabase.GetObjectsList(DEVICE_INSTANCE)
    if objectList is None or len(objectList) == 0:
        logger.error(
            "No objects found in database for device instance %s", DEVICE_INSTANCE)
        exit()
    AddObjectsFromDatabase(objectList)

    # 6. Network port is a special object that needs to be added and configured
    # ---------------------------------------------------------------------------------------------
    if AddAndConfigureNetworkPort(DEVICE_INSTANCE) is False:
        logger.error("Failed to add and configure network port")
        exit()

    # 7. Connect the UDP resource to the BACnet Port and get network info
    # ---------------------------------------------------------------------------------------------
    udp_port = BACnetDatabase.Get(
        DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["bacnetipudpport"])
    if udp_port is None:
        logger.error("Failed to get UDP port")
        exit()
    ConnectToSocket(int(udp_port))

    # 8. Send I-Am
    # To be a good BACnet citizen, we need to send an I-Am broadcast to let other BACnet devices
    # know we are here
    # ---------------------------------------------------------------------------------------------
    SendIAmBroadcast()

    # 9. Start the main loop
    # ---------------------------------------------------------------------------------------------
    logger.info("Entering main loop...")
    while True:
        # Call the CAS BACnet Stack tick function which checks for messages and processes them.
        # This function needs to be called at least once a second.
        CASBACnetStack.BACnetStack_Tick()

        # Sleep between loops. Give some time to other application
        time.sleep(0.1)

        # Every x seconds increment the AnalogInput presentValue property by 0.1
        if lastTimeValueWasUpdated + 3 < time.time():
            lastTimeValueWasUpdated = time.time()
            # updateValues()
