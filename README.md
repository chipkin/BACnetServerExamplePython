# BACnet Server Example Python

A basic BACnet IP server example written with Python 3.7 using the [CAS BACnet Stack](https://www.bacnetstack.com/)

- Device: 389001 (Device Rainbow)
  - analog_input: 0 (AnalogInput Bronze)
  - analog_output: 1 (AnalogOutput Chartreuse)
  - analog_value: 2 (AnalogValue Diamond)
  - binary_input: 3 (BinaryInput Emerald)
  - binary_output: 4 (BinaryOutput Fuchsia)
  - binary_value: 5 (BinaryValue Gold)
  - multi_state_input: 13 (MultiStateInput Hot Pink)
  - multi_state_output: 14 (MultiStateOutput Indigo)
  - multi_state_value: 19 (MultiStateValue Kiwi)
  - characterstring_value: 40 (CharacterstringValue Nickel)
  - integer_value: 45 (IntegerValue Purple)
  - large_analog_value: 46 (LargeAnalogValue Quartz)
  - positive_integer_value: 48 (PositiveIntegerValue Silver)
  - NetworkPort: 56 (NetworkPort Umber)

## Example output

```txt
FYI: CAS BACnet Stack Python Server Example v0.0.4
FYI: https://github.com/chipkin/BACnetServerExamplePython
FYI: CAS BACnet Stack version: 3.25.0.0
FYI: CAS BACnet Stack python adapter version: 0.0.4
FYI: Connecting UDP Resource to port=[47808]
FYI: Local IP address:  [192, 168, 1, 130]
FYI: Registering the Callback Functions with the CAS BACnet Stack
FYI: Setting up server Device. device.instance=[389001]
FYI: Adding AnalogInput. AnalogInput.instance=[0]
FYI: Adding BinaryInput. BinaryInput.instance=[3]
FYI: Adding MultiStateInput. MultiStateInput.instance=[13]
FYI: Adding analogOutput. analogOutput.instance=[1]
FYI: Adding analogValue. analogValue.instance=[2]
FYI: Adding binaryOutput. binaryOutput.instance=[4]
FYI: Adding binaryValue. binaryValue.instance=[5]
FYI: Adding multiStateOutput. multiStateOutput.instance=[14]
FYI: Adding multiStateOutput. multiStateValue.instance=[15]
FYI: Adding characterstringValue. characterstringValue.instance=[40]
FYI: Adding integerValue. integerValue.instance=[45]
FYI: Adding largeAnalogValue. largeAnalogValue.instance=[46]
FYI: Adding positiveIntegerValue. positiveIntegerValue.instance=[48]
FYI: Adding networkPort. networkPort.instance=[50]
FYI: Sending I-AM broadcast
FYI: Entering main loop...
FYI: Updating AnalogInput (0) PresentValue:  99.7
FYI: Updating AnalogInput (0) PresentValue:  99.8
FYI: Updating AnalogInput (0) PresentValue:  99.9
FYI: Updating AnalogInput (0) PresentValue:  100.0
FYI: Updating AnalogInput (0) PresentValue:  100.1
FYI: Updating AnalogInput (0) PresentValue:  100.2
FYI: Updating AnalogInput (0) PresentValue:  100.3
FYI: Updating AnalogInput (0) PresentValue:  100.4
FYI: Updating AnalogInput (0) PresentValue:  100.5
FYI: Updating AnalogInput (0) PresentValue:  100.6
```

## Building

This python script requires the [CAS BACnet Stack](https://www.bacnetstack.com/) DLL that can be purchased from [Chipkin Automation Systems](https://store.chipkin.com).

Place the DLL in the root folder. 
For Windows: CASBACnetStack_x64_Release.dll and CASBACnetStack_x64_Debug.dll.
For Linux: libCASBACnetStack_x64_Release.so and CASBACnetStack_x64_Debug.so.

```bash
pip install pathlib
pip install dnspython
pip install netifaces
```

## Running

```bash
python BACnetServerExample.py

```

## Useful links

- [Python ctypes](https://docs.python.org/3/library/ctypes.html)
- [Python Bindings Overview](https://realpython.com/python-bindings-overview/)
- [CAS BACnet Explorer](https://store.chipkin.com/products/tools/cas-bacnet-explorer) - A BACnet Client that can be used to discover and poll this example BACnet Server.
