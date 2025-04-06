import socket
import json
import threading

class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"  # À changer avec l'adresse de votre serveur
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connected = False
        self.room_code = None
        self.player_id = None
        self.game_state = {
            'current_phase': 'waiting',
            'current_drawer': None,
            'current_word': None,
            'round': 0,
            'players': []
        }
        self.callbacks = {}
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            return True
        except ConnectionRefusedError:
            print("Impossible de se connecter au serveur. Assurez-vous que le serveur est en cours d'exécution.")
            return False
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return False
            
    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            response = json.loads(self.client.recv(2048).decode())
            
            # Gérer les réponses du serveur
            if "type" in response:
                self.handle_server_message(response)
                
            return response
        except Exception as e:
            print(f"Erreur lors de l'envoi des données : {e}")
            return {"error": str(e)}
            
    def start_listening(self, callback):
        def listen():
            while self.connected:
                try:
                    data = self.client.recv(2048).decode()
                    if data:
                        message = json.loads(data)
                        self.handle_server_message(message)
                        if callback:
                            callback(message)
                except:
                    break
        
        thread = threading.Thread(target=listen)
        thread.daemon = True
        thread.start()

    def handle_server_message(self, message):
        message_type = message.get("type")
        
        if message_type == "player_joined":
            self.game_state['players'] = message.get('players', [])
            if "on_player_joined" in self.callbacks:
                self.callbacks["on_player_joined"](message)
                
        elif message_type == "game_started":
            self.game_state['current_phase'] = 'drawing'
            self.game_state['current_drawer'] = message.get('current_drawer')
            self.game_state['current_word'] = message.get('current_word')
            if "on_game_started" in self.callbacks:
                self.callbacks["on_game_started"](message)
                
        elif message_type == "draw_update":
            if "on_draw_update" in self.callbacks:
                self.callbacks["on_draw_update"](message.get('draw_data'))
                
        elif message_type == "turn_ended":
            self.game_state['current_drawer'] = message.get('current_drawer')
            self.game_state['current_word'] = message.get('current_word')
            self.game_state['current_phase'] = message.get('current_phase')
            if "on_turn_ended" in self.callbacks:
                self.callbacks["on_turn_ended"](message)
                
        elif message_type == "new_round":
            self.game_state['round'] = message.get('round')
            if "on_new_round" in self.callbacks:
                self.callbacks["on_new_round"](message)
                
        elif message_type == "game_ended":
            if "on_game_ended" in self.callbacks:
                self.callbacks["on_game_ended"](message.get('scores'))

    def register_callback(self, event_type, callback):
        self.callbacks[event_type] = callback

    def create_room(self):
        response = self.send({"type": "create_room"})
        if "room_code" in response:
            self.room_code = response["room_code"]
            return self.room_code
        return None

    def join_room(self, room_code):
        response = self.send({
            "type": "join_room",
            "room_code": room_code
        })
        if response.get("success"):
            self.room_code = room_code
            return True
        return False

    def start_game(self):
        if not self.room_code:
            return False
        response = self.send({
            "type": "start_game",
            "room_code": self.room_code
        })
        return response.get("success", False)

    def send_draw_data(self, draw_data):
        if not self.room_code:
            return False
        return self.send({
            "type": "draw",
            "room_code": self.room_code,
            "draw_data": draw_data
        })

    def send_guess(self, guess):
        if not self.room_code:
            return False
        return self.send({
            "type": "guess",
            "room_code": self.room_code,
            "guess": guess
        })

    def end_turn(self):
        if not self.room_code:
            return False
        return self.send({
            "type": "end_turn",
            "room_code": self.room_code
        })

    def __del__(self):
        try:
            if self.connected:
                self.client.close()
        except:
            pass 
