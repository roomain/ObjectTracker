"""Module de suivi d'objets."""

import cv2
import numpy as np
from typing import Tuple, Optional
import config


class ObjectTracker:
    """Suivi d'objets basé sur les couleurs et contours."""
    
    def __init__(self):
        """Initialiser le tracker d'objets."""
        self.object_location: Optional[Tuple[int, int]] = None
        self.object_found = False
        
    def track_by_color_range(self, frame: np.ndarray, 
                            lower_hsv: Tuple, 
                            upper_hsv: Tuple) -> Tuple[np.ndarray, Optional[Tuple[int, int]]]:
        """
        Tracker un objet par gamme de couleur HSV.
        
        Args:
            frame: Image de la caméra
            lower_hsv: Limite inférieure HSV (H, S, V)
            upper_hsv: Limite supérieure HSV (H, S, V)
            
        Returns:
            Tuple: (image traitée, position du centre de l'objet ou None)
        """
        # Convertir BGR vers HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Créer un masque pour les couleurs dans la gamme
        mask = cv2.inRange(hsv, np.array(lower_hsv), np.array(upper_hsv))
        
        # Appliquer des opérations morphologiques pour nettoyer le masque
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        center = None
        if contours:
            # Trouver le plus grand contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            if area > config.TRACKING_CONFIG['min_area']:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    center = (cx, cy)
                    
                    # Dessiner le contour et le centre
                    cv2.drawContours(frame, [largest_contour], 0, (0, 255, 0), 2)
                    cv2.circle(frame, center, 5, (0, 255, 0), -1)
                    cv2.circle(frame, center, 50, (0, 255, 0), 1)
                    
                    self.object_location = center
                    self.object_found = True
        
        if not center:
            self.object_found = False
        
        return frame, center
    
    def track_by_skin_detection(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[Tuple[int, int]]]:
        """
        Tracker le visage ou la peau (détection par couleur de peau).
        
        Args:
            frame: Image de la caméra
            
        Returns:
            Tuple: (image traitée, position du centre ou None)
        """
        # Gamme de couleur pour la détection de peau
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        return self.track_by_color_range(frame, tuple(lower_skin), tuple(upper_skin))
    
    def calculate_error(self, object_center: Tuple[int, int], 
                       frame_size: Tuple[int, int]) -> Tuple[float, float]:
        """
        Calculer l'erreur entre le centre de l'objet et le centre de la caméra.
        
        Args:
            object_center: Position (x, y) de l'objet
            frame_size: Taille de l'image (width, height)
            
        Returns:
            Tuple: (erreur_x en pixels, erreur_y en pixels)
        """
        center_x = frame_size[0] / 2
        center_y = frame_size[1] / 2
        
        error_x = object_center[0] - center_x
        error_y = object_center[1] - center_y
        
        return error_x, error_y
    
    def convert_error_to_angle(self, error_x: float, error_y: float, 
                              current_pan: float, current_tilt: float) -> Tuple[float, float]:
        """
        Convertir l'erreur en pixels en commandes d'angle.
        
        Args:
            error_x: Erreur en pixels (axe X)
            error_y: Erreur en pixels (axe Y)
            current_pan: Angle pan actuel
            current_tilt: Angle tilt actuel
            
        Returns:
            Tuple: (angle_pan cible, angle_tilt cible)
        """
        # Facteur de conversion: pixels vers degrés
        pixel_to_degree_x = 180 / config.CAMERA_CONFIG['width']
        pixel_to_degree_y = 180 / config.CAMERA_CONFIG['height']
        
        pan = current_pan + (error_x * pixel_to_degree_x * 0.1)
        tilt = current_tilt - (error_y * pixel_to_degree_y * 0.1)  # Y inversé
        
        return pan, tilt
    
    def get_status(self) -> dict:
        """Obtenir le statut du tracker."""
        return {
            'object_found': self.object_found,
            'object_location': self.object_location,
        }
