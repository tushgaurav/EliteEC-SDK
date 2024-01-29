# Elite EC Series Python SDK

## Introduction
There was no Python SDK for the Elite EC Series of Cobots, so I decided to make one. This SDK is based on the ELITE ROBOTS EC Series Programming Manual, provided by Elite Robots. The official manual provides functions that establish socket communication for controlling the robot. This SDK is the more pythonic version of the official manual.

## Usage
> Please insure that the robot is in remote mode when using this SDK.

You can ininsiate a robot class for each robot, the robot class requires IP address at the time of object creation.

```python
warehouse_bot = Robot("192.168.0.1")
```

You need to follow these steps to send commands to the robot.
1. Insinitate a new robot object with IP and Port (by default Robot class uses Port 8055).
2. Make connection to the robot.
3. Send commands to the robot using the execute function or set variables using setVariable function.
4. After usage is over, You should ideally disconnect the robot using disconnect function.

### Example Program

```python
import robot

warehouse_bot = Robot("192.168.0.1")

# Connect to the robot
connection, message = warehouse_bot.connect()
print(message)

if connection:
    # Accessing the value of System Variable B at address 1
    _, result = warehouse_bot.getVariable("SysVarB", 1)
    print("Value of SysVarB at addr 1: ", result)

    # Executing pause_trajectory command mentioned in the Programming Manual
    _, result = warehouse_bot.execute("pause_trajectory")
    print(result)

    # Disconnection the robot
    result, message = warehouse_bot.disconnect()
    print(message)
```

## Further Development
This SDK was made for the sole purpose of making my projects using this robot, easy to read and understand, the official "SDK", requires many lines of code to be written each time and it is difficult to understand.
