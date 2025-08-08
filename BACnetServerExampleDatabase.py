"""
Example Database used for the BACnet Server Example


# Set
BACnetDatabase.Set(1,2,3,77,"Device Rainbow" )
BACnetDatabase.Set(1,2,3,85,"99.88" )

# Get
print(f"Retrieved device objectName: {BACnetDatabase.Get(1,2,3,77)}")
print(f"Retrieved device presentValue: {BACnetDatabase.Get(1,2,3,85)}")


# Arrays
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["presentvalue"], [True, True, False, True])
print(f"1 Retrieved network port presentValue: {BACnetDatabase.Get(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["presentvalue"])}")
BACnetDatabase.Set(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["presentvalue"], False, True, 1)
print(f"2 Retrieved network port presentValue: {BACnetDatabase.Get(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["presentvalue"])}")
print(f"3 Retrieved network port presentValue: {BACnetDatabase.Get(DEVICE_INSTANCE, bacnet_objectType["networkPort"], NETWORK_PORT_VERMILLION_INSTANCE, bacnet_propertyIdentifier["presentvalue"], True, 1)}")
exit()


"""

import ctypes
import json
try:
    from typing import Dict, List, Tuple, Any, Optional, Union
except ImportError:
    # For older Python versions, ignore type hints
    pass

class ExampleDatabase:
    def __init__(self):
        # Use nested dictionaries for flexible structure
        self.db = {}

    def Get(self, deviceInstance, objectType, objectInstance, propertyIdentifier, useArrayIndex=False, propertyArrayIndex=0):
        # Ensure all parameters are the correct type for dictionary keys
        try:
            deviceInstance = int(deviceInstance)
            objectType = int(objectType)
            objectInstance = int(objectInstance)
            propertyIdentifier = int(propertyIdentifier)
        except Exception:
            print(f"Invalid parameter type. All parameters must be convertible to int.")
            return None



        
        try:
            raw_value = self.db[deviceInstance][objectType][objectInstance][propertyIdentifier]
            if raw_value is None:
               return None
            
            if useArrayIndex:
                if isinstance(raw_value, list) and propertyArrayIndex < len(raw_value):
                    return str(raw_value[propertyArrayIndex])
                else:
                    print(f"Array index {propertyArrayIndex} out of range for property {propertyIdentifier}")
                    return None
            elif isinstance(raw_value, list):
                return raw_value
            else:
              return str(raw_value)
        except KeyError:
            print(f"Failed to retrieve value for Device {deviceInstance}, Object Type {objectType}, Instance {objectInstance}, Property {propertyIdentifier}")
            pass
        except Exception as e:
            print(f"Error retrieving value: {e}")

        return None

    def GetObjectsList(self, deviceInstance):
        try:
            objects = []
            for objectType, instances in self.db[deviceInstance].items():
                for objectInstance in instances.keys():
                    objects.append((objectType, objectInstance))
            return objects
        except KeyError:
            return []

    def Set(self, deviceInstance, objectType, objectInstance, propertyIdentifier, value, useArrayIndex=False, propertyArrayIndex=0):
        # Create nested dicts as needed
        if deviceInstance not in self.db:
            self.db[deviceInstance] = {}
        if objectType not in self.db[deviceInstance]:
            self.db[deviceInstance][objectType] = {}
        if objectInstance not in self.db[deviceInstance][objectType]:
            self.db[deviceInstance][objectType][objectInstance] = {}
        
        if useArrayIndex:
            if propertyIdentifier not in self.db[deviceInstance][objectType][objectInstance]:
                self.db[deviceInstance][objectType][objectInstance][propertyIdentifier] = []
            # Ensure the list is large enough
            while len(self.db[deviceInstance][objectType][objectInstance][propertyIdentifier]) <= propertyArrayIndex:
                self.db[deviceInstance][objectType][objectInstance][propertyIdentifier].append(None)
            # Set the value at the specified index
            self.db[deviceInstance][objectType][objectInstance][propertyIdentifier][propertyArrayIndex] = value
        else:
            # Directly set the value without array index
            if propertyIdentifier not in self.db[deviceInstance][objectType][objectInstance]:
                self.db[deviceInstance][objectType][objectInstance][propertyIdentifier] = value
            else:
                # Update existing property
                if isinstance(self.db[deviceInstance][objectType][objectInstance][propertyIdentifier], list):
                    # If it's a list, append the new value
                    self.db[deviceInstance][objectType][objectInstance][propertyIdentifier].append(value)
                else:
                    # Otherwise, just set the value
                    self.db[deviceInstance][objectType][objectInstance][propertyIdentifier] = value




    def Save(self, fileName):
        '''
        Serialize the database to a file.
        '''
        try:
            with open(fileName, 'w') as f:
                json.dump(self.db, f)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

    def Load(self, fileName):
        '''
        Load the database from a file.
        '''
        try:
            with open(fileName, 'r') as f:
                self.db = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            return False
    
