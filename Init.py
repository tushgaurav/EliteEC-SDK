from .SDK import *

def initSystem(robot_ip: str = "192.168.0.2", test_mode: bool = False) -> None:
    '''Initiliazes robot and set initial variables and
    runs the jbi file.'''

    robot_ip = "192.168.0.2"
    jbi_filename = "cashify"
    
    if test_mode:
        jbi_filename = "trial"

    conSuc, sock=connectETController(robot_ip)

    # Get Servo Status
    suc, result , id=sendCMD(sock, "getServoStatus")
    if ( result == 0):
        # Set the servo status of the robot arm to ON
        suc, result, id=sendCMD(sock,"set_servo_status",{"status":1})
        print("Servo Status: ", suc, result)
        time.sleep(1)

    if(conSuc):
        suc, result , id=sendCMD(sock,"checkJbiExist",{"filename": jbi_filename })
        if (suc and result ==1):
            # Run jbi file
            suc, result, id=sendCMD(sock,"runJbi",{"filename": jbi_filename })
            print("jbi Run Status: ", suc, result)

            # Set system B variable -> for qr code
            suc, result, id = sendCMD(sock, "getSysVarB", {"addr":0})
            print("System B Variable :", result)

            suc, result, id=sendCMD(sock,"setSysVarB",{"addr":0,"value":0})
            print("System B Variable Set to 0: ", suc, result)
    else:
        print("ERROR: Can't connect to robot.")
        print("Exiting...")
        sys.exit(100)



if __name__ == "__main__":
    initSystem()