import socket
import json


class Robot:
    def __init__(self, ip, port=8055):
        self.ip_address = ip
        self.port = port
        self.connect_success = False
        self.sock = None

    def sendCMD(self,cmd,params=None,id=1):
        sock = self.sock

        if(not params):
            params=[]
        else:
            params=json.dumps(params)
        sendStr="{{\"method\":\"{0}\",\"params\":{1} ,\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd,params,id)+"\n"
        
        try:
            sock.sendall(bytes(sendStr,"utf-8"))
            ret=sock.recv(1024)
            jdata=json.loads(str(ret,"utf-8"))
            if("result" in jdata.keys()):
                return (True,json.loads(jdata["result"]),jdata["id"])
            elif("error" in jdata.keys()):
                return (False,jdata["error"],jdata["id"])
            else:
                return (False,None,None)
        except Exception as e:
            return (False,None,None)

    def connect(self):
        def connectETController(ip,port=8055):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((ip,port))
                return (True,sock)
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
        
    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            return [True, "Robot Disconnect Success"]
        else:
            self.sock = None
            return [True, "Robot Disconnect Success, Robot was already disconected."]

    def execute(self, command, params):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, command, params)

            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not execute: {result}")
        else:
            return [False, "Robot not connected."]
        
    def getVariable(self, variable_type, variable_address):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, f"get{variable_type}", {"addr": variable_address})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not get variable: {result}")
        else:
            return [False, f"Robot not connected at IP:{self.ip_address}"]
        
    def setVariable(self, variable_type, variable_address, variable_value):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, f"set{variable_type}", {"addr": variable_address, "value": variable_value})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not set variable: {result}")
        else:
            return [False, f"Robot not connected at IP:{self.ip_address}"]

    def setServoStatus(self, status):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, "set_servo_status", {"status": status})
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not set servo status: {result}")
        else:
            return [False, f"Robot not connected at IP:{self.ip_address}"]
        
    def runJbi(self, jbi_filename):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, "checkJbiExist", {"filename": jbi_filename})
            if suc and result == 1:
                suc, result, id = self.sendCMD(self.sock, "runJbi", {"filename": jbi_filename})
                if suc:
                    return [id, result]
                else:
                    raise Exception(f"Can not run jbi: {result}")
            else:
                raise Exception(f"Can not run jbi: {result}")
        else:
            return [False, f"Robot not connected at IP:{self.ip_address}"]
    
    def getJbiState(self):
        if self.connect_success:
            suc, result, id = self.sendCMD(self.sock, "getJbiState")
            if suc:
                return [id, result]
            else:
                raise Exception(f"Can not get jbi state: {result}")
        else:
            return [False, f"Robot not connected at IP:{self.ip_address}"]
    
    def __repr__(self):
        return f'Robot Object at IP:{self.ip_address}, Connection:{self.connect_success}'
        
        
    







if __name__ == "__main__": 
    # robot_ip = "192.168.0.2"
    # i = 5
    # conSuc,sock=connectETController(robot_ip)
    # if(conSuc):
    #     suc,result,id=sendCMD(sock,"getCurrentCoord")
    #     for n in range (0, 11 ,1) :
    #         # Set system B variable value
    #         suc, result , id=sendCMD(sock,"setSysVarI",{"addr":i,"value":10})
    #         print(suc, result, id)

    robot = Robot("192.168.0.2")
    print(robot)
    result = robot.execute("setSysVarI", {"addr": 1, "value": 10})
    print(result)
    result = robot.getVariable("SysVarI", 1)
    print("getVariable", result)
    print(robot.disconnect())
    # print(robot.connect())

    # robot_ip = "192.168.0.2"
    # conSuc,sock=connectETController(robot_ip)

    # if (conSuc):
    # # Get the state of the robot servo alarm
    #     suc, result , id = sendCMD(sock, "get_actual_tcp",{"tool_num":1,"user_num":1})
    #     print( suc, result, id )
    # else :
    #     print ("Connection failed")
    #     disconnectETController(sock)

    # jbi_filename = "trial"

    # # servo status
    # suc, result , id=sendCMD(sock, "getServoStatus")
    # if ( result == 0):
    #     # Set the servo status of the robot arm to ON
    #     suc, result , id=sendCMD(sock,"set_servo_status",{"status":1})
    #     print("Servo Status")
    #     print(suc, result, id)
    #     time.sleep(1)

    # if (conSuc):
    #     # Check if the jbi file exists
    #     suc, result , id=sendCMD(sock,"checkJbiExist",{"filename": jbi_filename })
    #     if (suc and result ==1):
    #         # Run jbi file
    #         suc, result , id=sendCMD(sock,"runJbi",{"filename": jbi_filename })
    #         if (suc and result ) :
    #             checkRunning=3
    #             while(checkRunning==3):
    #                 # Get jbi file running status
    #                 suc, result , id=sendCMD(sock,"getJbiState")
    #                 checkRunning=result[" runState "]
    #                 time. sleep (0.1)
        
    
     
    # if(conSuc):
    #     suc, result , id=sendCMD(sock,"checkJbiExist",{"filename": jbi_filename })
    #     if (suc and result ==1):
    #         # Run jbi file
    #         suc, result , id=sendCMD(sock,"runJbi",{"filename": jbi_filename })
    #         print(suc, result, id)

    #         # set system B variable
    #         suc, result , id = sendCMD(sock, "getSysVarB", {"addr":0})
    #         print( result )

    #         suc, result , id=sendCMD(sock,"setSysVarB",{"addr":0,"value":11})
    #         print("Variable B set result")
    #         print(suc, result, id)
    # else:
    #     print("Cannot Connect to Robot")
    #     print("Exiting...")
    #     sys.exit(100)
    
def disconnectETController(sock):
    if (sock):
        sock.close()
        sock = None
    else:
        sock = None