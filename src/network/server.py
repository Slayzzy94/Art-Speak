import socket
import threading
import json
from _thread import *
import random
import time

class GameServer:
    def __init__(self):
        self.server = "localhost"
        self.port = 5555
        self.init_socket()
        self.rooms = {}
        
    def init_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permettre la réutilisation de l'adresse
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.server, self.port))
            return True
        except Exception as e:
            print(f"Erreur d'initialisation du socket : {e}")
            return False
        
    def start(self):
        try:
            if not self.init_socket():
                print("Tentative de redémarrage du serveur dans 5 secondes...")
                time.sleep(5)
                if not self.init_socket():
                    print("Impossible de démarrer le serveur.")
                    return
            
            self.socket.listen(5)  # Accepter jusqu'à 5 connexions en attente
            print(f"Serveur démarré sur {self.server}:{self.port}")
            
            while True:
                try:
                    conn, addr = self.socket.accept()
                    print(f"Connecté à : {addr}")
                    start_new_thread(self.client_handler, (conn,))
                except Exception as e:
                    print(f"Erreur lors de l'acceptation de la connexion : {e}")
                    
        except KeyboardInterrupt:
            print("\nFermeture du serveur...")
        finally:
            self.socket.close()
            
    def stop(self):
        try:
            self.socket.close()
            print("Serveur arrêté.")
        except:
            pass

    def client_handler(self, conn):
        while True:
            try:
                data = conn.recv(2048).decode()
                if not data:
                    break
                    
                data = json.loads(data)
                response = {}
                
                if data["type"] == "create_room":
                    room_code = self.create_room()
                    if room_code:
                        # Créer la salle et y ajouter le créateur
                        self.rooms[room_code] = {
                            'players': [],
                            'current_turn': 0,
                            'words': [],
                            'drawings': [],
                            'connections': [conn],  # Ajouter directement le créateur
                            'game_started': False,
                            'current_phase': 'waiting',
                            'current_word': None,
                            'current_drawer': None,
                            'round': 0,
                            'max_rounds': 3
                        }
                        print(f"Salle créée : {room_code}")
                        response = {"success": True, "room_code": room_code}
                    else:
                        response = {"success": False, "error": "Erreur lors de la création de la salle"}
                
                elif data["type"] == "join_room":
                    result = self.join_room(data["room_code"], conn)
                    response = result
                    if result["success"]:
                        # Notifier tous les joueurs de la salle
                        self.broadcast_to_room(data["room_code"], {
                            "type": "player_joined",
                            "players": len(self.rooms[data["room_code"]]['connections'])
                        })
                
                elif data["type"] == "start_game":
                    if data["room_code"] in self.rooms:
                        room = self.rooms[data["room_code"]]
                        if len(room['connections']) >= 2:
                            room['game_started'] = True
                            room['current_phase'] = 'drawing'
                            room['current_drawer'] = 0
                            room['current_word'] = self.get_random_word()
                            response = {"success": True}
                            # Notifier tous les joueurs
                            self.broadcast_to_room(data["room_code"], {
                                "type": "game_started",
                                "current_word": room['current_word'],
                                "current_drawer": room['current_drawer']
                            })
                        else:
                            response = {"error": "Pas assez de joueurs"}
                    else:
                        response = {"error": "Salle introuvable"}
                
                elif data["type"] == "draw":
                    if data["room_code"] in self.rooms:
                        room = self.rooms[data["room_code"]]
                        # Vérifier si c'est le tour du joueur
                        if room['current_drawer'] == room['connections'].index(conn):
                            # Transmettre le dessin aux autres joueurs
                            self.broadcast_to_room(data["room_code"], {
                                "type": "draw_update",
                                "draw_data": data["draw_data"]
                            })
                
                elif data["type"] == "guess":
                    if data["room_code"] in self.rooms:
                        room = self.rooms[data["room_code"]]
                        # Vérifier si c'est la phase de devinette
                        if room['current_phase'] == 'guessing':
                            # Transmettre la devinette au dessinateur
                            drawer_conn = room['connections'][room['current_drawer']]
                            drawer_conn.send(json.dumps({
                                "type": "guess_received",
                                "guess": data["guess"]
                            }).encode())
                
                elif data["type"] == "end_turn":
                    if data["room_code"] in self.rooms:
                        room = self.rooms[data["room_code"]]
                        # Passer au joueur suivant
                        room['current_drawer'] = (room['current_drawer'] + 1) % len(room['connections'])
                        room['current_word'] = self.get_random_word()
                        
                        # Si tous les joueurs ont joué, passer à la phase de devinette
                        if room['current_drawer'] == 0:
                            room['current_phase'] = 'guessing'
                            room['round'] += 1
                            
                            # Si le nombre de tours est atteint, terminer la partie
                            if room['round'] >= room['max_rounds']:
                                self.end_game(data["room_code"])
                            else:
                                # Sinon, passer au tour suivant
                                room['current_phase'] = 'drawing'
                                self.broadcast_to_room(data["room_code"], {
                                    "type": "new_round",
                                    "round": room['round']
                                })
                        
                        # Notifier tous les joueurs
                        self.broadcast_to_room(data["room_code"], {
                            "type": "turn_ended",
                            "current_drawer": room['current_drawer'],
                            "current_word": room['current_word'],
                            "current_phase": room['current_phase']
                        })
                
                conn.send(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Erreur dans client_handler : {e}")
                break
        
        # Nettoyer les connexions à la déconnexion
        self.remove_player(conn)
        conn.close()

    def remove_player(self, conn):
        # Retirer le joueur de toutes les salles où il pourrait être
        for room_code, room in self.rooms.items():
            if conn in room['connections']:
                room['connections'].remove(conn)
                # Si la salle est vide, la supprimer
                if not room['connections']:
                    del self.rooms[room_code]
                    print(f"Salle supprimée : {room_code}")
                break

    def create_room(self):
        try:
            # Générer un code unique de 6 caractères
            code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            while code in self.rooms:  # S'assurer que le code est unique
                code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            
            # Créer la salle
            self.rooms[code] = {
                'players': [],
                'current_turn': 0,
                'words': [],
                'drawings': [],
                'connections': [],
                'game_started': False,
                'current_phase': 'waiting',  # waiting, drawing, guessing
                'current_word': None,
                'current_drawer': None,
                'round': 0,
                'max_rounds': 3
            }
            print(f"Salle créée avec le code : {code}")
            return code
        except Exception as e:
            print(f"Erreur lors de la création de la salle : {e}")
            return None

    def join_room(self, code, conn):
        try:
            if code in self.rooms:
                room = self.rooms[code]
                if len(room['connections']) < 4:  # Maximum 4 joueurs par salle
                    # Ajouter la connexion à la salle
                    room['connections'].append(conn)
                    print(f"Joueur rejoint la salle {code}")
                    return {"success": True, "room_code": code}
                else:
                    return {"success": False, "error": "La salle est pleine"}
            else:
                return {"success": False, "error": "Code de salle invalide"}
        except Exception as e:
            print(f"Erreur lors de la connexion à la salle : {e}")
            return {"success": False, "error": "Erreur lors de la connexion"}

    def broadcast_to_room(self, room_code, message):
        if room_code in self.rooms:
            room = self.rooms[room_code]
            for player_conn in room['connections']:
                try:
                    player_conn.send(json.dumps(message).encode())
                except:
                    continue

    def end_game(self, room_code):
        if room_code in self.rooms:
            room = self.rooms[room_code]
            # Calculer les scores et préparer les résultats
            results = {
                "type": "game_ended",
                "scores": self.calculate_scores(room)
            }
            # Envoyer les résultats à tous les joueurs
            self.broadcast_to_room(room_code, results)
            # Supprimer la salle
            del self.rooms[room_code]

    def calculate_scores(self, room):
        scores = {}
        for i, conn in enumerate(room['connections']):
            scores[i] = 0
            # Ajouter la logique de calcul des scores ici
        return scores

    def get_random_word(self):
        # Liste de mots simples pour le jeu
        words = ["chat", "chien", "maison", "voiture", "arbre", "fleur", "oiseau", "poisson", 
                 "livre", "crayon", "table", "chaise", "lune", "soleil", "étoile"]
        return random.choice(words)

if __name__ == "__main__":
    server = GameServer()
    server.start() 
