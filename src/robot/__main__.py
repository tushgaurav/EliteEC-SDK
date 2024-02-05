import warnings
import Logo
import SDK

warnings.filterwarnings('ignore')
print(Logo.Logo.ASCII_ART)
print(Logo.Logo.STRING_LOGO)


def main():
    ip_addr = input(
        "Enter the IP address of the robot (DEFAULT 192.168.0.2): ")
    port = input("Enter the port of the robot (DEFAULT 8055): ")

    if port == "":
        port = 8055

    if ip_addr == "":
        ip_addr = "192.168.0.2"

    print(f"Connecting to {ip_addr}:{port}...")

    robot = SDK.Robot(ip_addr, port)
    result, string = robot.connect()
    if result:
        print(f"Connected to {ip_addr}:{port} successfully!")
        print(string)
    else:
        print(f"Failed to connect to {ip_addr}:{port}!")
        print(string)
        return

    # Robot is connected now and we can start sending commands

    # Get servo status
    print("Getting Robot Status: ")
    print(robot.getStatus())

    print("Getting Robot Mode: ")
    print(robot.getRobotMode())

    print("Getting Robot Collision: ")
    print(robot.getCollisionStatus())

    print("Setting Collision State to TRUE: ")
    try:
        print(robot.setCollisionDetection(True))
    except Exception as e:
        print(e)

    while True:
        command = input("Enter a command: ")
        if command == "exit":
            break

        params = input("Enter the parameters (if any): ")

        output = robot.execute(command, params)
        print(output)

    print("Disconnecting from the robot...")
    robot.disconnect()


main()
