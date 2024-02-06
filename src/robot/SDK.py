import socket
import json


class Robot:
    def __init__(self, ip, port=8055):
        self.ip_address = ip
        self.port = port
        self.connect_success = False
        self.sock = None

    def sendCMD(self, cmd, params=None, id=1):
        '''
        Note: This function should not be used directly, instead use the execute function.

        Internal Function to send commands to the robot.
        This function is essentially the same as mentioned in the 
        official Programming Manual.
        All commands are mentioned in the Programming Manual.

        Attributes:
            cmd (string): The command that we want to send.
            params (dict): If the commands requires additional parameters, specify here.

        '''
        sock = self.sock

        if (not params):
            params = []
        else:
            params = json.dumps(params)
        sendStr = "{{\"method\":\"{0}\",\"params\":{1} ,\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(
            cmd, params, id)+"\n"

        try:
            sock.sendall(bytes(sendStr, "utf-8"))
            ret = sock.recv(1024)
            jdata = json.loads(str(ret, "utf-8"))
            if ("result" in jdata.keys()):
                return (True, json.loads(jdata["result"]), jdata["id"])
            elif ("error" in jdata.keys()):
                return (False, jdata["error"], jdata["id"])
            else:
                return (False, None, None)
        except Exception as e:
            return (False, None, None)

    def connect(self) -> list:
        '''
        This function is used to establish a connection with the robot.

        Returns:
            list: [bool, str] -> [True, "Robot connected at IP (ACTUAL IP)"] or [False, "Cannot connect at IP (ACTUAL IP)"]
        '''
        def connectETController(ip, port=8055):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((ip, port))
                return (True, sock)
            except Exception as e:
                sock.close()
                return (False,)

        try:
            conSuc, sock = connectETController(self.ip_address)
        except:
            return [False, f"Cannot connect at IP:{self.ip_address}, check if robot is powered ON and connected to this system."]

        if conSuc:
            self.connect_success = conSuc
            self.sock = sock
            return [True, f"Robot connected at IP:{self.ip_address}"]
        else:
            return [False, f"Cannot connect at IP:{self.ip_address}"]

    def disconnect(self) -> list:
        '''
        This function is used to disconnect from the robot.

        Returns:
            list: [bool, str] -> [True, "Robot Disconnect Success"]
        '''
        if self.sock:
            self.sock.close()
            self.sock = None
            return [True, "Robot Disconnect Success"]
        else:
            self.sock = None
            return [True, "Robot Disconnect Success, Robot was already disconected."]

    def execute(self, command: str, params: dict=None) -> list:
        '''
        This function is used to execute commands on the robot. Better version of the official sendCMD function.

        Attributes:
            command (string): The command that we want to execute.
            params (dict): If the commands requires additional parameters, specify here.

        Returns:
            list: [int, str] -> [ID, "Result of the command"]
        '''
        if self.connect_success:
            if (not params):
                suc, result, id = self.sendCMD(command)
            else:
                suc, result, id = self.sendCMD(command, params)

            if suc:
                return [id, result]
            else:
                # Check if the not executed due to remote mode not enabled
                if result["code"] == -32693:
                    raise Exception(
                        f"Robot must be in Remote Mode to execute {command}. Enable remote mode from the teach pendant.")
                else:
                    raise Exception(f"Can not execute: {result}")
        else:
            return [False, "Robot not connected."]

    def getStatus(self) -> str:
        '''
        Get the status of the robot. The status can be one of the following:
        - STOP
        - PAUSE
        - EMERGENCY_STOP
        - RUNNING
        - ALARM
        - COLLISION

        Returns:
            str: The status of the robot.

        '''
        STATES = [
            "STOP",
            "PAUSE",
            "EMERGENCY_STOP",
            "RUNNING",
            "ALARM",
            "COLLISION",
        ]

        if self.connect_success:
            _, result = self.execute("getRobotState")
            return STATES[result]
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def getRobotMode(self) -> str:
        '''
        Get the mode of the robot. The mode can be one of the following:
        - TEACHING
        - OPERATING
        - REMOTE

        Returns:
            str: The mode of the robot.

        '''

        MODES = [
            "TEACHING",
            "OPERATING",
            "REMOTE"
        ]

        if self.connect_success:
            _, result = self.execute("getRobotMode")
            return MODES[result]
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    # Collision Options
    def getCollisionStatus(self) -> bool:
        '''
        Get the collision status of the robot.

        Returns:
            bool: True if collision is detected, False otherwise.

        '''

        if self.connect_success:
            _, result = self.execute("getCollisionEnable")
            return result == 1
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")


    def setCollisionDetection(self, status: bool) -> bool:
        '''
        Set the collision detection status of the robot.

        Attributes:
            status (bool): True to enable collision detection, False to disable.

        Returns:
            bool: True if collision detection status is set, False otherwise.

        '''
        if self.connect_success:
            _, result = self.execute("setCollisionEnable", {"enable": status})
            return result
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")
        

    def getVariable(self, variable_type: str, variable_address: int) -> list:
        '''
        This function is used to get the value of a variable from the robot.

        Attributes:
            variable_type (string): The type of variable we want to get, for example: SysVarI, SysVarB, etc.
            variable_address (int): The address of the variable we want to get.

        Returns:
            list: [int, str] -> [ID, Value of the variable]
        '''

        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, f"get{variable_type}", {
                                           "addr": variable_address})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not get variable: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def setVariable(self, variable_type: str, variable_address: int, variable_value: int) -> list:
        '''
        This function is used to set the value of a variable from the robot.

        Attributes:
            variable_type (string): The type of variable we want to set, for example: SysVarI, SysVarB, etc.
            variable_address (int): The address of the variable we want to set.
            variable_value (int): The value of the variable we want to set.

        Returns:
            list: [int, str] -> [ID, Result of the command]
        '''
        if self.connect_success:
            suc, result, id = self.sendCMD(f"set{variable_type}", {
                "addr": variable_address, "value": variable_value})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not set variable: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def setServoStatus(self, status: int) -> list:
        '''
        This function is used to set the servo status of the robot.

        Attributes:
            status (int): The status of the servo, 0 for OFF and 1 for ON.

        Returns:
            list: [int, str] -> [ID, Result of the command]
        '''
        if self.connect_success:
            suc, result, id = self.sendCMD(
                self.sock, "set_servo_status", {"status": status})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not set servo status: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def stopOperation(self) -> bool:
        '''
        This function is used to stop the robot operation.

        Returns:
            bool: True if the robot is stopped, False otherwise.
        '''
        if self.connect_success:
            suc, result, _ = self.execute("stop")
            if suc:
                return result
            else:
                raise Exception(f"Can not stop robot: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")
    
    def pause(self) -> bool:
        '''
        This function is used to pause the robot operation.

        Returns:
            bool: True if the robot is paused, False otherwise.
        '''
        if self.connect_success:
            suc, result, _ = self.execute("pause")
            if suc:
                return result
            else:
                raise Exception(f"Can not pause robot: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")
    
    def run(self) -> bool:
        '''
        This function is used to run the robot operation.

        Returns:
            bool: True if the robot is running, False otherwise.
        '''
        if self.connect_success:
            suc, result, _ = self.execute("run")
            if suc:
                return result
            else:
                raise Exception(f"Can not run robot: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")
        
    def setSpeed(self, speed) -> bool:
        '''
        This function is used to set the robot running speed.

        Attributes:
            speed (double [0.05,100]): The speed value.

        Returns:
            bool: True if the speed is set, False otherwise.
        '''
        if self.connect_success:
            id, result = self.execute("setSpeed", {"value": speed})
            return result
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")
        
    # JBI File Operations
    def checkJbiExist(self, jbi_filename: str) -> bool:
        '''
        This function is used to check if a jbi file exists on the robot.

        Attributes:
            jbi_filename (string): The name of the jbi file we want to check.

        Returns:
            bool: True if the jbi file exists, False otherwise.
        '''
        if self.connect_success:
            id, result = self.execute(
                "checkJbiExist", {"filename": jbi_filename})
            return result == 1
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def runJbi(self, jbi_filename) -> list:
        '''
        This function is used to run a jbi file on the robot.

        Attributes:
            jbi_filename (string): The name of the jbi file we want to run.

        Returns:
            list: [int, str] -> [ID, Result of the command]
        '''

        if self.connect_success:
            if self.checkJbiExist(jbi_filename):
                id, result = self.execute(
                    "runJbi", {"filename": jbi_filename})
                return [id, result]
            else:
                raise Exception(f"Jbi file {jbi_filename} does not exist.")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def getJbiState(self) -> list:
        '''
        This function is used to get the state of the jbi file running on the robot.

        Returns:
            list: [int, str] -> [ID, Result of the command]
        '''
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, "getJbiState")
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not get jbi state: {result}")
        else:
            raise Exception(f"Robot not connected at IP:{self.ip_address}")

    def __repr__(self):
        return f'Robot Object at IP:{self.ip_address}, Connection:{self.connect_success}'


if __name__ == "__main__":
    print("This is a library file, not a standalone script.")