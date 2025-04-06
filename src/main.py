import pygame
import numpy as np
from math import sqrt, sin, cos, pi, atan2
import colorsys
import sys
import random
import os
import math
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from network.client import NetworkClient

class GarticPhone:
    def __init__(self):
        pygame.init()
        # Cacher le curseur par défaut
        pygame.mouse.set_visible(False)
        
        # Obtenir la résolution de l'écran
        screen_info = pygame.display.Info()
        
        # Définir une résolution minimale
        MIN_WIDTH = 1280
        MIN_HEIGHT = 720
        
        # Utiliser la plus grande valeur entre la résolution de l'écran et la résolution minimale
        self.WINDOW_WIDTH = max(screen_info.current_w, MIN_WIDTH)
        self.WINDOW_HEIGHT = max(screen_info.current_h, MIN_HEIGHT)
        
        # Calculer les ratios par rapport à la résolution de référence (1920x1080)
        self.scale_x = self.WINDOW_WIDTH / 1920
        self.scale_y = self.WINDOW_HEIGHT / 1080
        
        # Ajuster les dimensions du canvas pour qu'il ne soit pas trop grand sur les petits écrans
        max_canvas_width = self.WINDOW_WIDTH - 400  # Garder de l'espace pour les menus
        max_canvas_height = self.WINDOW_HEIGHT - 200  # Garder de l'espace pour les contrôles
        
        self.CANVAS_WIDTH = min(int(1400 * self.scale_x), max_canvas_width)
        self.CANVAS_HEIGHT = min(int(800 * self.scale_y), max_canvas_height)
        
        # Centrer le canvas si nécessaire
        self.CANVAS_X = (self.WINDOW_WIDTH - self.CANVAS_WIDTH) // 2
        self.CANVAS_Y = (self.WINDOW_HEIGHT - self.CANVAS_HEIGHT) // 3
        
        # Ajuster la taille des éléments UI pour les petits écrans
        min_scale = min(self.scale_x, self.scale_y, 1.0)  # Ne pas dépasser la taille originale
        
        # Configuration de la palette de couleurs
        self.COLORS_PER_ROW = 3  # Nombre de couleurs par ligne
        
        # Redimensionner les éléments de la palette de couleurs
        self.COLOR_SQUARE_SIZE = max(20, int(35 * min_scale))  # Taille minimale de 20px
        self.COLOR_MARGIN = max(4, int(8 * min_scale))  # Marge minimale de 4px
        self.COLOR_RECT_PADDING = max(8, int(15 * min_scale))  # Padding minimal de 8px
        
        # Couleurs pour le thème dark simple
        self.DARK_BG = (25, 25, 25)     # Fond principal
        self.ACCENT = (70, 130, 180)    # Bleu acier pour les accents
        self.WHITE = (255, 255, 255)    # Pour le canvas
        self.BLACK = (0, 0, 0)          # Pour le dessin
        self.BORDER = (45, 45, 48)      # Bordures
        self.TEXT = (230, 230, 230)     # Texte clair
        
        # Couleurs de l'interface cyberpunk
        self.NEON_PINK = (255, 20, 147)
        self.NEON_BLUE = (0, 255, 255)
        self.GRID_COLOR = (40, 40, 60)
        self.BORDER_COLOR = (0, 255, 255)
        
        # Palette de couleurs prédéfinies (sans le blanc)
        self.colors = [
            (0, 0, 0),        # Noir
            (128, 128, 128),  # Gris
            (255, 0, 0),      # Rouge
            (0, 255, 0),      # Vert
            (0, 0, 255),      # Bleu
            (255, 255, 0),    # Jaune
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (128, 0, 0),      # Rouge foncé
            (0, 128, 0),      # Vert foncé
            (0, 0, 128),      # Bleu foncé
            (128, 128, 0),    # Olive
            (128, 0, 128),    # Violet
            (0, 128, 128),    # Turquoise
            (255, 128, 0),    # Orange
            (255, 192, 203)   # Rose
        ]
        
        # Maintenant nous pouvons calculer les dimensions du rectangle des couleurs
        self.COLOR_RECT_WIDTH = (self.COLOR_SQUARE_SIZE * self.COLORS_PER_ROW) + (self.COLOR_MARGIN * (self.COLORS_PER_ROW - 1)) + (self.COLOR_RECT_PADDING * 2)
        self.COLOR_RECT_HEIGHT = (self.COLOR_SQUARE_SIZE * ((len(self.colors) + self.COLORS_PER_ROW - 1) // self.COLORS_PER_ROW)) + (self.COLOR_MARGIN * (((len(self.colors) + self.COLORS_PER_ROW - 1) // self.COLORS_PER_ROW) - 1)) + (self.COLOR_RECT_PADDING * 2)
        
        # Redimensionner les éléments principaux
        self.CANVAS_WIDTH = int(1400 * self.scale_x)
        self.CANVAS_HEIGHT = int(800 * self.scale_y)
        self.CANVAS_X = int(300 * self.scale_x)
        self.CANVAS_Y = int(50 * self.scale_y)
        
        # Calculer la position du rectangle des couleurs
        self.COLOR_RECT_X = self.CANVAS_X - self.COLOR_RECT_WIDTH - int(20 * self.scale_x)
        self.COLOR_RECT_Y = self.CANVAS_Y + (self.CANVAS_HEIGHT - self.COLOR_RECT_HEIGHT) // 2
        
        # Redimensionner le sélecteur de couleur
        self.COLOR_PICKER_X = int(50 * self.scale_x)
        self.COLOR_PICKER_Y = int(600 * self.scale_y)
        self.COLOR_PICKER_WIDTH = int(200 * self.scale_x)
        self.COLOR_PICKER_HEIGHT = int(350 * self.scale_y)
        self.SLIDER_HEIGHT = int(20 * self.scale_y)
        self.SLIDER_MARGIN = int(60 * self.scale_y)
        
        # Redimensionner le bouton pinceau
        self.BRUSH_BUTTON_WIDTH = int(50 * self.scale_x)
        self.BRUSH_BUTTON_HEIGHT = int(50 * self.scale_y)
        self.BRUSH_BUTTON_X = self.CANVAS_X + self.CANVAS_WIDTH + int(30 * self.scale_x)
        self.BRUSH_BUTTON_Y = int(50 * self.scale_y)
        
        # Redimensionner le curseur de taille du pinceau
        self.BRUSH_SLIDER_WIDTH = int(200 * self.scale_x)
        self.BRUSH_SLIDER_HEIGHT = int(20 * self.scale_y)
        self.BRUSH_SLIDER_X = self.CANVAS_X + (self.CANVAS_WIDTH - self.BRUSH_SLIDER_WIDTH) // 2
        self.BRUSH_SLIDER_Y = self.CANVAS_Y + self.CANVAS_HEIGHT + int(30 * self.scale_y)
        
        # Ajuster le nombre de particules en fonction de la taille de l'écran
        self.num_particles = int(100 * (self.WINDOW_WIDTH * self.WINDOW_HEIGHT) / (1920 * 1080))
        
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Art&Speak")
        
        # Configuration du canvas
        self.canvas_surface = pygame.Surface((self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        self.canvas_surface.fill(self.WHITE)  # Assurez-vous que le canvas est blanc
        
        # Configuration du sélecteur de couleur
        self.rgb_values = [255, 255, 255]
        self.current_color = (255, 255, 255)
        self.dragging_slider = None
        self.editing_value = None
        self.input_text = ""
        
        # État
        self.drawing = False
        self.points_buffer = []
        
        # Animation du fond
        self.particles = []
        for _ in range(self.num_particles):
            x = random.randint(0, self.WINDOW_WIDTH)
            y = random.randint(0, self.WINDOW_HEIGHT)
            speed = random.uniform(0.5, 2)
            size = random.randint(1, 3)
            alpha = random.randint(50, 200)
            color = random.choice([self.NEON_BLUE, self.NEON_PINK])  # Couleurs néon aléatoires
            self.particles.append({
                'x': x, 'y': y,
                'speed': speed,
                'size': size,
                'alpha': alpha,
                'color': color
            })

        self.clock = pygame.time.Clock()
        
        # Charger et redimensionner l'icône du pinceau
        self.brush_icon = pygame.image.load('brush_icon.png')
        button_size = int(self.BRUSH_BUTTON_WIDTH * 0.7)  # 70% de la taille du bouton
        self.brush_icon = pygame.transform.scale(self.brush_icon, (button_size, button_size))
        
        # Charger et redimensionner l'icône du pot de peinture
        self.paint_bucket_icon = pygame.image.load('paint_bucket_icon.png')
        self.paint_bucket_icon = pygame.transform.scale(self.paint_bucket_icon, (button_size, button_size))
        
        # Charger l'image de fond du menu
        self.menu_background = pygame.image.load('assets/74235825-fond-de-texture-dégradé-bleu-foncé-et-noir-matériau-de-surface-abstrait.jpg')
        # Redimensionner l'image pour qu'elle corresponde à la taille de la fenêtre
        self.menu_background = pygame.transform.scale(self.menu_background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        
        # Configuration du curseur de taille du pinceau
        self.MIN_BRUSH_SIZE = 1
        self.MAX_BRUSH_SIZE = 50
        self.brush_size = 5  # Taille initiale du pinceau
        self.dragging_brush_slider = False
        
        # État de l'application
        self.current_screen = "preface"  # "menu" ou "drawing"
        
        # Configuration du menu
        self.menu_title_font = pygame.font.SysFont('Arial', int(80 * min(self.scale_x, self.scale_y)))
        self.menu_button_font = pygame.font.SysFont('Arial', int(30 * min(self.scale_x, self.scale_y)))
        self.menu_button_hover = None
        self.menu_button_rects = {}
        
        # Configuration du bouton de fermeture
        close_button_size = 40
        self.close_button = {
            'rect': pygame.Rect(self.WINDOW_WIDTH - close_button_size - 20, 20, close_button_size, close_button_size),
            'hover': False
        }
        
        # Configuration du bouton de démarrage
        button_width = int(300 * min(self.scale_x, self.scale_y))
        button_height = int(60 * min(self.scale_x, self.scale_y))
        self.start_button = {
            'rect': pygame.Rect((self.WINDOW_WIDTH - button_width) // 2,
                               (self.WINDOW_HEIGHT + 100) // 2,
                               button_width, button_height),
            'text': 'CREATION LIBRE',
            'color': self.NEON_BLUE,
            'hover': False,
            'scale': 1.0,
            'target_scale': 1.0,
            'pulse_time': 0,
            'click_effect': 0
        }
        
        # Paramètres de transition
        self.transition = {
            'active': False,
            'progress': 0,
            'duration': 60,  # Nombre de frames pour la transition
            'type': None     # Type de transition (in/out)
        }

        # Ajouter des variables pour l'animation du curseur
        self.cursor_current_size = 0
        self.cursor_target_size = 0
        self.cursor_rotation = 0

        # Variables pour les effets dynamiques
        self.hover_effects = {
            'color_picker': {'scale': 1.0, 'target': 1.0},
            'brush_button': {'scale': 1.0, 'target': 1.0},
            'canvas_glow': 0
        }
        self.canvas_pulse = 0
        self.last_draw_time = 0

        # Historique des actions pour undo/redo
        self.canvas_history = []
        self.current_history_index = -1
        self.MAX_HISTORY = 50  # Limite de l'historique
        
        # Configuration des boutons d'outils
        button_size = int(40 * min(self.scale_x, self.scale_y))
        button_margin = int(10 * min(self.scale_x, self.scale_y))
        buttons_x = self.CANVAS_X + self.CANVAS_WIDTH + button_margin * 2
        
        # Première rangée (déplacée plus bas)
        self.BRUSH_BUTTON = {
            'rect': pygame.Rect(buttons_x, 
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2,
                               button_size, button_size),
            'active': True,
            'hover': False
        }
        
        self.PAINT_BUCKET_BUTTON = {
            'rect': pygame.Rect(buttons_x + button_size + button_margin, 
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2,
                               button_size, button_size),
            'active': False,
            'hover': False
        }
        
        # Deuxième rangée
        self.ERASER_BUTTON = {
            'rect': pygame.Rect(buttons_x, 
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2 + button_size + button_margin,
                               button_size, button_size),
            'active': False,
            'hover': False
        }
        
        self.LINE_BUTTON = {
            'rect': pygame.Rect(buttons_x + button_size + button_margin, 
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2 + button_size + button_margin,
                               button_size, button_size),
            'active': False,
            'hover': False
        }

        # Troisième rangée
        self.CIRCLE_BUTTON = {
            'rect': pygame.Rect(buttons_x, 
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2 + (button_size + button_margin) * 2,
                               button_size, button_size),
            'active': False,
            'hover': False
        }
        
        # Boutons undo/redo à côté du cercle
        self.UNDO_BUTTON = {
            'rect': pygame.Rect(buttons_x + button_size + button_margin,
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2 + (button_size + button_margin) * 2,
                               button_size, button_size),
            'hover': False,
            'scale': 1.0,
            'target_scale': 1.0,
            'click_animation': 0
        }
        
        self.REDO_BUTTON = {
            'rect': pygame.Rect(buttons_x + button_size + button_margin,
                               self.CANVAS_Y + self.CANVAS_HEIGHT // 2 + (button_size + button_margin) * 3,
                               button_size, button_size),
            'hover': False,
            'scale': 1.0,
            'target_scale': 1.0,
            'click_animation': 0
        }

        # Variables pour le cercle
        self.drawing_circle = False
        self.circle_start = None
        self.circle_end = None

        # Variables pour la ligne droite
        self.line_start = None
        self.line_end = None
        self.drawing_line = False
        
        # Sauvegarder l'état initial du canvas
        self.save_canvas_state()

        self.is_drawing = False  # Pour tracker si on est en train de dessiner

        # Ajouter des variables pour l'animation du fond
        self.background_time = 0
        self.wave_offset = 0

        # Nouvelles variables pour le mode chrono
        self.game_mode = None
        self.word_to_draw = None
        self.timer = 0
        # Configuration du mode chrono
        self.chrono_config = {
            'time_unit': 'seconds',  # 'seconds' ou 'minutes'
            'time_value': 60,  # Valeur par défaut
            'content_type': 'word',  # 'word' ou 'phrase'
            'buttons': {
                'back': pygame.Rect(20, 20, 100, 40),  # Bouton retour en haut à gauche
                'unit': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 - 200, 300, 50),
                'plus': pygame.Rect(self.WINDOW_WIDTH//2 + 100, self.WINDOW_HEIGHT//2 - 100, 50, 50),
                'minus': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 - 100, 50, 50),
                'word': pygame.Rect(self.WINDOW_WIDTH//2 - 200, self.WINDOW_HEIGHT//2 + 100, 180, 50),
                'phrase': pygame.Rect(self.WINDOW_WIDTH//2 + 20, self.WINDOW_HEIGHT//2 + 100, 180, 50),
                'start': pygame.Rect(self.WINDOW_WIDTH//2 - 100, self.WINDOW_HEIGHT//2 + 200, 200, 50)
            },
            'hover': None
        }

        # Charger les mots et phrases à dessiner
        self.words = self.load_words()
        self.phrases = self.load_phrases()

        # Ajouter le bouton retour
        self.BACK_BUTTON = {
            'rect': pygame.Rect(20, 20, 50, 50),  # Position en haut à gauche
            'hover': False
        }

        # Ajouter le bouton de sauvegarde
        self.SAVE_BUTTON = {
            'rect': pygame.Rect(self.WINDOW_WIDTH - 70, 20, 50, 50),  # Position en haut à droite
            'hover': False
        }

        # Importer tkinter pour la boîte de dialogue de sauvegarde
        self.root = tk.Tk()
        self.root.withdraw()  # Cacher la fenêtre principale de tkinter

        # Ajouter l'état de préface
        self.preface_alpha = 0  # Pour le fade in/out
        self.preface_stage = 0  # Pour gérer les différentes étapes de la préface
        self.preface_text = [
            "Bienvenue dans Gartic Phone",
            "Un jeu de dessin créatif",
            "Trois modes de jeu :",
            "Création libre : Dessinez ce que vous voulez",
            "Mode chronomètre : Relevez le défi du temps",
            "Mode multijoueur : Jouez avec vos amis !",
            "Cliquez pour continuer..."
        ]
        self.preface_timer = 0

        # Ajouter les variables pour le multijoueur
        self.network = None
        self.room_code = None
        self.players = []
        self.current_turn = 0
        self.is_host = False

        # Ajouter les variables pour l'édition RGB
        self.editing_rgb = None  # Index de la valeur RGB en cours d'édition (0=R, 1=G, 2=B)
        self.rgb_input_text = ""  # Texte en cours de saisie
        self.last_click_time = 0  # Pour détecter le double-clic
        self.double_click_delay = 500  # Délai maximum entre deux clics (en millisecondes)

        # Ajouter les variables pour l'animation de fin de chrono
        self.chrono_end_effect = {
            'active': False,
            'alpha': 0,
            'scale': 1.0,
            'rotation': 0,
            'duration': 120,  # Durée de l'animation en frames
            'progress': 0
        }

    def create_color_picker(self):
        surface = pygame.Surface((self.COLOR_PICKER_WIDTH, self.COLOR_PICKER_HEIGHT), pygame.SRCALPHA)
        
        # Fond principal avec coins arrondis
        pygame.draw.rect(surface, (30, 30, 35), 
                        (0, 0, self.COLOR_PICKER_WIDTH, self.COLOR_PICKER_HEIGHT),
                        border_radius=10)
        
        # Titre
        font = pygame.font.SysFont('Arial', 16)
        title = font.render('Couleur', True, self.TEXT)
        surface.blit(title, (20, 20))
        
        # Aperçu de la couleur
        preview_width = self.COLOR_PICKER_WIDTH - 40
        preview_rect = pygame.Rect(20, 50, preview_width, 40)
        pygame.draw.rect(surface, (20, 20, 25), preview_rect, border_radius=8)
        pygame.draw.rect(surface, self.current_color, preview_rect.inflate(-4, -4), border_radius=8)
        
        # Sliders RGB
        y_offset = 110
        slider_width = preview_width
        
        for i, (label, value) in enumerate(zip(['R', 'G', 'B'], self.rgb_values)):
            # Label et valeur
            if self.editing_rgb == i:
                # Afficher le texte en cours d'édition
                value_text = self.rgb_input_text + "_"  # Ajouter un curseur
                text_color = self.ACCENT  # Utiliser la couleur d'accent pour montrer l'édition
            else:
                value_text = str(value)
                text_color = self.TEXT
            
            text = font.render(f"{label}: {value_text}", True, text_color)
            surface.blit(text, (20, y_offset + i * 50))
            
            # Fond du slider
            slider_rect = pygame.Rect(20, y_offset + i * 50 + 25, slider_width, 8)
            pygame.draw.rect(surface, (20, 20, 25), slider_rect, border_radius=4)
            
            # Barre de progression
            progress_width = (value / 255) * slider_width
            if progress_width > 0:
                progress_rect = pygame.Rect(20, y_offset + i * 50 + 25, progress_width, 8)
                colors = [(220, 60, 60), (60, 220, 60), (60, 60, 220)]  # R, G, B
                pygame.draw.rect(surface, colors[i], progress_rect, border_radius=4)
            
            # Poignée du slider
            handle_x = 20 + progress_width
            handle_y = y_offset + i * 50 + 29
            pygame.draw.circle(surface, (20, 20, 25), (handle_x, handle_y), 10, 2)
            pygame.draw.circle(surface, self.TEXT, (handle_x, handle_y), 8)
            pygame.draw.circle(surface, (255, 255, 255, 30), (handle_x-1, handle_y-1), 4)
        
        return surface

    def handle_color_picker_click(self, pos):
        mouse_x, mouse_y = pos
        relative_x = mouse_x - self.COLOR_PICKER_X
        relative_y = mouse_y - self.COLOR_PICKER_Y
        
        # Vérifier si le clic est dans la zone des sliders
        slider_width = self.COLOR_PICKER_WIDTH - 40
        start_y = 110  # Position de départ des sliders
        spacing = 50   # Espacement entre les sliders
        
        for i in range(3):
            slider_y = start_y + (i * spacing)
            slider_rect = pygame.Rect(20, slider_y + 25, slider_width, 20)
            
            if (20 <= relative_x <= 20 + slider_width and 
                slider_y + 15 <= relative_y <= slider_y + 45):
                self.dragging_slider = i
                self.handle_slider_drag(pos)
                return True
        return False

    def handle_slider_drag(self, pos):
        if self.dragging_slider is not None:
            mouse_x, _ = pos
            slider_width = self.COLOR_PICKER_WIDTH - 40
            relative_x = mouse_x - (self.COLOR_PICKER_X + 20)
            # Limiter la valeur entre 0 et la largeur max
            relative_x = max(0, min(relative_x, slider_width))
            value = int((relative_x / slider_width) * 255)
            self.rgb_values[self.dragging_slider] = value
            self.current_color = tuple(self.rgb_values)

    def is_in_color_picker_area(self, pos):
        x, y = pos
        return (self.COLOR_PICKER_X <= x <= self.COLOR_PICKER_X + self.COLOR_PICKER_WIDTH and
                self.COLOR_PICKER_Y <= y <= self.COLOR_PICKER_Y + self.COLOR_PICKER_HEIGHT)

    def get_clicked_rgb_value(self, pos):
        # Convertir la position globale en position relative au color picker
        rel_x = pos[0] - self.COLOR_PICKER_X
        rel_y = pos[1] - self.COLOR_PICKER_Y
        
        # Vérifier si le clic est dans la zone des valeurs RGB
        y_offset = 110
        for i in range(3):
            # Zone de clic pour chaque valeur RGB
            value_rect = pygame.Rect(20, y_offset + i * 50, 60, 20)
            if value_rect.collidepoint(rel_x, rel_y):
                return i
        return None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = event.pos
                
                # Vérifier le double-clic sur les valeurs RGB
                current_time = pygame.time.get_ticks()
                if current_time - self.last_click_time < self.double_click_delay:
                    # C'est un double-clic, vérifier si on clique sur une valeur RGB
                    clicked_rgb = self.get_clicked_rgb_value(mouse_pos)
                    if clicked_rgb is not None:
                        self.editing_rgb = clicked_rgb
                        self.rgb_input_text = ""  # Commencer avec une chaîne vide
                        return
                self.last_click_time = current_time
                
                # Vérifier le clic sur le bouton retour en premier
                if self.BACK_BUTTON['rect'].collidepoint(mouse_pos):
                    # Réinitialiser le canvas
                    self.canvas_surface.fill(self.WHITE)
                    self.canvas_history = [self.canvas_surface.copy()]
                    self.current_history_index = 0
                    # Retourner au menu
                    self.current_screen = "menu"
                    self.game_mode = None
                    return
                
                # Vérifier les clics sur les boutons undo/redo
                if self.UNDO_BUTTON['rect'].collidepoint(mouse_pos):
                    self.UNDO_BUTTON['click_animation'] = 1.0
                    self.undo()
                    return
                if self.REDO_BUTTON['rect'].collidepoint(mouse_pos):
                    self.REDO_BUTTON['click_animation'] = 1.0
                    self.redo()
                    return
                
                # Vérifier le clic sur le bouton cercle
                if self.CIRCLE_BUTTON['rect'].collidepoint(mouse_pos):
                    self.CIRCLE_BUTTON['active'] = True
                    self.PAINT_BUCKET_BUTTON['active'] = False
                    self.BRUSH_BUTTON['active'] = False
                    self.ERASER_BUTTON['active'] = False
                    self.LINE_BUTTON['active'] = False
                    return

                # Vérifier le clic sur le bouton ligne droite
                if self.LINE_BUTTON['rect'].collidepoint(mouse_pos):
                    self.LINE_BUTTON['active'] = True
                    self.PAINT_BUCKET_BUTTON['active'] = False
                    self.BRUSH_BUTTON['active'] = False
                    self.ERASER_BUTTON['active'] = False
                    self.CIRCLE_BUTTON['active'] = False
                    return
                
                # Vérifier le clic sur le bouton pinceau
                if self.BRUSH_BUTTON['rect'].collidepoint(mouse_pos):
                    self.BRUSH_BUTTON['active'] = True
                    self.PAINT_BUCKET_BUTTON['active'] = False
                    self.ERASER_BUTTON['active'] = False
                    self.LINE_BUTTON['active'] = False
                    self.CIRCLE_BUTTON['active'] = False
                    return
                
                # Vérifier le clic sur le bouton gomme
                if self.ERASER_BUTTON['rect'].collidepoint(mouse_pos):
                    self.ERASER_BUTTON['active'] = True
                    self.PAINT_BUCKET_BUTTON['active'] = False
                    self.BRUSH_BUTTON['active'] = False
                    self.LINE_BUTTON['active'] = False
                    self.CIRCLE_BUTTON['active'] = False
                    return
                
                # Vérifier le clic sur le bouton pot de peinture
                if self.PAINT_BUCKET_BUTTON['rect'].collidepoint(mouse_pos):
                    self.PAINT_BUCKET_BUTTON['active'] = True
                    self.BRUSH_BUTTON['active'] = False
                    self.ERASER_BUTTON['active'] = False
                    self.LINE_BUTTON['active'] = False
                    self.CIRCLE_BUTTON['active'] = False
                    return

                # Vérifier le clic sur le curseur de taille du pinceau
                if (self.BRUSH_SLIDER_X <= mouse_pos[0] <= self.BRUSH_SLIDER_X + self.BRUSH_SLIDER_WIDTH and
                    self.BRUSH_SLIDER_Y <= mouse_pos[1] <= self.BRUSH_SLIDER_Y + self.BRUSH_SLIDER_HEIGHT):
                    self.dragging_brush_slider = True
                    self.update_brush_size(mouse_pos[0])
                    return
                
                # Vérifier les clics sur la palette de couleurs prédéfinies
                if (self.COLOR_RECT_X <= mouse_pos[0] <= self.COLOR_RECT_X + self.COLOR_RECT_WIDTH and
                    self.COLOR_RECT_Y <= mouse_pos[1] <= self.COLOR_RECT_Y + self.COLOR_RECT_HEIGHT):
                    rel_x = mouse_pos[0] - (self.COLOR_RECT_X + self.COLOR_RECT_PADDING)
                    rel_y = mouse_pos[1] - (self.COLOR_RECT_Y + self.COLOR_RECT_PADDING)
                    col = rel_x // (self.COLOR_SQUARE_SIZE + self.COLOR_MARGIN)
                    row = rel_y // (self.COLOR_SQUARE_SIZE + self.COLOR_MARGIN)
                    idx = row * self.COLORS_PER_ROW + col
                    if 0 <= idx < len(self.colors):
                        self.current_color = self.colors[idx]
                        self.rgb_values = list(self.current_color)
                        return
                
                # Vérifier si on clique sur une valeur RGB pour l'éditer
                clicked_value = self.get_clicked_rgb_value(mouse_pos)
                if clicked_value is not None:
                    self.editing_value = clicked_value
                    self.input_text = str(self.rgb_values[clicked_value])
                    return
                else:
                    self.editing_value = None
                
                # Vérifier les clics sur le sélecteur de couleur RGB
                if self.is_in_color_picker_area(mouse_pos):
                    self.handle_color_picker_click(mouse_pos)
                    return
                
                # Vérifier le clic sur le bouton de sauvegarde
                if self.SAVE_BUTTON['rect'].collidepoint(mouse_pos):
                    self.save_drawing()
                    return

                # Si on est sur le canvas
                if (self.CANVAS_X <= mouse_pos[0] <= self.CANVAS_X + self.CANVAS_WIDTH and
                    self.CANVAS_Y <= mouse_pos[1] <= self.CANVAS_Y + self.CANVAS_HEIGHT):
                    if self.CIRCLE_BUTTON['active']:
                        self.drawing_circle = True
                        self.circle_start = (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                        self.circle_end = self.circle_start
                        return
                    elif self.LINE_BUTTON['active']:
                        # Démarrer le dessin d'une ligne droite
                        self.drawing_line = True
                        self.line_start = (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                        self.line_end = (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                        return
                    elif self.PAINT_BUCKET_BUTTON['active']:
                        # Utiliser le pot de peinture
                        self.flood_fill(mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                    else:
                        # Dessin normal ou gomme
                        self.drawing = True
                        self.is_drawing = True
                        color = (255, 255, 255) if self.ERASER_BUTTON['active'] else self.current_color
                        pygame.draw.circle(self.canvas_surface, color, 
                                        (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y), 
                                        self.brush_size)
                        self.points_buffer = [(mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.drawing_line and self.LINE_BUTTON['active']:
                    # Dessiner la ligne finale
                    if self.line_start and self.line_end:
                        pygame.draw.line(self.canvas_surface, self.current_color, 
                                       self.line_start, self.line_end, self.brush_size)
                        self.save_canvas_state()
                    self.drawing_line = False
                    self.line_start = None
                    self.line_end = None
                    return
                
                if self.is_drawing:
                    # Sauvegarder l'état seulement à la fin du trait
                    self.save_canvas_state()
                self.drawing = False
                self.is_drawing = False
                self.dragging_slider = None
                self.dragging_brush_slider = False

                if self.drawing_circle and self.CIRCLE_BUTTON['active']:
                    # Dessiner le cercle final
                    if self.circle_start and self.circle_end:
                        center_x = (self.circle_start[0] + self.circle_end[0]) // 2
                        center_y = (self.circle_start[1] + self.circle_end[1]) // 2
                        radius = int(sqrt((self.circle_end[0] - self.circle_start[0])**2 + 
                                        (self.circle_end[1] - self.circle_start[1])**2) / 2)
                        pygame.draw.circle(self.canvas_surface, self.current_color, 
                                        (center_x, center_y), radius, self.brush_size)
                        self.save_canvas_state()
                    self.drawing_circle = False
                    self.circle_start = None
                    self.circle_end = None
                    return

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing_line and self.LINE_BUTTON['active']:
                mouse_pos = event.pos
                if (self.CANVAS_X <= mouse_pos[0] <= self.CANVAS_X + self.CANVAS_WIDTH and
                    self.CANVAS_Y <= mouse_pos[1] <= self.CANVAS_Y + self.CANVAS_HEIGHT):
                    self.line_end = (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                return
            
            if self.drawing:
                mouse_pos = event.pos
                if (self.CANVAS_X <= mouse_pos[0] <= self.CANVAS_X + self.CANVAS_WIDTH and
                    self.CANVAS_Y <= mouse_pos[1] <= self.CANVAS_Y + self.CANVAS_HEIGHT):
                    self.points_buffer.append((mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y))
                    self.draw_line(self.points_buffer)
                    self.points_buffer = [(mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)]
            
            if self.dragging_slider is not None:
                self.handle_slider_drag(event.pos)
            
            if self.dragging_brush_slider:
                self.update_brush_size(event.pos[0])

            if self.drawing_circle and self.CIRCLE_BUTTON['active']:
                mouse_pos = event.pos
                if (self.CANVAS_X <= mouse_pos[0] <= self.CANVAS_X + self.CANVAS_WIDTH and
                    self.CANVAS_Y <= mouse_pos[1] <= self.CANVAS_Y + self.CANVAS_HEIGHT):
                    self.circle_end = (mouse_pos[0] - self.CANVAS_X, mouse_pos[1] - self.CANVAS_Y)
                return

            # Mettre à jour l'état de survol des boutons
            mouse_pos = pygame.mouse.get_pos()
            self.UNDO_BUTTON['hover'] = self.UNDO_BUTTON['rect'].collidepoint(mouse_pos)
            self.REDO_BUTTON['hover'] = self.REDO_BUTTON['rect'].collidepoint(mouse_pos)

            # Mettre à jour l'état de survol du bouton retour
            self.BACK_BUTTON['hover'] = self.BACK_BUTTON['rect'].collidepoint(mouse_pos)

            # Mettre à jour l'état de survol du bouton de sauvegarde
            self.SAVE_BUTTON['hover'] = self.SAVE_BUTTON['rect'].collidepoint(mouse_pos)

        elif event.type == pygame.KEYDOWN:
            if self.editing_rgb is not None:
                if event.key == pygame.K_RETURN:
                    # Valider la saisie
                    try:
                        value = min(255, max(0, int(self.rgb_input_text or "0")))  # Utiliser 0 si vide
                        self.rgb_values[self.editing_rgb] = value
                        self.current_color = tuple(self.rgb_values)
                    except ValueError:
                        pass  # Ignorer les valeurs invalides
                    self.editing_rgb = None
                    self.rgb_input_text = ""
                elif event.key == pygame.K_ESCAPE:
                    # Annuler la saisie
                    self.editing_rgb = None
                    self.rgb_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    # Permettre la suppression
                    self.rgb_input_text = self.rgb_input_text[:-1]
                elif event.unicode.isdigit():
                    # N'accepter que les chiffres et limiter la longueur à 3 caractères
                    if len(self.rgb_input_text) < 3:
                        self.rgb_input_text += event.unicode
                        # Vérifier si la valeur ne dépasse pas 255
                        try:
                            value = int(self.rgb_input_text)
                            if value > 255:
                                self.rgb_input_text = "255"
                        except ValueError:
                            pass

    def draw_line(self, points):
        if len(points) < 2:
            return
        
        p1, p2 = points
        x1, y1 = p1
        x2, y2 = p2
        
        dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if dist < 1:
            return
        
        steps = max(int(dist), 1)
        
        # Utiliser la couleur blanche pour la gomme
        color = (255, 255, 255) if self.ERASER_BUTTON['active'] else self.current_color
        
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            pygame.draw.circle(self.canvas_surface, color, (x, y), self.brush_size)
        
        # Augmenter l'effet de lueur du canvas
        self.hover_effects['canvas_glow'] = min(1.0, self.hover_effects['canvas_glow'] + 0.1)
        self.last_draw_time = pygame.time.get_ticks()
        
        # Ne plus sauvegarder l'état ici, on le fait à la fin du trait

    def draw_canvas_border(self):
        # Simple bordure autour du canvas
        outer_rect = pygame.Rect(self.CANVAS_X - 2, self.CANVAS_Y - 2,
                                self.CANVAS_WIDTH + 4, self.CANVAS_HEIGHT + 4)
        pygame.draw.rect(self.screen, self.BORDER, outer_rect, 2)

    def draw_color_picker(self):
        # Rectangle de la palette de couleurs avec style simple
        color_rect = pygame.Rect(self.COLOR_RECT_X, self.COLOR_RECT_Y,
                               self.COLOR_RECT_WIDTH, self.COLOR_RECT_HEIGHT)
        pygame.draw.rect(self.screen, self.DARK_BG, color_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER, color_rect, 2, border_radius=5)

    def draw_custom_cursor(self, pos):
        if not pygame.mouse.get_focused():
            return
        
        x, y = pos
        
        if self.current_screen == "preface" or self.current_screen == "menu":
            # Curseur blanc pour le menu et la préface
            pygame.draw.circle(self.screen, (255, 255, 255), pos, 5, 2)
        else:
            # Curseur pour l'écran de dessin
            on_canvas = (self.CANVAS_X <= x <= self.CANVAS_X + self.CANVAS_WIDTH and
                        self.CANVAS_Y <= y <= self.CANVAS_Y + self.CANVAS_HEIGHT)
            
            if on_canvas:
                if self.ERASER_BUTTON['active']:
                    # Curseur gomme sur canvas (noir)
                    cursor_size = max(8, self.brush_size)
                    pygame.draw.circle(self.screen, (50, 50, 50), pos, cursor_size, 2)
                else:
                    # Curseur pinceau sur canvas (noir)
                    cursor_size = max(8, self.brush_size)
                    pygame.draw.circle(self.screen, (50, 50, 50), pos, cursor_size, 2)
            else:
                # Curseur hors canvas (blanc)
                pygame.draw.circle(self.screen, (230, 230, 230), pos, 5, 2)

    def draw_brush_size_slider(self):
        # Fond du slider
        slider_rect = pygame.Rect(self.BRUSH_SLIDER_X, self.BRUSH_SLIDER_Y,
                                self.BRUSH_SLIDER_WIDTH, self.BRUSH_SLIDER_HEIGHT)
        pygame.draw.rect(self.screen, self.DARK_BG, slider_rect, border_radius=4)
        pygame.draw.rect(self.screen, self.BORDER, slider_rect, 2, border_radius=4)
        
        # Barre de progression
        percentage = (self.brush_size - self.MIN_BRUSH_SIZE) / (self.MAX_BRUSH_SIZE - self.MIN_BRUSH_SIZE)
        progress_width = self.BRUSH_SLIDER_WIDTH * percentage
        
        if progress_width > 0:
            progress_rect = pygame.Rect(self.BRUSH_SLIDER_X, self.BRUSH_SLIDER_Y,
                                      progress_width, self.BRUSH_SLIDER_HEIGHT)
            pygame.draw.rect(self.screen, self.ACCENT, progress_rect, border_radius=4)
        
        # Poignée
        handle_x = self.BRUSH_SLIDER_X + progress_width
        handle_y = self.BRUSH_SLIDER_Y + self.BRUSH_SLIDER_HEIGHT // 2
        pygame.draw.circle(self.screen, self.TEXT, (handle_x, handle_y), 6)

        # Afficher la taille actuelle en petit
        font = pygame.font.Font(None, 20)  # Taille de police réduite
        size_text = font.render(f"{self.brush_size}px", True, self.TEXT)
        text_rect = size_text.get_rect(midtop=(self.BRUSH_SLIDER_X + self.BRUSH_SLIDER_WIDTH // 2,
                                             self.BRUSH_SLIDER_Y - 15))  # Position plus proche du slider
        self.screen.blit(size_text, text_rect)

    def draw_undo_redo_buttons(self):
        for button, is_undo in [(self.UNDO_BUTTON, True), (self.REDO_BUTTON, False)]:
            # Animation au survol et au clic
            if button['hover']:
                button['target_scale'] = 1.1
            else:
                button['target_scale'] = 1.0
            
            # Animation fluide
            button['scale'] += (button['target_scale'] - button['scale']) * 0.2
            
            # Animation de clic
            if button['click_animation'] > 0:
                button['click_animation'] *= 0.8  # Diminuer progressivement
                scale = button['scale'] * (1 - button['click_animation'] * 0.2)
            else:
                scale = button['scale']
            
            # Calculer le rectangle mis à l'échelle
            scaled_rect = button['rect'].copy()
            scaled_rect.width *= scale
            scaled_rect.height *= scale
            scaled_rect.center = button['rect'].center
            
            # Fond du bouton
            if button['hover']:
                pygame.draw.rect(self.screen, (35, 35, 40), scaled_rect, border_radius=5)
            
            # Bordure
            pygame.draw.rect(self.screen, self.BORDER, scaled_rect, 2, border_radius=5)
            
            # Flèche
            arrow_points = self.get_arrow_points(scaled_rect, is_undo)
            pygame.draw.polygon(self.screen, self.TEXT, arrow_points)

    def draw(self):
        # Ajuster la position du canvas et du slider pour le mode chrono
        if self.game_mode == "chrono":
            canvas_y_offset = 100  # Espace pour le texte et le timer
            self.CANVAS_Y = (self.WINDOW_HEIGHT - self.CANVAS_HEIGHT) // 3 + canvas_y_offset
            self.BRUSH_SLIDER_Y = self.CANVAS_Y + self.CANVAS_HEIGHT + int(30 * self.scale_y)
        else:
            # Position normale pour le mode création libre
            self.CANVAS_Y = (self.WINDOW_HEIGHT - self.CANVAS_HEIGHT) // 3
            self.BRUSH_SLIDER_Y = self.CANVAS_Y + self.CANVAS_HEIGHT + int(30 * self.scale_y)
        
        # Dessiner le fond animé
        self.draw_background()
        
        # Afficher le mot à dessiner et le chronomètre avant le canvas en mode chrono
        if self.game_mode == "chrono":
            font = pygame.font.Font(None, 40)
            # Mot à dessiner
            word_text = font.render(f"Dessinez : {self.word_to_draw}", True, self.TEXT)
            word_rect = word_text.get_rect(midtop=(self.WINDOW_WIDTH // 2, 20))
            self.screen.blit(word_text, word_rect)
            
            # Chronomètre
            if self.timer >= 60:
                minutes = int(self.timer // 60)
                seconds = int(self.timer % 60)
                time_text = font.render(f"Temps : {minutes}m {seconds}s", True, self.TEXT)
            else:
                time_text = font.render(f"Temps : {int(self.timer)}s", True, self.TEXT)
            time_rect = time_text.get_rect(midtop=(self.WINDOW_WIDTH // 2, 60))
            self.screen.blit(time_text, time_rect)
        
        # Canvas
        self.screen.blit(self.canvas_surface, (self.CANVAS_X, self.CANVAS_Y))
        
        # Ajouter la bordure néon du canvas
        self.draw_canvas_border()
        
        # Rectangle contenant la palette de couleurs avec style simple
        self.draw_color_picker()
        
        # Palette de couleurs prédéfinies
        for i, color in enumerate(self.colors):
            row = i // self.COLORS_PER_ROW
            col = i % self.COLORS_PER_ROW
            x = self.COLOR_RECT_X + self.COLOR_RECT_PADDING + col * (self.COLOR_SQUARE_SIZE + self.COLOR_MARGIN)
            y = self.COLOR_RECT_Y + self.COLOR_RECT_PADDING + row * (self.COLOR_SQUARE_SIZE + self.COLOR_MARGIN)
            
            # Rectangle de couleur avec effet néon
            color_rect = pygame.Rect(x, y, self.COLOR_SQUARE_SIZE, self.COLOR_SQUARE_SIZE)
            pygame.draw.rect(self.screen, color, color_rect)
            if color == self.current_color:
                pygame.draw.rect(self.screen, self.ACCENT, color_rect, 2)
                # Effet de lueur
                pygame.draw.rect(self.screen, self.TEXT, color_rect.inflate(4, 4), 1)
        
        # Sélecteur de couleur RGB
        color_picker = self.create_color_picker()
        self.screen.blit(color_picker, (self.COLOR_PICKER_X, self.COLOR_PICKER_Y))
        
        # Bouton pinceau
        self.draw_tool_buttons()
        
        # Ajouter le curseur de taille du pinceau
        self.draw_brush_size_slider()
        
        # Dessiner les boutons undo/redo
        self.draw_undo_redo_buttons()
        
        # Dessiner le bouton de sauvegarde
        if self.SAVE_BUTTON['hover']:
            button_color = (45, 45, 50)
        else:
            button_color = (35, 35, 40)
        
        # Fond du bouton de sauvegarde
        pygame.draw.rect(self.screen, button_color, self.SAVE_BUTTON['rect'], border_radius=10)
        pygame.draw.rect(self.screen, self.ACCENT, self.SAVE_BUTTON['rect'], 2, border_radius=10)
        
        # Icône de sauvegarde
        save_icon_rect = self.SAVE_BUTTON['rect'].inflate(-20, -20)
        pygame.draw.circle(self.screen, self.TEXT, save_icon_rect.center, 10)
        pygame.draw.circle(self.screen, button_color, save_icon_rect.center, 6)
        triangle_points = [
            (save_icon_rect.centerx, save_icon_rect.top + 2),
            (save_icon_rect.centerx - 8, save_icon_rect.top + 10),
            (save_icon_rect.centerx + 8, save_icon_rect.top + 10)
        ]
        pygame.draw.polygon(self.screen, self.TEXT, triangle_points)
        
        # Dessiner le bouton retour
        if self.BACK_BUTTON['hover']:
            back_button_color = (45, 45, 50)
        else:
            back_button_color = (35, 35, 40)
        
        # Fond du bouton retour
        pygame.draw.rect(self.screen, back_button_color, self.BACK_BUTTON['rect'], border_radius=10)
        pygame.draw.rect(self.screen, self.ACCENT, self.BACK_BUTTON['rect'], 2, border_radius=10)
        
        # Flèche de retour
        arrow_points = [
            (self.BACK_BUTTON['rect'].centerx + 10, self.BACK_BUTTON['rect'].centery),  # Pointe droite
            (self.BACK_BUTTON['rect'].centerx - 10, self.BACK_BUTTON['rect'].centery),  # Pointe gauche
            (self.BACK_BUTTON['rect'].centerx - 5, self.BACK_BUTTON['rect'].centery - 8),  # Haut
            (self.BACK_BUTTON['rect'].centerx - 10, self.BACK_BUTTON['rect'].centery),  # Pointe gauche
            (self.BACK_BUTTON['rect'].centerx - 5, self.BACK_BUTTON['rect'].centery + 8),  # Bas
        ]
        pygame.draw.polygon(self.screen, self.TEXT, arrow_points)
        
        # Ajouter la transition par-dessus tout
        if self.transition['active']:
            self.draw_transition()
        
        # Dessiner le curseur personnalisé en DERNIER
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        # Ajouter l'effet de fin de chrono par-dessus tout
        if self.chrono_end_effect['active']:
            self.draw_chrono_end_effect()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Afficher l'image de fond
        self.screen.blit(self.menu_background, (0, 0))
        
        # Ajouter un overlay semi-transparent pour assurer la lisibilité du texte
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.fill(self.DARK_BG)
        overlay.set_alpha(100)  # Réduit de 180 à 100 pour rendre l'image plus visible
        self.screen.blit(overlay, (0, 0))
        
        # Dessiner le bouton de fermeture
        close_button_color = (45, 45, 50) if self.close_button['hover'] else (35, 35, 40)
        pygame.draw.rect(self.screen, close_button_color, self.close_button['rect'], border_radius=10)
        pygame.draw.rect(self.screen, self.ACCENT, self.close_button['rect'], 2, border_radius=10)
        
        # Dessiner la croix
        cross_color = (255, 255, 255)
        margin = 12
        # Ligne horizontale
        pygame.draw.line(self.screen, cross_color,
                        (self.close_button['rect'].left + margin, self.close_button['rect'].centery),
                        (self.close_button['rect'].right - margin, self.close_button['rect'].centery),
                        3)
        # Ligne verticale
        pygame.draw.line(self.screen, cross_color,
                        (self.close_button['rect'].centerx, self.close_button['rect'].top + margin),
                        (self.close_button['rect'].centerx, self.close_button['rect'].bottom - margin),
                        3)
        
        # Titre "Art&Speak" avec effet moderne
        title_font = pygame.font.Font(None, 120)
        title_shadow = title_font.render("Art&Speak", True, (40, 40, 45))
        title_text = title_font.render("Art&Speak", True, self.TEXT)
        
        # Position du titre (remonté)
        title_x = self.WINDOW_WIDTH // 2
        title_y = self.WINDOW_HEIGHT // 4  # Changé de //3 à //4 pour remonter le titre
        
        # Effet de profondeur subtil pour le titre
        for i in range(3):
            shadow_rect = title_shadow.get_rect(center=(title_x + i, title_y + i))
            self.screen.blit(title_shadow, shadow_rect)
        
        # Titre principal
        title_rect = title_text.get_rect(center=(title_x, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Premier bouton (CREATION LIBRE)
        button_width = 320
        button_height = 90
        button_margin = 30
        button_x = self.WINDOW_WIDTH // 2 - button_width // 2
        button_y = self.WINDOW_HEIGHT // 2 - 100  # Remonté de 100 pixels par rapport au centre
        
        # Effet de survol pour CREATION LIBRE
        if self.menu_button_hover == "libre":
            glow_surface = pygame.Surface((button_width + 20, button_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.ACCENT[:3], 30),
                            (0, 0, button_width + 20, button_height + 20),
                            border_radius=20)
            self.screen.blit(glow_surface, (button_x - 10, button_y - 10))
            button_color = (45, 45, 50)
        else:
            button_color = (35, 35, 40)
        
        # Dessiner le premier bouton
        pygame.draw.rect(self.screen, button_color,
                        (button_x, button_y, button_width, button_height),
                        border_radius=20)
        pygame.draw.rect(self.screen, (*self.ACCENT[:3], 150),
                        (button_x, button_y, button_width, button_height),
                        2, border_radius=20)
        
        # Texte du premier bouton
        button_font = pygame.font.Font(None, 55)
        button_text = button_font.render("CREATION LIBRE", True, self.TEXT)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, 
                                               button_y + button_height//2))
        self.screen.blit(button_text, text_rect)
        
        # Deuxième bouton (CHRONOMETRE)
        button2_y = button_y + button_height + button_margin
        
        # Effet de survol pour CHRONOMETRE
        if self.menu_button_hover == "chrono":
            glow_surface = pygame.Surface((button_width + 20, button_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.ACCENT[:3], 30),
                            (0, 0, button_width + 20, button_height + 20),
                            border_radius=20)
            self.screen.blit(glow_surface, (button_x - 10, button2_y - 10))
            button2_color = (45, 45, 50)
        else:
            button2_color = (35, 35, 40)
        
        # Dessiner le deuxième bouton
        pygame.draw.rect(self.screen, button2_color,
                        (button_x, button2_y, button_width, button_height),
                        border_radius=20)
        pygame.draw.rect(self.screen, (*self.ACCENT[:3], 150),
                        (button_x, button2_y, button_width, button_height),
                        2, border_radius=20)
        
        # Texte du deuxième bouton
        button_text = button_font.render("CHRONOMETRE", True, self.TEXT)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, 
                                               button2_y + button_height//2))
        self.screen.blit(button_text, text_rect)
        
        # Troisième bouton (MULTIJOUEUR)
        button3_y = button2_y + button_height + button_margin
        
        if self.menu_button_hover == "multi":
            button3_color = (45, 45, 50)
        else:
            button3_color = (35, 35, 40)
        
        pygame.draw.rect(self.screen, button3_color,
                        (button_x, button3_y, button_width, button_height),
                        border_radius=20)
        pygame.draw.rect(self.screen, (*self.ACCENT[:3], 150),
                        (button_x, button3_y, button_width, button_height),
                        2, border_radius=20)
        
        button_text = button_font.render("MULTIJOUEUR", True, self.TEXT)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, 
                                               button3_y + button_height//2))
        self.screen.blit(button_text, text_rect)
        
        # Mettre à jour les zones de clic des boutons
        self.menu_button_rects = {
            "libre": pygame.Rect(button_x, button_y, button_width, button_height),
            "chrono": pygame.Rect(button_x, button2_y, button_width, button_height),
            "multi": pygame.Rect(button_x, button3_y, button_width, button_height)
        }
        
        # Dessiner le curseur personnalisé
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        # Afficher la transition si active
        if self.transition['active']:
            self.draw_transition()
        
        # Important : mettre à jour l'affichage
        pygame.display.flip()

    def handle_menu_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Mettre à jour l'état de survol des boutons
            mouse_pos = event.pos
            self.menu_button_hover = None
            for button_type, rect in self.menu_button_rects.items():
                if rect.collidepoint(mouse_pos):
                    self.menu_button_hover = button_type
                    break
            
            # Mettre à jour l'état de survol du bouton de fermeture
            self.close_button['hover'] = self.close_button['rect'].collidepoint(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.transition['active']:
                # Vérifier le clic sur le bouton de fermeture
                if self.close_button['rect'].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                
                if self.menu_button_hover == "libre":
                    self.game_mode = "libre"
                    self.start_transition('out')
                elif self.menu_button_hover == "chrono":
                    self.game_mode = "chrono"
                    self.current_screen = "chrono_config"
                elif self.menu_button_hover == "multi":
                    self.game_mode = "multi"
                    self.show_multiplayer_menu()

    def show_multiplayer_menu(self):
        # Initialiser le client réseau si pas déjà fait
        try:
            if not self.network:
                self.network = NetworkClient()
                if not self.network.connect():  # Tester la connexion immédiatement
                    raise Exception("Impossible de se connecter au serveur")
        except Exception as e:
            print(f"Erreur réseau : {e}")
            self.multi_menu = {
                'active': True,
                'buttons': {
                    'create': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 - 60, 300, 50),
                    'join': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 + 10, 300, 50)
                },
                'hover': None,
                'room_code': '',
                'joining': False,
                'error_message': "Serveur non disponible"
            }
        else:
            # Si la connexion réussit, créer le menu normalement
            self.multi_menu = {
                'active': True,
                'buttons': {
                    'create': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 - 60, 300, 50),
                    'join': pygame.Rect(self.WINDOW_WIDTH//2 - 150, self.WINDOW_HEIGHT//2 + 10, 300, 50)
                },
                'hover': None,
                'room_code': '',
                'joining': False,
                'error_message': ''
            }
        
        # Changer l'écran actuel pour le menu multijoueur
        self.current_screen = "multi_menu"

    def draw_multiplayer_menu(self):
        # Fond sombre semi-transparent
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.fill(self.DARK_BG)
        overlay.set_alpha(230)
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        title_font = pygame.font.Font(None, 60)
        title = title_font.render("Mode Multijoueur", True, self.TEXT)
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//3))
        self.screen.blit(title, title_rect)
        
        # Boutons
        for btn_name, btn_rect in self.multi_menu['buttons'].items():
            color = (45, 45, 50) if self.multi_menu['hover'] == btn_name else (35, 35, 40)
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.ACCENT, btn_rect, 2, border_radius=10)
            
            text = "Créer une partie" if btn_name == "create" else "Rejoindre une partie"
            btn_text = pygame.font.Font(None, 30).render(text, True, self.TEXT)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            self.screen.blit(btn_text, text_rect)
        
        # Si on rejoint une partie, afficher le champ de saisie du code
        if self.multi_menu['joining']:
            code_font = pygame.font.Font(None, 40)
            code_text = code_font.render(f"Code: {self.multi_menu['room_code']}", True, self.TEXT)
            code_rect = code_text.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 100))
            self.screen.blit(code_text, code_rect)
            
            # Instructions
            instructions = pygame.font.Font(None, 30).render(
                "Entrez le code de la partie et appuyez sur Entrée", True, self.TEXT)
            instructions_rect = instructions.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 150))
            self.screen.blit(instructions, instructions_rect)
        
        # Afficher le message d'erreur s'il y en a un
        if self.multi_menu['error_message']:
            error_font = pygame.font.Font(None, 30)
            error_text = error_font.render(self.multi_menu['error_message'], True, (255, 50, 50))
            error_rect = error_text.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 200))
            self.screen.blit(error_text, error_rect)
        
        # Ajouter un bouton retour
        back_button = pygame.Rect(20, 20, 100, 40)
        pygame.draw.rect(self.screen, (35, 35, 40), back_button, border_radius=10)
        pygame.draw.rect(self.screen, self.ACCENT, back_button, 2, border_radius=10)
        back_text = pygame.font.Font(None, 30).render("Retour", True, self.TEXT)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
        
        # Ajouter le bouton à la liste des boutons du menu
        self.multi_menu['buttons']['back'] = back_button
        
        # Afficher le curseur personnalisé
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        pygame.display.flip()

    def draw_multiplayer_game(self):
        # Dessiner le fond et le canvas normalement
        self.draw_background()
        self.screen.blit(self.canvas_surface, (self.CANVAS_X, self.CANVAS_Y))
        self.draw_canvas_border()
        
        # Dessiner les outils et les contrôles
        self.draw_tool_buttons()
        self.draw_brush_size_slider()
        self.draw_undo_redo_buttons()
        
        # Afficher les informations de la partie
        info_font = pygame.font.Font(None, 30)
        
        # Afficher le code de la salle
        room_text = info_font.render(f"Salle: {self.room_code}", True, self.TEXT)
        self.screen.blit(room_text, (20, 20))
        
        # Afficher le tour actuel
        round_text = info_font.render(f"Tour: {self.game_state['round'] + 1}/3", True, self.TEXT)
        self.screen.blit(round_text, (20, 60))
        
        # Afficher le nombre de joueurs
        players_text = info_font.render(f"Joueurs: {len(self.game_state['players'])}", True, self.TEXT)
        self.screen.blit(players_text, (20, 100))
        
        # Si c'est notre tour de dessiner
        if self.game_state['current_drawer'] == self.player_id:
            word_text = info_font.render(f"Mot à dessiner: {self.game_state['current_word']}", True, self.TEXT)
            self.screen.blit(word_text, (self.WINDOW_WIDTH//2 - word_text.get_width()//2, 20))
            
            # Bouton pour terminer le tour
            end_turn_button = pygame.Rect(self.WINDOW_WIDTH - 150, 20, 130, 40)
            pygame.draw.rect(self.screen, (45, 45, 50), end_turn_button, border_radius=10)
            pygame.draw.rect(self.screen, self.ACCENT, end_turn_button, 2, border_radius=10)
            end_text = info_font.render("Terminer", True, self.TEXT)
            end_rect = end_text.get_rect(center=end_turn_button.center)
            self.screen.blit(end_text, end_rect)
            
            # Ajouter le bouton à la liste des boutons
            self.multi_menu['buttons']['end_turn'] = end_turn_button
        
        # Si c'est la phase de devinette
        elif self.game_state['current_phase'] == 'guessing':
            guess_text = info_font.render("Devinez le mot:", True, self.TEXT)
            self.screen.blit(guess_text, (self.WINDOW_WIDTH//2 - guess_text.get_width()//2, 20))
            
            # Champ de saisie pour la devinette
            guess_box = pygame.Rect(self.WINDOW_WIDTH//2 - 100, 60, 200, 40)
            pygame.draw.rect(self.screen, (35, 35, 40), guess_box, border_radius=10)
            pygame.draw.rect(self.screen, self.ACCENT, guess_box, 2, border_radius=10)
            
            # Afficher le texte saisi
            guess_input = info_font.render(self.guess_input, True, self.TEXT)
            self.screen.blit(guess_input, (guess_box.x + 10, guess_box.y + 5))
        
        # Afficher le curseur personnalisé
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        pygame.display.flip()

    def handle_multiplayer_game_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = event.pos
                
                # Vérifier le clic sur le bouton "Terminer"
                if 'end_turn' in self.multi_menu['buttons']:
                    if self.multi_menu['buttons']['end_turn'].collidepoint(mouse_pos):
                        self.network.end_turn()
                        return
                
                # Si c'est notre tour de dessiner, gérer le dessin normalement
                if self.game_state['current_drawer'] == self.player_id:
                    self.handle_event(event)
        
        elif event.type == pygame.KEYDOWN:
            # Si on est en phase de devinette
            if self.game_state['current_phase'] == 'guessing':
                if event.key == pygame.K_RETURN:
                    # Envoyer la devinette
                    if self.guess_input:
                        self.network.send_guess(self.guess_input)
                        self.guess_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.guess_input = self.guess_input[:-1]
                else:
                    # Ajouter le caractère à la devinette
                    if event.unicode.isprintable():
                        self.guess_input += event.unicode
        
        # Gérer le dessin normalement si c'est notre tour
        if self.game_state['current_drawer'] == self.player_id:
            self.handle_event(event)

    def start_multiplayer_game(self):
        try:
            if self.is_host:
                # Le host démarre la partie
                if not self.network.start_game():
                    self.multi_menu['error_message'] = "Erreur lors du démarrage de la partie"
                    return
            
            # Initialiser l'interface de jeu multijoueur
            self.current_screen = "drawing"
            self.game_state = {
                'current_player': 0,
                'round': 0,
                'word': None,
                'timer': 60,
                'waiting': False
            }
            
            # Réinitialiser le canvas
            self.canvas_surface.fill(self.WHITE)
            self.canvas_history = [self.canvas_surface.copy()]
            self.current_history_index = 0
            
            # Initialiser les variables pour la devinette
            self.guess_input = ""
            
            # Enregistrer les callbacks pour les événements réseau
            self.network.register_callback("on_draw_update", self.handle_draw_update)
            self.network.register_callback("on_turn_ended", self.handle_turn_ended)
            self.network.register_callback("on_game_ended", self.handle_game_ended)
            
        except Exception as e:
            print(f"Erreur lors du démarrage du jeu multijoueur : {e}")
            self.multi_menu['error_message'] = "Erreur lors du démarrage de la partie"

    def handle_draw_update(self, draw_data):
        # Mettre à jour le canvas avec les données de dessin reçues
        # À implémenter selon le format des données de dessin
        pass

    def handle_turn_ended(self, message):
        # Mettre à jour l'état du jeu
        self.game_state['current_phase'] = message['current_phase']
        self.game_state['current_drawer'] = message['current_drawer']
        self.game_state['current_word'] = message['current_word']
        
        # Si c'est notre tour de dessiner
        if self.game_state['current_drawer'] == self.player_id:
            # Réinitialiser le canvas
            self.canvas_surface.fill(self.WHITE)
            self.canvas_history = [self.canvas_surface.copy()]
            self.current_history_index = 0

    def handle_game_ended(self, scores):
        # Afficher l'écran de fin de partie
        self.current_screen = "game_end"
        self.game_scores = scores

    def draw_chrono_config(self):
        # Afficher l'image de fond
        self.screen.blit(self.menu_background, (0, 0))
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.fill(self.DARK_BG)
        overlay.set_alpha(100)
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        title_font = pygame.font.Font(None, 60)
        title = title_font.render("Configuration du Chronomètre", True, self.TEXT)
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        # Label pour la section temps
        label_font = pygame.font.Font(None, 40)
        time_label = label_font.render("Durée :", True, self.TEXT)
        time_label_rect = time_label.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 - 250))
        self.screen.blit(time_label, time_label_rect)
        
        # Texte du temps
        time_font = pygame.font.Font(None, 50)
        time_text = f"{self.chrono_config['time_value']} {self.chrono_config['time_unit']}"
        time_surface = time_font.render(time_text, True, self.TEXT)
        time_rect = time_surface.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 - 100))
        self.screen.blit(time_surface, time_rect)
        
        # Label pour la section type de contenu
        content_label = label_font.render("Type de contenu à dessiner :", True, self.TEXT)
        content_label_rect = content_label.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 50))
        self.screen.blit(content_label, content_label_rect)
        
        # Boutons
        for btn_name, btn_rect in self.chrono_config['buttons'].items():
            # Couleur du bouton selon le survol et l'état
            if self.chrono_config['hover'] == btn_name:
                button_color = (45, 45, 50)
            elif btn_name in ['word', 'phrase'] and btn_name == self.chrono_config['content_type']:
                button_color = (60, 60, 65)  # Couleur plus claire pour le bouton actif
            else:
                button_color = (35, 35, 40)
            
            # Dessiner le bouton
            pygame.draw.rect(self.screen, button_color, btn_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.ACCENT, btn_rect, 2, border_radius=10)
            
            # Texte ou symbole du bouton
            if btn_name == 'unit':
                text = "Minutes" if self.chrono_config['time_unit'] == 'seconds' else "Secondes"
            elif btn_name == 'plus':
                text = "+"
            elif btn_name == 'minus':
                text = "-"
            elif btn_name == 'start':
                text = "Démarrer"
            elif btn_name == 'back':
                text = "Retour"
            elif btn_name == 'word':
                text = "Mot"
            elif btn_name == 'phrase':
                text = "Phrase"
            
            # Police et taille selon le bouton
            if btn_name in ['plus', 'minus']:
                font = pygame.font.Font(None, 40)
            else:
                font = pygame.font.Font(None, 30)
            
            text_surface = font.render(text, True, self.TEXT)
            text_rect = text_surface.get_rect(center=btn_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Dessiner le curseur personnalisé
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        pygame.display.flip()

    def handle_chrono_config_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Mettre à jour l'état de survol des boutons
            mouse_pos = event.pos
            self.chrono_config['hover'] = None
            for btn_name, btn_rect in self.chrono_config['buttons'].items():
                if btn_rect.collidepoint(mouse_pos):
                    self.chrono_config['hover'] = btn_name
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = event.pos
                for btn_name, btn_rect in self.chrono_config['buttons'].items():
                    if btn_rect.collidepoint(mouse_pos):
                        if btn_name == 'back':
                            self.current_screen = "menu"
                            return
                        elif btn_name == 'unit':
                            # Changer l'unité de temps
                            if self.chrono_config['time_unit'] == 'seconds':
                                self.chrono_config['time_unit'] = 'minutes'
                                self.chrono_config['time_value'] = 1
                            else:
                                self.chrono_config['time_unit'] = 'seconds'
                                self.chrono_config['time_value'] = 60
                        elif btn_name == 'plus':
                            # Augmenter le temps
                            if self.chrono_config['time_unit'] == 'seconds':
                                self.chrono_config['time_value'] = min(3600, self.chrono_config['time_value'] + 30)
                            else:
                                self.chrono_config['time_value'] = min(60, self.chrono_config['time_value'] + 1)
                        elif btn_name == 'minus':
                            # Diminuer le temps
                            if self.chrono_config['time_unit'] == 'seconds':
                                self.chrono_config['time_value'] = max(30, self.chrono_config['time_value'] - 30)
                            else:
                                self.chrono_config['time_value'] = max(1, self.chrono_config['time_value'] - 1)
                        elif btn_name in ['word', 'phrase']:
                            # Changer le type de contenu
                            self.chrono_config['content_type'] = btn_name
                        elif btn_name == 'start':
                            # Démarrer le mode chronomètre
                            if self.chrono_config['content_type'] == 'word':
                                self.word_to_draw = self.get_random_word()
                            else:
                                self.word_to_draw = random.choice(self.phrases)
                            if self.chrono_config['time_unit'] == 'minutes':
                                self.timer = self.chrono_config['time_value'] * 60
                            else:
                                self.timer = self.chrono_config['time_value']
                            self.current_screen = "drawing"  # Changement direct de l'écran
                            return
                        break

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.current_screen == "preface":
                    self.handle_preface_event(event)
                elif self.current_screen == "menu":
                    self.handle_menu_event(event)
                elif self.current_screen == "chrono_config":
                    self.handle_chrono_config_event(event)
                elif self.current_screen == "multi_menu":
                    self.handle_multiplayer_menu_event(event)
                else:
                    self.handle_event(event)
            
            if self.current_screen == "preface":
                self.draw_preface()
            elif self.current_screen == "menu":
                self.draw_menu()
            elif self.current_screen == "chrono_config":
                self.draw_chrono_config()
            elif self.current_screen == "multi_menu":
                self.draw_multiplayer_menu()
            else:
                if self.game_mode == "chrono":
                    self.update_timer()
                self.draw()
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def update_brush_size(self, mouse_x):
        # Calculer la nouvelle taille du pinceau en fonction de la position de la souris
        relative_x = mouse_x - self.BRUSH_SLIDER_X
        percentage = max(0, min(1, relative_x / self.BRUSH_SLIDER_WIDTH))
        self.brush_size = int(self.MIN_BRUSH_SIZE + (self.MAX_BRUSH_SIZE - self.MIN_BRUSH_SIZE) * percentage)

    def start_transition(self, transition_type):
        self.transition['active'] = True
        self.transition['progress'] = 0
        self.transition['type'] = transition_type

    def draw_transition(self):
        if not self.transition['active']:
            return
        
        progress = self.transition['progress'] / self.transition['duration']
        
        if self.transition['type'] == 'out':
            alpha = int(255 * progress)
        else:  # transition in
            alpha = int(255 * (1 - progress))
        
        # Créer une surface pour l'effet de transition
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.fill(self.DARK_BG)
        overlay.set_alpha(alpha)
        
        # Ajouter des lignes néon qui se déplacent
        num_lines = 10
        for i in range(num_lines):
            pos = int(self.WINDOW_WIDTH * ((i + progress * 2) % 1))
            alpha_line = max(0, min(255, alpha))
            pygame.draw.line(overlay, (*self.NEON_BLUE[:3], alpha_line),
                            (pos, 0), (pos - 200, self.WINDOW_HEIGHT), 2)

        self.screen.blit(overlay, (0, 0))
        
        # Mettre à jour la progression
        self.transition['progress'] += 1
        if self.transition['progress'] >= self.transition['duration']:
            self.transition['active'] = False
            if self.transition['type'] == 'out':
                self.current_screen = 'drawing'
                self.start_transition('in')

    def is_mouse_over_brush_button(self, pos):
        return (self.BRUSH_BUTTON['rect'].collidepoint(pos) or
                self.ERASER_BUTTON['rect'].collidepoint(pos))

    def save_canvas_state(self):
        # Créer une copie du canvas actuel
        canvas_copy = self.canvas_surface.copy()
        
        # Si nous sommes au milieu de l'historique, supprimer les états futurs
        if self.current_history_index < len(self.canvas_history) - 1:
            self.canvas_history = self.canvas_history[:self.current_history_index + 1]
        
        # Ajouter le nouvel état
        self.canvas_history.append(canvas_copy)
        self.current_history_index += 1
        
        # Limiter la taille de l'historique
        if len(self.canvas_history) > self.MAX_HISTORY:
            self.canvas_history.pop(0)
            self.current_history_index -= 1

    def undo(self):
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self.canvas_surface = self.canvas_history[self.current_history_index].copy()

    def redo(self):
        if self.current_history_index < len(self.canvas_history) - 1:
            self.current_history_index += 1
            self.canvas_surface = self.canvas_history[self.current_history_index].copy()

    def draw_background(self):
        # Fond principal noir
        self.screen.fill(self.DARK_BG)
        
        # Effet de vignette subtil sur les coins
        vignette_size = 300
        surface = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Coins plus sombres
        for x, y in [(0, 0), (self.WINDOW_WIDTH, 0), 
                     (0, self.WINDOW_HEIGHT), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)]:
            for i in range(vignette_size):
                alpha = int(40 * (i/vignette_size))  # Transparence très subtile
                radius = vignette_size - i
                pygame.draw.circle(surface, (0, 0, 0, alpha), (x, y), radius)
        
        # Léger dégradé en haut
        gradient_height = 200
        for i in range(gradient_height):
            alpha = int(15 * (1 - i/gradient_height))  # Très subtil
            pygame.draw.line(surface, (255, 255, 255, alpha), 
                            (0, i), (self.WINDOW_WIDTH, i))
        
        self.screen.blit(surface, (0, 0))

    def draw_tool_buttons(self):
        # Dessiner le bouton pinceau
        pygame.draw.rect(self.screen, (35, 35, 40), self.BRUSH_BUTTON['rect'], border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER if not self.BRUSH_BUTTON['active'] else self.ACCENT,
                        self.BRUSH_BUTTON['rect'], 2, border_radius=5)
        
        # Centrer l'icône dans le bouton
        icon_x = self.BRUSH_BUTTON['rect'].centerx - self.brush_icon.get_width() // 2
        icon_y = self.BRUSH_BUTTON['rect'].centery - self.brush_icon.get_height() // 2
        self.screen.blit(self.brush_icon, (icon_x, icon_y))
        
        # Dessiner le bouton gomme
        pygame.draw.rect(self.screen, (35, 35, 40), self.ERASER_BUTTON['rect'], border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER if not self.ERASER_BUTTON['active'] else self.ACCENT,
                        self.ERASER_BUTTON['rect'], 2, border_radius=5)
        # Dessiner une icône de gomme simple
        eraser_rect = self.ERASER_BUTTON['rect'].inflate(-10, -10)
        pygame.draw.rect(self.screen, self.TEXT, eraser_rect, border_radius=3)
        
        # Dessiner le bouton pot de peinture
        pygame.draw.rect(self.screen, (35, 35, 40), self.PAINT_BUCKET_BUTTON['rect'], border_radius=5)
        
        # Ajouter un fond blanc légèrement plus petit que le bouton
        inner_rect = self.PAINT_BUCKET_BUTTON['rect'].inflate(-4, -4)
        pygame.draw.rect(self.screen, (255, 255, 255), inner_rect, border_radius=4)
        
        # Bordure du bouton
        pygame.draw.rect(self.screen, self.BORDER if not self.PAINT_BUCKET_BUTTON['active'] else self.ACCENT,
                        self.PAINT_BUCKET_BUTTON['rect'], 2, border_radius=5)
        
        # Centrer l'icône dans le bouton
        icon_x = self.PAINT_BUCKET_BUTTON['rect'].centerx - self.paint_bucket_icon.get_width() // 2
        icon_y = self.PAINT_BUCKET_BUTTON['rect'].centery - self.paint_bucket_icon.get_height() // 2
        self.screen.blit(self.paint_bucket_icon, (icon_x, icon_y))
        
        # Dessiner le bouton ligne droite
        pygame.draw.rect(self.screen, (35, 35, 40), self.LINE_BUTTON['rect'], border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER if not self.LINE_BUTTON['active'] else self.ACCENT,
                        self.LINE_BUTTON['rect'], 2, border_radius=5)
        
        # Dessiner l'icône de ligne droite
        line_rect = self.LINE_BUTTON['rect'].inflate(-10, -10)
        pygame.draw.line(self.screen, self.TEXT,
                        (line_rect.left, line_rect.centery),
                        (line_rect.right, line_rect.centery), 2)
        
        # Dessiner le bouton cercle
        pygame.draw.rect(self.screen, (35, 35, 40), self.CIRCLE_BUTTON['rect'], border_radius=5)
        pygame.draw.rect(self.screen, self.BORDER if not self.CIRCLE_BUTTON['active'] else self.ACCENT,
                        self.CIRCLE_BUTTON['rect'], 2, border_radius=5)
        
        # Dessiner l'icône de cercle
        circle_rect = self.CIRCLE_BUTTON['rect'].inflate(-10, -10)
        pygame.draw.circle(self.screen, self.TEXT,
                         circle_rect.center, min(circle_rect.width, circle_rect.height) // 2 - 2, 2)
        
        # Si on est en train de dessiner une ligne, afficher la prévisualisation
        if self.drawing_line and self.line_start and self.line_end:
            # Créer une surface temporaire pour la prévisualisation
            preview_surface = pygame.Surface((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), pygame.SRCALPHA)
            # Dessiner la ligne avec une transparence
            pygame.draw.line(preview_surface, (*self.current_color[:3], 128),
                           self.line_start, self.line_end, self.brush_size)
            self.screen.blit(preview_surface, (self.CANVAS_X, self.CANVAS_Y))

        # Si on est en train de dessiner un cercle, afficher la prévisualisation
        if self.drawing_circle and self.circle_start and self.circle_end:
            # Créer une surface temporaire pour la prévisualisation
            preview_surface = pygame.Surface((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), pygame.SRCALPHA)
            center_x = (self.circle_start[0] + self.circle_end[0]) // 2
            center_y = (self.circle_start[1] + self.circle_end[1]) // 2
            radius = int(sqrt((self.circle_end[0] - self.circle_start[0])**2 + 
                            (self.circle_end[1] - self.circle_start[1])**2) / 2)
            # Dessiner le cercle avec une transparence
            pygame.draw.circle(preview_surface, (*self.current_color[:3], 128),
                             (center_x, center_y), radius, self.brush_size)
            self.screen.blit(preview_surface, (self.CANVAS_X, self.CANVAS_Y))

    def get_arrow_points(self, rect, is_undo):
        """Calcule les points pour dessiner une flèche"""
        x, y = rect.centerx, rect.centery
        width = rect.width * 0.4
        height = rect.height * 0.3
        
        if is_undo:
            # Flèche vers la gauche
            points = [
                (x + width/2, y - height/2),  # Haut droit
                (x - width/2, y),             # Pointe gauche
                (x + width/2, y + height/2)   # Bas droit
            ]
        else:
            # Flèche vers la droite
            points = [
                (x - width/2, y - height/2),  # Haut gauche
                (x + width/2, y),             # Pointe droite
                (x - width/2, y + height/2)   # Bas gauche
            ]
        
        return points

    def flood_fill(self, x, y):
        # Obtenir la couleur du pixel de départ
        target_color = self.canvas_surface.get_at((x, y))
        replacement_color = self.current_color
        
        # Si la couleur est la même, pas besoin de remplir
        if target_color == replacement_color:
            return
        
        # Créer une surface temporaire pour le remplissage
        temp_surface = pygame.Surface((self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        temp_surface.blit(self.canvas_surface, (0, 0))
        
        # Remplir la zone
        pygame.draw.rect(temp_surface, replacement_color, (0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT))
        
        # Copier le résultat sur le canvas
        self.canvas_surface.blit(temp_surface, (0, 0))
        
        # Sauvegarder l'état après le remplissage
        self.save_canvas_state()

    def load_words(self):
        try:
            with open('data/words.txt', 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return ["chat", "chien", "maison"]  # Mots par défaut si le fichier n'existe pas

    def get_random_word(self):
        return random.choice(self.words)

    def update_timer(self):
        if self.game_mode == "chrono" and self.timer > 0:
            self.timer -= 1/60  # Diminuer d'une seconde (en supposant 60 FPS)
            if self.timer <= 0:
                self.timer = 0
                self.chrono_end_effect['active'] = True
                self.chrono_end_effect['progress'] = 0

    def save_drawing(self):
        try:
            # Ouvrir la boîte de dialogue de sauvegarde
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ],
                title="Sauvegarder le dessin"
            )
            
            # Si un nom de fichier a été choisi (l'utilisateur n'a pas annulé)
            if filename:
                # Sauvegarder le canvas
                pygame.image.save(self.canvas_surface, filename)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def draw_preface(self):
        self.screen.fill(self.DARK_BG)
        
        # Animation du texte
        current_text = self.preface_text[self.preface_stage]
        text_font = pygame.font.Font(None, 50)
        
        # Effet de fade in/out
        if self.preface_timer < 30:  # Fade in
            self.preface_alpha = min(255, self.preface_alpha + 8)
        elif self.preface_timer > 90:  # Fade out
            self.preface_alpha = max(0, self.preface_alpha - 8)
        
        # Rendu du texte avec transparence
        text_surface = text_font.render(current_text, True, self.TEXT)
        text_surface.set_alpha(self.preface_alpha)
        text_rect = text_surface.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        
        # Afficher le texte
        self.screen.blit(text_surface, text_rect)
        
        # Mise à jour du timer
        self.preface_timer += 1
        if self.preface_timer >= 120:  # Changer de texte toutes les 2 secondes
            self.preface_timer = 0
            self.preface_alpha = 0
            self.preface_stage += 1
            if self.preface_stage >= len(self.preface_text):
                self.current_screen = "menu"
        
        # Dessiner le curseur personnalisé
        self.draw_custom_cursor(pygame.mouse.get_pos())
        
        pygame.display.flip()

    def handle_preface_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                self.current_screen = "menu"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.current_screen = "menu"

    def handle_multiplayer_menu_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Gérer le survol des boutons
            mouse_pos = event.pos
            self.multi_menu['hover'] = None
            for btn_name, btn_rect in self.multi_menu['buttons'].items():
                if btn_rect.collidepoint(mouse_pos):
                    self.multi_menu['hover'] = btn_name
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = event.pos
                for btn_name, btn_rect in self.multi_menu['buttons'].items():
                    if btn_rect.collidepoint(mouse_pos):
                        if btn_name == "back":
                            self.current_screen = "menu"
                            return
                        elif btn_name == "create":
                            # Créer une nouvelle partie
                            if not self.network or not self.network.connected:
                                self.multi_menu['error_message'] = "Serveur non disponible"
                                return
                            
                            try:
                                response = self.network.send({"type": "create_room"})
                                if not response:
                                    self.multi_menu['error_message'] = "Pas de réponse du serveur"
                                    return
                                    
                                if "room_code" in response:
                                    self.room_code = response["room_code"]
                                    if self.room_code:  # Vérifier que le code n'est pas None
                                        self.is_host = True
                                        self.multi_menu['room_code'] = self.room_code
                                        self.multi_menu['error_message'] = f"Code de la salle : {self.room_code}"
                                    else:
                                        self.multi_menu['error_message'] = "Erreur lors de la création de la salle"
                                else:
                                    self.multi_menu['error_message'] = "Réponse invalide du serveur"
                            except Exception as e:
                                print(f"Erreur lors de la création de la partie : {e}")
                                self.multi_menu['error_message'] = "Erreur de connexion"
                        elif btn_name == "join":
                            self.multi_menu['joining'] = True
                        break
        
        elif event.type == pygame.KEYDOWN and self.multi_menu['joining']:
            if event.key == pygame.K_RETURN:
                # Tenter de rejoindre la partie
                try:
                    response = self.network.send({
                        "type": "join_room",
                        "room_code": self.multi_menu['room_code']
                    })
                    if response.get("success"):
                        self.room_code = self.multi_menu['room_code']
                        self.is_host = False
                        self.start_multiplayer_game()
                    else:
                        self.multi_menu['error_message'] = "Code de partie invalide"
                except Exception as e:
                    self.multi_menu['error_message'] = f"Erreur : {str(e)}"
            elif event.key == pygame.K_BACKSPACE:
                self.multi_menu['room_code'] = self.multi_menu['room_code'][:-1]
            else:
                # Ajouter les caractères au code
                if len(self.multi_menu['room_code']) < 6:  # Limite de 6 caractères
                    if event.unicode.isalnum():  # Seulement les caractères alphanumériques
                        self.multi_menu['room_code'] += event.unicode.upper()

    def load_phrases(self):
        try:
            with open('data/phrases.txt', 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return ["Un chat qui joue avec une pelote de laine", "Un chien qui court après sa queue", "Une maison dans les arbres"]  # Phrases par défaut

    def draw_chrono_end_effect(self):
        # Augmenter la progression
        self.chrono_end_effect['progress'] += 1
        progress = self.chrono_end_effect['progress'] / self.chrono_end_effect['duration']
        
        # Créer une surface pour l'effet
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Flash rouge qui pulse
        flash_alpha = int(abs(math.sin(progress * math.pi * 4)) * 128)
        overlay.fill((255, 0, 0, flash_alpha))
        
        # Texte "TEMPS ÉCOULÉ!"
        font_size = int(80 * (1 + math.sin(progress * math.pi * 2) * 0.2))  # Effet de pulsation
        font = pygame.font.Font(None, font_size)
        text = font.render("TEMPS ÉCOULÉ !", True, self.WHITE)
        
        # Faire tourner le texte légèrement
        rotation = math.sin(progress * math.pi * 3) * 5  # Oscillation de ±5 degrés
        rotated_text = pygame.transform.rotate(text, rotation)
        
        # Centrer le texte
        text_rect = rotated_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        
        # Ajouter une ombre au texte
        shadow_offset = 4
        shadow_text = font.render("TEMPS ÉCOULÉ !", True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        
        # Dessiner des cercles concentriques qui s'étendent
        num_circles = 3
        for i in range(num_circles):
            circle_progress = (progress + i/num_circles) % 1
            radius = circle_progress * max(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            circle_alpha = int((1 - circle_progress) * 128)
            circle_surface = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*self.NEON_PINK[:3], circle_alpha),
                             (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2), radius, 4)
            overlay.blit(circle_surface, (0, 0))
        
        # Dessiner l'ombre et le texte
        overlay.blit(shadow_text, shadow_rect)
        overlay.blit(rotated_text, text_rect)
        
        # Ajouter des particules qui volent vers l'extérieur
        num_particles = 20
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * math.pi
            distance = progress * max(self.WINDOW_WIDTH, self.WINDOW_HEIGHT) / 2
            x = self.WINDOW_WIDTH//2 + math.cos(angle) * distance
            y = self.WINDOW_HEIGHT//2 + math.sin(angle) * distance
            particle_size = int(10 * (1 - progress))
            particle_alpha = int(255 * (1 - progress))
            particle_color = (*self.NEON_BLUE[:3], particle_alpha)
            pygame.draw.circle(overlay, particle_color, (int(x), int(y)), particle_size)
        
        # Afficher l'overlay
        self.screen.blit(overlay, (0, 0))
        
        # Désactiver l'effet une fois terminé
        if self.chrono_end_effect['progress'] >= self.chrono_end_effect['duration']:
            self.chrono_end_effect['active'] = False
            self.current_screen = "menu"  # Retourner au menu

if __name__ == '__main__':
    game = GarticPhone()
    game.run()

