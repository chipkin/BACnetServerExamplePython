# BACnet Server Example Python

A basic BACnet IP server example written with Python using the CAS BACnet Stack and CASBACnetRPC.

- Device: 389999 (Device Rainbow)
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

## CASBACnetRPC

The CASBACnetRPC is a Windows or Linux C++ application built using the [CAS BACnet Stack](https://www.bacnetstack.com/) with a [gRPC](https://grpc.io/) interface. The gRPC interface allows applications written in [Python](https://www.python.org/), and other non-compiled programming languages to access the BACnet IP/MSTP network.

The CASBACnetRPC middleware application is required because of the tight timing requirements of the BACnet MSTP protocol. The BACnet MSTP protocol requires a 3ms response time to any incoming messages. Non-real-time operating systems such as (Linux Ubuntu, or Windows) can not guaranteed response times and depending on the system load and the baud rate may have a hard time keeping up with this timing requirement. It is recommended to use a [BACnet IP to BACnet MSTP router](https://store.chipkin.com/products/bacnet-ip-to-bacnet-mstp-quickserver-gateway) instead of directly interacting with the BACnet MSTP network.

## Example output

```txt
BACnetServerExample v0.0.1
bacnet_rpc_version: 0.0.3.1
bacnet_stack_version: 3.13.8.0
CreateObject: Device (389999)
CreateObject: Analog Input (0)
CreateObject: Analog Output (1)
CreateObject: Analog Value (2)
CreateObject: Binary Input (3)
CreateObject: Binary Output (4)
CreateObject: Binary Value (5)
Configure BACnet IP
Configure BACnet MSTP
Done configuration
Updating AnalogInput (0) PresentValue = 0.01
Updating AnalogInput (0) PresentValue = 0.02
Updating AnalogInput (0) PresentValue = 0.03
Updating AnalogInput (0) PresentValue = 0.04
Updating AnalogInput (0) PresentValue = 0.05
Updating AnalogInput (0) PresentValue = 0.06
Updating AnalogInput (0) PresentValue = 0.07
Updating AnalogInput (0) PresentValue = 0.08
Updating AnalogInput (0) PresentValue = 0.09
```

## Building

This project also auto built using [Gitlab CI](https://docs.gitlab.com/ee/ci/) on every commit.
