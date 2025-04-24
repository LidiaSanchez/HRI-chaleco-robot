import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from pythonosc import udp_client

SERVER_IP = "192.168.123.54"
SERVER_PORT = 5005

class OSCClient(Node):
    def __init__(self):
        super().__init__('osc_cliente_movimiento_node')
        self.client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )
        self.last_position = None

    def pose_callback(self, msg):
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y
        print(f"Posición del robot: x={current_x}, y={current_y}")

        if self.last_position is None:
            self.last_position = (current_x, current_y)
            return

        last_x, last_y = self.last_position
        dx, dy = current_x - last_x, current_y - last_y
        self.last_position = (current_x, current_y)

        
        if dx != 0 or dy != 0:
            self.detect_direction(dx, dy)

    def detect_direction(self, dx, dy):
        if abs(dx) > abs(dy):  
            if dx > 0:
                print("Movimiento hacia la derecha")
                self.send_vibration("/vest_front", [2, 3, 6, 7])  # Derecha
            else:
                print("Movimiento hacia la izquierda")
                self.send_vibration("/vest_front", [0, 1, 4, 5])  # Izquierda
        else:  # Movimiento vertical
            if dy > 0:
                print("Movimiento hacia adelante")
                self.send_vibration("/vest_front", list(range(0, 10)))  
            else:
                print("Movimiento hacia atrás")
                self.send_vibration("/vest_back", list(range(0, 10)))  

    def send_vibration(self, address, indices):
        message = ",".join(map(str, indices))
        print(f"Enviando vibración a {address}: {message}")
        self.client.send_message(address, message)

def main(args=None):
    rclpy.init(args=args)
    osc_client = OSCClient()
    rclpy.spin(osc_client)
    osc_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
