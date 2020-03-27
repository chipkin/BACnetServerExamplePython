#!/usr/bin/python

# BACnetServerExamplePython
# 
# A basic BACnet IP server example written with Python using the CAS BACnet Stack and CASBACnetRPC.
# More information: https://github.com/chipkin/BACnetServerExamplePython 
#
# Created by: Steven Smethurst
# Last Updated: 2020 March 26 
# 

from __future__ import print_function
import logging
import threading

import grpc

import casbacnetstack_pb2
import casbacnetstack_pb2_grpc

analogInputPresentValue =  0.0

#
# BACnet stack Enumerations 
# -----------------------------------------------------------
# These are the most commonly used enumeration in the CAS BACnet stack. 
# A full list can be found here: \submodules\cas-bacnet-stack\docs\quickstart.md.html
#
# Date types:         
# Null = 0, Boolean = 1, UnsignedInteger = 2, SignedInteger = 3, Real = 4, Double = 5, OctetString = 6
# CharacterString = 7, BitString = 8, Enumerated = 9, Date = 10, Time = 11, ObjectIdentifier = 12,
#
# Object types: 
# analogInput = 0, analogOutput = 1, analogValue = 2, binaryInput = 3, binaryOutput = 4, binaryValue = 5, device = 8, 
# multiStateInput = 13, multiStateOutput = 14, multiStateValue = 19
#
# Property identifier: 
# objectName = 77, presentValue	= 85, units = 117, description = 28, location = 58, vendorIdentifier = 120, applicationSoftwareVersion = 12
#
# Engineering Units
# noUnits = 95, degreesCelsius = 62, degreesKelvin = 63, degreesFahrenheit = 64, wattHours = 18, kilowattHours = 19, megawattHours = 146
#

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = casbacnetstack_pb2_grpc.CASBacnetStackStub(channel)
        print("BACnetServerExample v0.0.1")

        response = stub.GetVersion(casbacnetstack_pb2.Empty())
        print("bacnet_rpc_version: " + str(response.version_bacnet_rpc_major) + "." + str(response.version_bacnet_rpc_minor)+ "." + str(response.version_bacnet_rpc_patch)+ "." + str(response.version_bacnet_rpc_build))
        print("bacnet_stack_version: " + str(response.version_bacnet_stack_major) + "." + str(response.version_bacnet_stack_minor)+ "." + str(response.version_bacnet_stack_patch)+ "." + str(response.version_bacnet_stack_build))

        deviceInstance = 389999

        print("CreateObject: Device (389999)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( object_type=8, object_instance=deviceInstance ))        
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( object_type=8, object_instance=deviceInstance, property_identifier=77, data_type=7, value="Device Rainbow" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( object_type=8, object_instance=deviceInstance, property_identifier=28, data_type=7, value="Device description" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( object_type=8, object_instance=deviceInstance, property_identifier=58, data_type=7, value="Device location information" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( object_type=8, object_instance=deviceInstance, property_identifier=120, data_type=2, value="389" )) # Vendor idenitfier, 389 = Chipkin Automation Systems

        print("CreateObject: Analog Input (0)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=0, object_instance=0 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=0, object_instance=0, property_identifier=77, data_type=7, value="AnalogInput Bronze" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=0, object_instance=0, property_identifier=85, data_type=4, value=str(round(analogInputPresentValue, 2))))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=0, object_instance=0, property_identifier=117, data_type=9, value="64" ))

        print("CreateObject: Analog Output (1)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=1, object_instance=1 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=1, object_instance=1, property_identifier=77, data_type=7, value="AnalogOutput Chartreuse" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=1, object_instance=1, property_identifier=85, data_type=4, value="88.8" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=1, object_instance=1, property_identifier=117, data_type=9, value="95" ))

        print("CreateObject: Analog Value (2)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=2, object_instance=2 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=2, object_instance=2, property_identifier=77, data_type=7, value="AnalogValue Diamond" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=2, object_instance=2, property_identifier=85, data_type=4, value="77.7" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=2, object_instance=2, property_identifier=117, data_type=9, value="95" ))

        print("CreateObject: Binary Input (3)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=3, object_instance=3 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=3, object_instance=3, property_identifier=77, data_type=7, value="BinaryInput Emerald" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=3, object_instance=3, property_identifier=85, data_type=9, value="1" ))

        print("CreateObject: Binary Output (4)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=4, object_instance=4 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=4, object_instance=4, property_identifier=77, data_type=7, value="BinaryOutput Fuchsia" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=4, object_instance=4, property_identifier=85, data_type=9, value="0" ))

        print("CreateObject: Binary Value (5)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=5, object_instance=5 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=5, object_instance=5, property_identifier=77, data_type=7, value="BinaryValue Gold" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=5, object_instance=5, property_identifier=85, data_type=9, value="1" ))

        '''
        print("CreateObject: Multi State Input (13)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=13, object_instance=13 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=13, object_instance=13, property_identifier=77, data_type=7, value="MultiStateInput Hot Pink" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=13, object_instance=13, property_identifier=85, data_type=9, value="1" ))

        print("CreateObject: Multi State Output (14)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=14, object_instance=14 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=14, object_instance=14, property_identifier=77, data_type=7, value="MultiStateOutput Indigo" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=14, object_instance=14, property_identifier=85, data_type=9, value="2" ))

        print("CreateObject: Multi State Value (19)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=19, object_instance=19 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=19, object_instance=19, property_identifier=77, data_type=7, value="MultiStateValue Kiwi" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=19, object_instance=19, property_identifier=85, data_type=9, value="3" ))

        print("CreateObject: Character string Value (40)")
        response = stub.CreateObject(casbacnetstack_pb2.CreateObjectMessage( device_instance=deviceInstance, object_type=40, object_instance=40 ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=40, object_instance=40, property_identifier=77, data_type=7, value="CharacterstringValue Nickel" ))
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( device_instance=deviceInstance, object_type=40, object_instance=40, property_identifier=85, data_type=7, value="Example text" ))
        '''

        print("Configure BACnet IP")
        response = stub.ConfigureBACnetIP(casbacnetstack_pb2.BACnetIPConfigration( enabled=True, udp_port=47808 ))
 
        print("Configure BACnet MSTP")
        # response = stub.ConfigureBACnetMSTP(casbacnetstack_pb2.BACnetMSTPConfigration( enabled=True, com_port="/dev/ttyS4", baud_rate=38400, mac_address=4 ))

        # Debug 
        response = stub.Debug(casbacnetstack_pb2.Empty())
        # print(response) 

        print("Done configuration")


def autoIncurmentAnalogInput():
    threading.Timer(1.0, autoIncurmentAnalogInput).start()

    global analogInputPresentValue
    analogInputPresentValue += 0.01
    print("Updating AnalogInput (0) PresentValue = " + str( round(analogInputPresentValue, 2)) )

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = casbacnetstack_pb2_grpc.CASBacnetStackStub(channel)
        response = stub.SetProperty(casbacnetstack_pb2.SetPropertyMessage( object_type=0, object_instance=0, property_identifier=85, data_type=4, value=str(round(analogInputPresentValue, 2)) ))

if __name__ == '__main__':
    logging.basicConfig()
    run()    
    autoIncurmentAnalogInput()
