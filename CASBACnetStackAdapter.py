# 
# CAS BACnet Stack Python Adapter
# This file is used to help integration between the CAS BACnet stack DLL/.so files and a Python 3.7 application.
# Full documentation on what these function, and their parameters can be found in /source/CASBACnetStackDLL.h file. 
#

import ctypes
import platform

casbacnetstack_adapter_version = "0.0.4"  # For CASBACnetStack version 3.25.0 or greater

# libname
# ---------------------------------------------------------------------------
# Depending on the platform we will need to import a different CAS BACnet Stack library
# https://stackoverflow.com/a/54837707

# Debug
# print("os.name                      ",  os.name)
# print("sys.platform                 ",  sys.platform)
# print("sysconfig.get_platform()     ",  sysconfig.get_platform())
# print("platform.system()            ",  platform.system())
# print("platform.machine()           ",  platform.machine())
# print("platform.architecture()      ",  platform.architecture())

if platform.system() == "Windows":
    if platform.architecture()[0] == '64bit':
        libname = "CASBACnetStack_x64_Release.dll"
    elif platform.architecture()[0] == "32bit":
        libname = "CASBACnetStack_x86_Release.dll"
    else:
        print("Error: Could not detect the platform.architecture", platform.architecture())
elif platform.system() == "Linux":
    if platform.architecture()[0] == "64bit":
        libname = "libCASBACnetStack_x64_Release.so"
    elif platform.architecture()[0] == "32bit":
        if "armv7" in platform.machine():
            # Raspberry PI 3 or 4. Arm7
            libname = "libCASBACnetStack_arm7_Release.so"
        else:
            libname = "CASBACnetStack_x86_Release.so"
    else:
        print("Error: Could not detect the platform.architecture", platform.architecture())
else:
    print("Error: Could not detect the platform.system", platform.system())

# Callbacks ---------------------------------------------------------------------------
# https://docs.python.org/3/library/ctypes.html#callback-functions Factory functions are called with the result type
# as first argument, and the callback functions expected argument types as the remaining arguments.


# General Functions
fpCallbackReceiveMessage = ctypes.CFUNCTYPE(ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint16,
                                            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8,
                                            ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8))
fpCallbackSendMessage = ctypes.CFUNCTYPE(ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint16,
                                         ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_bool)
fpCallbackGetSystemTime = ctypes.CFUNCTYPE(ctypes.c_uint64)
fpCallbackSetSystemTime = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8,
                                           ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8,
                                           ctypes.c_uint8, ctypes.c_uint8)
fpCallbackReinitializeDevice = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint32,
                                                ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
                                                ctypes.POINTER(ctypes.c_uint32))
fpCallbackDeviceCommunicationControl = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8),
                                                        ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint16,
                                                        ctypes.POINTER(ctypes.c_uint32))

# CallbackGetProperty
fpCallbackGetPropertyBitString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                  ctypes.c_uint32, ctypes.POINTER(ctypes.c_bool),
                                                  ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_bool,
                                                  ctypes.c_uint32)
fpCallbackGetPropertyBool = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_bool), ctypes.c_bool,
                                             ctypes.c_uint32)
fpCallbackGetPropertyCharString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                   ctypes.c_uint32, ctypes.POINTER(ctypes.c_char),
                                                   ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32,
                                                   ctypes.POINTER(ctypes.c_uint8), ctypes.c_bool, ctypes.c_uint32)
fpCallbackGetPropertyDate = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                             ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8),
                                             ctypes.POINTER(ctypes.c_uint8), ctypes.c_bool, ctypes.c_uint32)
fpCallbackGetPropertyDouble = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                               ctypes.c_uint32, ctypes.POINTER(ctypes.c_double), ctypes.c_bool,
                                               ctypes.c_uint32)
fpCallbackGetPropertyEnum = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_bool,
                                             ctypes.c_uint32)
fpCallbackGetPropertyOctetString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                    ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                                    ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_bool,
                                                    ctypes.c_uint32)
fpCallbackGetPropertyInt = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                            ctypes.c_uint32, ctypes.POINTER(ctypes.c_int32), ctypes.c_bool,
                                            ctypes.c_uint32)
fpCallbackGetPropertyReal = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_float), ctypes.c_bool,
                                             ctypes.c_uint32)
fpCallbackGetPropertyTime = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                             ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8),
                                             ctypes.POINTER(ctypes.c_uint8), ctypes.c_bool, ctypes.c_uint32)
fpCallbackGetPropertyUInt = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_bool,
                                             ctypes.c_uint32)
fpCallbackGetListOfEnumerations = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                   ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint32, ctypes.c_bool,
                                                   ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_bool))
# CallbackSetProperty
fpCallbackSetPropertyBitString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                  ctypes.c_uint32, ctypes.POINTER(ctypes.c_bool), ctypes.c_uint32,
                                                  ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                                  ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyBool = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_bool, ctypes.c_bool, ctypes.c_uint32,
                                             ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyCharString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                   ctypes.c_uint32, ctypes.POINTER(ctypes.c_char), ctypes.c_uint32,
                                                   ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                                   ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyDate = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8,
                                             ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                             ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyDouble = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                               ctypes.c_uint32, ctypes.c_double, ctypes.c_bool, ctypes.c_uint32,
                                               ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyEnum = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                             ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyNull = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                             ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyOctetString = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                                    ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
                                                    ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                                    ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyInt = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                            ctypes.c_uint32, ctypes.c_int32, ctypes.c_bool, ctypes.c_uint32,
                                            ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyReal = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_float, ctypes.c_bool, ctypes.c_uint32,
                                             ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyTime = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint8,
                                             ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8,
                                             ctypes.POINTER(ctypes.c_uint32))
fpCallbackSetPropertyUInt = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32,
                                             ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                             ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint32))

fpCallbackLogDebugMessage = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint16, ctypes.c_uint8)

# Client Hooks
fpHookIAm = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16,
                             ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                             ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookIHave = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint16, ctypes.c_uint32, ctypes.POINTER(ctypes.c_char),
                               ctypes.c_uint32, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8,
                               ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookError = ctypes.CFUNCTYPE(None, ctypes.c_uint8, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
                               ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                               ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint16,
                               ctypes.c_uint32, ctypes.c_uint32)
fpHookReject = ctypes.CFUNCTYPE(None, ctypes.c_uint8, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8,
                                ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookAbort = ctypes.CFUNCTYPE(None, ctypes.c_uint8, ctypes.c_bool, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                               ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8),
                               ctypes.c_uint8)
fpHookSimpleAck = ctypes.CFUNCTYPE(None, ctypes.c_uint8, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.c_uint8)
fpHookTimeout = ctypes.CFUNCTYPE(None, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8,
                                 ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyBitString = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                           ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                           ctypes.POINTER(ctypes.c_bool), ctypes.c_uint32,
                                           ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8,
                                           ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyBool = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_bool,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyCharString = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                            ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                            ctypes.POINTER(ctypes.c_char), ctypes.c_uint32, ctypes.c_uint8,
                                            ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8,
                                            ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyDate = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8,
                                      ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8,
                                      ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyDouble = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                        ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_double,
                                        ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                        ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyEnum = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyNull = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                      ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8),
                                      ctypes.c_uint8)
fpHookPropertyObjectIdentifier = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16,
                                                  ctypes.c_uint32, ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                                  ctypes.c_uint16, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint8),
                                                  ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                                  ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyOctString = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                           ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32,
                                           ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint32,
                                           ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8,
                                           ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyInt = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                     ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_int32,
                                     ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                     ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyReal = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_float,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyTime = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint8,
                                      ctypes.c_uint8, ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8,
                                      ctypes.c_uint8, ctypes.c_uint16, ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)
fpHookPropertyUInt = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint32,
                                      ctypes.c_uint32, ctypes.c_bool, ctypes.c_uint32, ctypes.c_uint32,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8, ctypes.c_uint8, ctypes.c_uint16,
                                      ctypes.POINTER(ctypes.c_uint8), ctypes.c_uint8)

# Constants
# ---------------------------------------------------------------------------
MAX_BACNET_PRIORITY = 16

# Enumerations
# ---------------------------------------------------------------------------

# Full list in BACnetObjectTypes.h
bacnet_objectType = {"analogInput": 0, "analogOutput": 1, "analogValue": 2, "binaryInput": 3, "binaryOutput": 4,
                     "binaryValue": 5, "calendar": 6, "command": 7, "device": 8, "eventEnrollment": 9, "file": 10,
                     "group": 11, "loop": 12, "multiStateInput": 13, "multiStateOutput": 14, "notificationClass": 15,
                     "program": 16, "schedule": 17, "averaging": 18, "multiStateValue": 19, "trendLog": 20,
                     "lifeSafetyPoint": 21, "lifeSafetyZone": 22, "accumulator": 23, "pulseConverter": 24,
                     "eventLog": 25, "globalGroup": 26, "trendLogMultiple": 27, "loadControl": 28, "structuredView": 29,
                     "accessDoor": 30, "timer": 31, "accessCredential": 32, "accessPoint": 33, "accessRights": 34,
                     "accessUser": 35, "accessZone": 36, "credentialDataInput": 37, "networkSecurity": 38,
                     "bitstringValue": 39, "characterstringValue": 40, "datepatternValue": 41, "dateValue": 42,
                     "datetimepatternValue": 43, "datetimeValue": 44, "integerValue": 45, "largeAnalogValue": 46,
                     "octetstringValue": 47, "positiveIntegerValue": 48, "timepatternValue": 49, "timeValue": 50,
                     "notificationForwarder": 51, "alertEnrollment": 52, "channel": 53, "lightingOutput": 54,
                     "binaryLightingOutput": 55, "networkPort": 56, "elevatorGroup": 57, "escalator": 58, "lift": 59}

# Full list in BACnetPropertyIdentifier.h
bacnet_propertyIdentifier = {"absenteelimit": 244, "acceptedmodes": 175, "accessalarmevents": 245, "accessdoors": 246,
                             "accessevent": 247, "accesseventauthenticationfactor": 248, "accesseventcredential": 249,
                             "accesseventtag": 322, "accesseventtime": 250, "accesstransactionevents": 251,
                             "accompaniment": 252, "accompanimenttime": 253, "ackrequired": 1, "ackedtransitions": 0,
                             "action": 2, "actiontext": 3, "activationtime": 254, "activeauthenticationpolicy": 255,
                             "activecovmultiplesubscriptions": 481, "activecovsubscriptions": 152, "activetext": 4,
                             "activevtsessions": 5, "actualshedlevel": 212, "adjustvalue": 176, "alarmvalue": 6,
                             "alarmvalues": 7, "alignintervals": 193, "all": 8, "allwritessuccessful": 9,
                             "allowgroupdelayinhibit": 365, "apdulength": 399, "apdusegmenttimeout": 10,
                             "apdutimeout": 11, "applicationsoftwareversion": 12, "archive": 13,
                             "assignedaccessrights": 256, "assignedlandingcalls": 447, "attemptedsamples": 124,
                             "authenticationfactors": 257, "authenticationpolicylist": 258,
                             "authenticationpolicynames": 259, "authenticationstatus": 260,
                             "authorizationexemptions": 364, "authorizationmode": 261, "autoslavediscovery": 169,
                             "averagevalue": 125, "backupandrestorestate": 338, "backupfailuretimeout": 153,
                             "backuppreparationtime": 339, "bacnetipglobaladdress": 407, "bacnetipmode": 408,
                             "bacnetipmulticastaddress": 409, "bacnetipnattraversal": 410, "bacnetipudpport": 412,
                             "bacnetipv6mode": 435, "bacnetipv6udpport": 438, "bacnetipv6multicastaddress": 440,
                             "basedevicesecuritypolicy": 327, "bbmdacceptfdregistrations": 413,
                             "bbmdbroadcastdistributiontable": 414, "bbmdforeigndevicetable": 415, "belongsto": 262,
                             "bias": 14, "bitmask": 342, "bittext": 343, "blinkwarnenable": 373, "buffersize": 126,
                             "carassigneddirection": 448, "cardoorcommand": 449, "cardoorstatus": 450,
                             "cardoortext": 451, "cardoorzone": 452, "cardrivestatus": 453, "carload": 454,
                             "carloadunits": 455, "carmode": 456, "carmovingdirection": 457, "carposition": 458,
                             "changeofstatecount": 15, "changeofstatetime": 16, "changespending": 416,
                             "channelnumber": 366, "clientcovincrement": 127, "command": 417, "commandtimearray": 430,
                             "configurationfiles": 154, "controlgroups": 367, "controlledvariablereference": 19,
                             "controlledvariableunits": 20, "controlledvariablevalue": 21, "count": 177,
                             "countbeforechange": 178, "countchangetime": 179, "covincrement": 22, "covperiod": 180,
                             "covresubscriptioninterval": 128, "covuperiod": 349, "covurecipients": 350,
                             "credentialdisable": 263, "credentialstatus": 264, "credentials": 265,
                             "credentialsinzone": 266, "currentcommandpriority": 431, "databaserevision": 155,
                             "datelist": 23, "daylightsavingsstatus": 24, "daysremaining": 267, "deadband": 25,
                             "defaultfadetime": 374, "defaultramprate": 375, "defaultstepincrement": 376,
                             "defaultsubordinaterelationship": 490, "defaulttimeout": 393,
                             "deployedprofilelocation": 484, "derivativeconstant": 26, "derivativeconstantunits": 27,
                             "description": 28, "descriptionofhalt": 29, "deviceaddressbinding": 30, "devicetype": 31,
                             "directreading": 156, "distributionkeyrevision": 328, "donothide": 329,
                             "dooralarmstate": 226, "doorextendedpulsetime": 227, "doormembers": 228,
                             "dooropentoolongtime": 229, "doorpulsetime": 230, "doorstatus": 231,
                             "doorunlockdelaytime": 232, "dutywindow": 213, "effectiveperiod": 32, "egressactive": 386,
                             "egresstime": 377, "elapsedactivetime": 33, "elevatorgroup": 459, "enable": 133,
                             "energymeter": 460, "energymeterref": 461, "entrypoints": 268, "errorlimit": 34,
                             "escalatormode": 462, "eventalgorithminhibit": 354, "eventalgorithminhibitref": 355,
                             "eventdetectionenable": 353, "eventenable": 35, "eventmessagetexts": 351,
                             "eventmessagetextsconfig": 352, "eventparameters": 83, "eventstate": 36,
                             "eventtimestamps": 130, "eventtype": 37, "exceptionschedule": 38, "executiondelay": 368,
                             "exitpoints": 269, "expectedshedlevel": 214, "expirationtime": 270,
                             "extendedtimeenable": 271, "failedattemptevents": 272, "failedattempts": 273,
                             "failedattemptstime": 274, "faulthighlimit": 388, "faultlowlimit": 389,
                             "faultparameters": 358, "faultsignals": 463, "faulttype": 359, "faultvalues": 39,
                             "fdbbmdaddress": 418, "fdsubscriptionlifetime": 419, "feedbackvalue": 40,
                             "fileaccessmethod": 41, "filesize": 42, "filetype": 43, "firmwarerevision": 44,
                             "floortext": 464, "fulldutybaseline": 215, "globalidentifier": 323, "groupid": 465,
                             "groupmembernames": 346, "groupmembers": 345, "groupmode": 467, "highlimit": 45,
                             "higherdeck": 468, "inprocess": 47, "inprogress": 378, "inactivetext": 46,
                             "initialtimeout": 394, "inputreference": 181, "installationid": 469, "instanceof": 48,
                             "instantaneouspower": 379, "integralconstant": 49, "integralconstantunits": 50,
                             "interfacevalue": 387, "intervaloffset": 195, "ipaddress": 400, "ipdefaultgateway": 401,
                             "ipdhcpenable": 402, "ipdhcpleasetime": 403, "ipdhcpleasetimeremaining": 404,
                             "ipdhcpserver": 405, "ipdnsserver": 406, "ipsubnetmask": 411, "ipv6address": 436,
                             "ipv6autoaddressingenable": 442, "ipv6defaultgateway": 439, "ipv6dhcpleasetime": 443,
                             "ipv6dhcpleasetimeremaining": 444, "ipv6dhcpserver": 445, "ipv6dnsserver": 441,
                             "ipv6prefixlength": 437, "ipv6zoneindex": 446, "isutc": 344, "keysets": 330,
                             "landingcallcontrol": 471, "landingcalls": 470, "landingdoorstatus": 472,
                             "lastaccessevent": 275, "lastaccesspoint": 276, "lastcommandtime": 432,
                             "lastcredentialadded": 277, "lastcredentialaddedtime": 278, "lastcredentialremoved": 279,
                             "lastcredentialremovedtime": 280, "lastkeyserver": 331, "lastnotifyrecord": 173,
                             "lastpriority": 369, "lastrestartreason": 196, "lastrestoretime": 157,
                             "laststatechange": 395, "lastusetime": 281, "lifesafetyalarmvalues": 166,
                             "lightingcommand": 380, "lightingcommanddefaultpriority": 381, "limitenable": 52,
                             "limitmonitoringinterval": 182, "linkspeed": 420, "linkspeedautonegotiate": 422,
                             "linkspeeds": 421, "listofgroupmembers": 53, "listofobjectpropertyreferences": 54,
                             "localdate": 56, "localforwardingonly": 360, "localtime": 57, "location": 58,
                             "lockstatus": 233, "lockout": 282, "lockoutrelinquishtime": 283, "logbuffer": 131,
                             "logdeviceobjectproperty": 132, "loginterval": 134, "loggingobject": 183,
                             "loggingrecord": 184, "loggingtype": 197, "lowdifflimit": 390, "lowlimit": 59,
                             "lowerdeck": 473, "macaddress": 423, "machineroomid": 474, "maintenancerequired": 158,
                             "makingcarcall": 475, "manipulatedvariablereference": 60, "manualslaveaddressbinding": 170,
                             "maskedalarmvalues": 234, "maxactualvalue": 382, "maxapdulengthaccepted": 62,
                             "maxfailedattempts": 285, "maxinfoframes": 63, "maxmaster": 64, "maxpresvalue": 65,
                             "maxsegmentsaccepted": 167, "maximumoutput": 61, "maximumvalue": 135,
                             "maximumvaluetimestamp": 149, "memberof": 159, "memberstatusflags": 347, "members": 286,
                             "minactualvalue": 383, "minpresvalue": 69, "minimumofftime": 66, "minimumontime": 67,
                             "minimumoutput": 68, "minimumvalue": 136, "minimumvaluetimestamp": 150, "mode": 160,
                             "modelname": 70, "modificationdate": 71, "musterpoint": 287, "negativeaccessrules": 288,
                             "networkaccesssecuritypolicies": 332, "networkinterfacename": 424, "networknumber": 425,
                             "networknumberquality": 426, "networktype": 427, "nextstoppingfloor": 476,
                             "nodesubtype": 207, "nodetype": 208, "notificationclass": 17, "notificationthreshold": 137,
                             "notifytype": 72, "numberofapduretries": 73, "numberofauthenticationpolicies": 289,
                             "numberofstates": 74, "objectidentifier": 75, "objectlist": 76, "objectname": 77,
                             "objectpropertyreference": 78, "objecttype": 79, "occupancycount": 290,
                             "occupancycountadjust": 291, "occupancycountenable": 292, "occupancylowerlimit": 294,
                             "occupancylowerlimitenforced": 295, "occupancystate": 296, "occupancyupperlimit": 297,
                             "occupancyupperlimitenforced": 298, "operationdirection": 477, "operationexpected": 161,
                             "optional": 80, "outofservice": 81, "outputunits": 82, "packetreordertime": 333,
                             "passbackmode": 300, "passbacktimeout": 301, "passengeralarm": 478, "polarity": 84,
                             "portfilter": 363, "positiveaccessrules": 302, "power": 384, "powermode": 479,
                             "prescale": 185, "presentvalue": 85, "priority": 86, "priorityarray": 87,
                             "priorityforwriting": 88, "processidentifier": 89, "processidentifierfilter": 361,
                             "profilelocation": 485, "profilename": 168, "programchange": 90, "programlocation": 91,
                             "programstate": 92, "propertylist": 371, "proportionalconstant": 93,
                             "proportionalconstantunits": 94, "protocollevel": 482, "protocolobjecttypessupported": 96,
                             "protocolrevision": 139, "protocolservicessupported": 97, "protocolversion": 98,
                             "pulserate": 186, "readonly": 99, "reasonfordisable": 303, "reasonforhalt": 100,
                             "recipientlist": 102, "recordcount": 141, "recordssincenotification": 140,
                             "referenceport": 483, "registeredcarcall": 480, "reliability": 103,
                             "reliabilityevaluationinhibit": 357, "relinquishdefault": 104, "represents": 491,
                             "requestedshedlevel": 218, "requestedupdateinterval": 348, "required": 105,
                             "resolution": 106, "restartnotificationrecipients": 202, "restorecompletiontime": 340,
                             "restorepreparationtime": 341, "routingtable": 428, "scale": 187, "scalefactor": 188,
                             "scheduledefault": 174, "securedstatus": 235, "securitypdutimeout": 334,
                             "securitytimewindow": 335, "segmentationsupported": 107, "serialnumber": 372,
                             "setpoint": 108, "setpointreference": 109, "setting": 162, "shedduration": 219,
                             "shedleveldescriptions": 220, "shedlevels": 221, "silenced": 163,
                             "slaveaddressbinding": 171, "slaveproxyenable": 172, "starttime": 142,
                             "statechangevalues": 396, "statedescription": 222, "statetext": 110, "statusflags": 111,
                             "stoptime": 143, "stopwhenfull": 144, "strikecount": 391, "structuredobjectlist": 209,
                             "subordinateannotations": 210, "subordinatelist": 211, "subordinatenodetypes": 487,
                             "subordinaterelationships": 489, "subordinatetags": 488, "subscribedrecipients": 362,
                             "supportedformatclasses": 305, "supportedformats": 304, "supportedsecurityalgorithms": 336,
                             "systemstatus": 112, "tags": 486, "threatauthority": 306, "threatlevel": 307,
                             "timedelay": 113, "timedelaynormal": 356, "timeofactivetimereset": 114,
                             "timeofdevicerestart": 203, "timeofstatecountreset": 115, "timeofstrikecountreset": 392,
                             "timesynchronizationinterval": 204, "timesynchronizationrecipients": 116,
                             "timerrunning": 397, "timerstate": 398, "totalrecordcount": 145, "traceflag": 308,
                             "trackingvalue": 164, "transactionnotificationclass": 309, "transition": 385,
                             "trigger": 205, "units": 117, "updateinterval": 118, "updatekeysettimeout": 337,
                             "updatetime": 189, "userexternalidentifier": 310, "userinformationreference": 311,
                             "username": 317, "usertype": 318, "usesremaining": 319, "utcoffset": 119,
                             "utctimesynchronizationrecipients": 206, "validsamples": 146, "valuebeforechange": 190,
                             "valuechangetime": 192, "valueset": 191, "valuesource": 433, "valuesourcearray": 434,
                             "variancevalue": 151, "vendoridentifier": 120, "vendorname": 121, "verificationtime": 326,
                             "virtualmacaddresstable": 429, "vtclassessupported": 122, "weeklyschedule": 123,
                             "windowinterval": 147, "windowsamples": 148, "writestatus": 370, "zonefrom": 320,
                             "zonemembers": 165, "zoneto": 32}

# Full list in BACnetEngineeringUnits.h
bacnet_engineeringUnits = {"meterspersecondpersecond": 166, "squaremeters": 0, "squarecentimeters": 116,
                           "squarefeet": 1, "squareinches": 115, "currency1": 105, "currency2": 106, "currency3": 107,
                           "currency4": 108, "currency5": 109, "currency6": 110, "currency7": 111, "currency8": 112,
                           "currency9": 113, "currency10": 114, "milliamperes": 2, "amperes": 3, "amperespermeter": 167,
                           "amperespersquaremeter": 168, "amperesquaremeters": 169, "decibels": 199,
                           "decibelsmillivolt": 200, "decibelsvolt": 201, "farads": 170, "henrys": 171, "ohms": 4,
                           "ohmmetersquaredpermeter": 237, "ohmmeters": 172, "milliohms": 145, "kilohms": 122,
                           "megohms": 123, "microsiemens": 190, "millisiemens": 202, "siemens": 173,
                           "siemenspermeter": 174, "teslas": 175, "volts": 5, "millivolts": 124, "kilovolts": 6,
                           "megavolts": 7, "voltamperes": 8, "kilovoltamperes": 9, "megavoltamperes": 10,
                           "volt_amperes_reactive": 11, "kilovoltamperesreactive": 12, "megavoltamperesreactive": 13,
                           "voltsperdegreekelvin": 176, "voltspermeter": 177, "degreesphase": 14, "powerfactor": 15,
                           "webers": 178, "ampereseconds": 238, "voltamperehours": 239, "kilovoltamperehours": 240,
                           "megavoltamperehours": 241, "voltamperehoursreactive": 242,
                           "kilovoltamperehoursreactive": 243, "megavoltamperehoursreactive": 244,
                           "voltsquarehours": 245, "amperesquarehours": 246, "joules": 16, "kilojoules": 17,
                           "kilojoulesperkilogram": 125, "megajoules": 126, "watt_hours": 18, "kilowatt_hours": 19,
                           "megawatt_hours": 146, "watthoursreactive": 203, "kilowatthoursreactive": 204,
                           "megawatthoursreactive": 205, "btus": 20, "kilobtus": 147, "megabtus": 148, "therms": 21,
                           "tonhours": 22, "joulesperkilogramdryair": 23, "kilojoulesperkilogramdryair": 149,
                           "megajoulesperkilogramdryair": 150, "btusperpounddryair": 24, "btusperpound": 117,
                           "joulesperdegreekelvin": 127, "kilojoulesperdegreekelvin": 151,
                           "megajoulesperdegreekelvin": 152, "joulesperkilogramdegreekelvin": 128, "newton": 153,
                           "cyclesperhour": 25, "cyclesperminute": 26, "hertz": 27, "kilohertz": 129, "megahertz": 130,
                           "perhour": 131, "gramsofwaterperkilogramdryair": 28, "percentrelativehumidity": 29,
                           "micrometers": 194, "millimeters": 30, "centimeters": 118, "kilometers": 193, "meters": 31,
                           "inches": 32, "feet": 33, "candelas": 179, "candelaspersquaremeter": 180,
                           "wattspersquarefoot": 34, "wattspersquaremeter": 35, "lumens": 36, "luxes": 37,
                           "footcandles": 38, "milligrams": 196, "grams": 195, "kilograms": 39, "poundsmass": 40,
                           "tons": 41, "gramspersecond": 154, "gramsperminute": 155, "kilogramspersecond": 42,
                           "kilogramsperminute": 43, "kilogramsperhour": 44, "poundsmasspersecond": 119,
                           "poundsmassperminute": 45, "poundsmassperhour": 46, "tonsperhour": 156, "milliwatts": 132,
                           "watts": 47, "kilowatts": 48, "megawatts": 49, "btusperhour": 50, "kilobtusperhour": 157,
                           "jouleperhours": 247, "horsepower": 51, "tonsrefrigeration": 52, "pascals": 53,
                           "hectopascals": 133, "kilopascals": 54, "millibars": 134, "bars": 55,
                           "poundsforcepersquareinch": 56, "millimetersofwater": 206, "centimetersofwater": 57,
                           "inchesofwater": 58, "millimetersofmercury": 59, "centimetersofmercury": 60,
                           "inchesofmercury": 61, "degreescelsius": 62, "degreeskelvin": 63,
                           "degreeskelvinperhour": 181, "degreeskelvinperminute": 182, "degreesfahrenheit": 64,
                           "degreedayscelsius": 65, "degreedaysfahrenheit": 66, "deltadegreesfahrenheit": 120,
                           "deltadegreeskelvin": 121, "years": 67, "months": 68, "weeks": 69, "days": 70, "hours": 71,
                           "minutes": 72, "seconds": 73, "hundredthsseconds": 158, "milliseconds": 159,
                           "newtonmeters": 160, "millimeterspersecond": 161, "millimetersperminute": 162,
                           "meterspersecond": 74, "metersperminute": 163, "metersperhour": 164, "kilometersperhour": 75,
                           "feetpersecond": 76, "feetperminute": 77, "milesperhour": 78, "cubicfeet": 79,
                           "cubicmeters": 80, "imperialgallons": 81, "milliliters": 197, "liters": 82, "usgallons": 83,
                           "cubicfeetpersecond": 142, "cubicfeetperminute": 84,
                           "millionstandardcubicfeetperminute": 254, "cubicfeetperhour": 191, "cubicfeetperday": 248,
                           "standardcubicfeetperday": 47808, "millionstandardcubicfeetperday": 47809,
                           "thousandcubicfeetperday": 47810, "thousandstandardcubicfeetperday": 47811,
                           "poundsmassperday": 47812, "cubicmeterspersecond": 85, "cubicmetersperminute": 165,
                           "cubicmetersperhour": 135, "cubicmetersperday": 249, "imperialgallonsperminute": 86,
                           "milliliterspersecond": 198, "literspersecond": 87, "litersperminute": 88,
                           "litersperhour": 136, "usgallonsperminute": 89, "usgallonsperhour": 192,
                           "degreesangular": 90, "degreescelsiusperhour": 91, "degreescelsiusperminute": 92,
                           "degreesfahrenheitperhour": 93, "degreesfahrenheitperminute": 94, "jouleseconds": 183,
                           "kilogramspercubicmeter": 186, "kilowatthourspersquaremeter": 137,
                           "kilowatthourspersquarefoot": 138, "watthourspercubicmeter": 250, "joulespercubicmeter": 251,
                           "megajoulespersquaremeter": 139, "megajoulespersquarefoot": 140, "molepercent": 252,
                           "no_units": 95, "newtonseconds": 187, "newtonspermeter": 188, "partspermillion": 96,
                           "partsperbillion": 97, "pascalseconds": 253, "percent": 98, "percentobscurationperfoot": 143,
                           "percentobscurationpermeter": 144, "percentpersecond": 99, "perminute": 100,
                           "persecond": 101, "psiperdegreefahrenheit": 102, "radians": 103, "radianspersecond": 184,
                           "revolutionsperminute": 104, "squaremeterspernewton": 185,
                           "wattspermeterperdegreekelvin": 189, "wattspersquaremeterdegreekelvin": 141, "permille": 207,
                           "gramspergram": 208, "kilogramsperkilogram": 209, "gramsperkilogram": 210,
                           "milligramspergram": 211, "milligramsperkilogram": 212, "gramspermilliliter": 213,
                           "gramsperliter": 214, "milligramsperliter": 215, "microgramsperliter": 216,
                           "gramspercubicmeter": 217, "milligramspercubicmeter": 218, "microgramspercubicmeter": 219,
                           "nanogramspercubicmeter": 220, "gramspercubiccentimeter": 221, "becquerels": 222,
                           "kilobecquerels": 223, "megabecquerels": 224, "gray": 225, "milligray": 226,
                           "microgray": 227, "sieverts": 228, "millisieverts": 229, "microsieverts": 230,
                           "microsievertsperhour": 231, "millirems": 47814, "milliremsperhour": 47815, "decibelsa": 232,
                           "nephelometricturbidityunit": 233, "ph": 234, "gramspersquaremeter": 235,
                           "minutesperdegreekelvin": 236}

bacnet_reliability = {"no-fault-detected": 0, "no-sensor": 1, "over-range": 2, "under-range": 3, "open-loop": 4,
                      "shorted-loop": 5, "no-output": 6, "unreliable-other": 7, "process-error": 8,
                      "multi-state-fault": 9, "configuration-error": 10, "communication-failure": 12,
                      "member-fault": 13, "monitored-object-fault": 14, "tripped": 15, "lamp-failure": 16,
                      "activation-failure": 17, "renew-dhcp-failure": 18, "renew-fd-registration-failure": 19,
                      "restart-auto-negotiation-failure": 20, "restart-failure": 21, "proprietary-command-failure": 22,
                      "faults-listed": 23, "referenced-object-fault": 24, "multi-state-out-of-range": 25}

bacnet_errorCode = {"missing-required-parameter": 16, "password-failure": 26, "optional-functionality-not-supported": 45}


casbacnetstack_service = {"subscribeCov": 5, "createObject": 10, "deleteObject": 11, "readPropertyMultiple": 14,
                          "writeProperty": 15, "writePropertyMultiple": 16, "deviceCommunicationControl": 17,
                          "confirmedTextMessage": 19, "reinitializeDevice": 20, "iAm": 26, "iHave": 27,
                          "unconfirmedTextMessage": 31, "timeSynchronization": 32, "utcTimeSynchronization": 36,
                          "subscribeCovProperty": 38}

casbacnetstack_reinitializeState = {"state-warm-start": 1, "state-activate-changes": 7}

casbacnetstack_networkType = {"ip": 0, "mstp": 1, "ipv4": 5}

casbacnetstack_protocolLevel = {"bacnet-application": 2}

casbacnetstack_fdBbmdAddressOffset = {"host": 1, "port": 2}

casbacnetstack_network_port_lowest_protocol_level = 4194303

casbacnet_ReleaseMessageType = {"Error": 0, "Info": 1}
