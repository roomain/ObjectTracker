"""Contrôleur pour les servomoteurs."""

import serial
import time
from typing import Optional
import config


class ServoController:
    """Contrôle des servomoteurs via port série."""
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600):
        """
        Initialiser le contrôleur de servomoteurs.
        
        Args:
            port: Port série (ex: 'COM3'), utilise la config si None
            baudrate: Vitesse de transmission
        """
        self.port = port or config.SERVO_CONFIG['port']
        self.baudrate = baudrate
        self.serial_conn: Optional[serial.Serial] = None
        self.pan_angle = 90
        self.tilt_angle = 90
        self.connected = False
        
    def connect(self) -> bool:
        """Établir la connexion avec le port série."""
        try:
            self.serial_conn = serial.Serial(
                self.port,
                self.baudrate,
                timeout=1
            )
            self.connected = True
            print(f"✓ Connecté au port {self.port}")
            time.sleep(2)  # Attendre que la connexion s'établisse
            return True
        except serial.SerialException as e:
            print(f"✗ Erreur de connexion: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Fermer la connexion série."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            self.connected = False
            print("✓ Déconnecté du port série")
    
    def set_angle(self, servo_num: int, angle: float) -> bool:
        """
        Définir l'angle d'un servomoteur.
        
        Args:
            servo_num: Numéro du servomoteur (1=pan, 2=tilt)
            angle: Angle en degrés (0-180)
            
        Returns:
            True si succès, False sinon
        """
        if not self.connected or not self.serial_conn:
            print("✗ Non connecté au port série")
            return False
        
        # Limiter l'angle
        angle = max(config.SERVO_CONFIG['min_angle'], 
                   min(angle, config.SERVO_CONFIG['max_angle']))
        
        try:
            # Format: #<servo><angle> (ex: #1090)
            command = f"#{servo_num}{int(angle)}\n"
            self.serial_conn.write(command.encode())
            
            if servo_num == 1:
                self.pan_angle = angle
            elif servo_num == 2:
                self.tilt_angle = angle
            
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'envoi de la commande: {e}")
            return False
    
    def pan(self, angle: float) -> bool:
        """Contrôler le mouvement horizontal (pan)."""
        angle = max(config.PAN_MIN, min(angle, config.PAN_MAX))
        return self.set_angle(1, angle)
    
    def tilt(self, angle: float) -> bool:
        """Contrôler le mouvement vertical (tilt)."""
        angle = max(config.TILT_MIN, min(angle, config.TILT_MAX))
        return self.set_angle(2, angle)
    
    def center(self):
        """Repositionner les servos au centre."""
        self.pan(90)
        self.tilt(90)
    
    def test_servos(self):
        """Tester les servomoteurs en effectuant des mouvements."""
        if not self.connected:
            print("✗ Non connecté")
            return
        
        print("Test des servomoteurs...")
        
        # Test pan
        for angle in [90, 120, 60, 90]:
            self.pan(angle)
            time.sleep(0.5)
        
        # Test tilt
        for angle in [90, 120, 60, 90]:
            self.tilt(angle)
            time.sleep(0.5)
        
        print("✓ Test terminé")
    
    def smooth_move(self, pan_angle: float, tilt_angle: float, steps: int = 10):
        """
        Mouvement en douceur vers les angles cibles.
        
        Args:
            pan_angle: Angle pan cible
            tilt_angle: Angle tilt cible
            steps: Nombre d'étapes pour le mouvement
        """
        pan_start = self.pan_angle
        tilt_start = self.tilt_angle
        
        for i in range(steps + 1):
            ratio = i / steps
            current_pan = pan_start + (pan_angle - pan_start) * ratio
            current_tilt = tilt_start + (tilt_angle - tilt_start) * ratio
            
            self.pan(current_pan)
            self.tilt(current_tilt)
            time.sleep(0.05)
