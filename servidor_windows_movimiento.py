import argparse
from bhaptics import haptic_player
from pythonosc import dispatcher, osc_server

player = haptic_player.HapticPlayer()

def handle_front(unused_addr, args):
    print(f"Vibración en VestFront: {args}")
    indices = list(map(int, args.split(',')))
    feedback = [{"index": idx, "intensity": 100} for idx in indices]
    player.submit_dot("VestFront", "VestFront", feedback, 100)

def handle_back(unused_addr, args):
    print(f"Vibración en VestBack: {args}")
    indices = list(map(int, args.split(',')))
    feedback = [{"index": idx, "intensity": 100} for idx in indices]
    player.submit_dot("VestBack", "VestBack", feedback, 100)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="IP para escuchar")
    parser.add_argument("--port", type=int, default=5005, help="Puerto para escuchar")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/vest_front", handle_front)  
    dispatcher.map("/vest_back", handle_back)   

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print(f"Servidor ejecutándose en {server.server_address}")

    server.serve_forever()
