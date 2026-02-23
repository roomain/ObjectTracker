"""Application principale de suivi d'objet."""

import cv2
import numpy as np
import time
from servo_controller import ServoController
from object_tracker import ObjectTracker
import config


class ObjectTrackingApp:
    """Application complète de suivi d'objet avec contrôle de servomoteurs."""
    
    def __init__(self):
        """Initialiser l'application."""
        self.servo = ServoController()
        self.tracker = ObjectTracker()
        self.camera = None
        self.running = False
        self.paused = False
        
        # Configuration de la détection
        self.detection_color_type = 'hsv'  # 'hsv', 'color'
        
    def setup_camera(self) -> bool:
        """Initialiser la caméra."""
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_CONFIG['camera_id'])
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_CONFIG['width'])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_CONFIG['height'])
            self.camera.set(cv2.CAP_PROP_FPS, config.CAMERA_CONFIG['fps'])
            
            if not self.camera.isOpened():
                print("✗ Impossible d'ouvrir la caméra")
                return False
            
            print("✓ Caméra initialisée")
            return True
        except Exception as e:
            print(f"✗ Erreur caméra: {e}")
            return False
    
    def release_camera(self):
        """Libérer la caméra."""
        if self.camera:
            self.camera.release()
            print("✓ Caméra fermée")
    
    def draw_interface(self, frame: np.ndarray, info: dict) -> np.ndarray:
        """
        Ajouter l'interface visuelle sur l'image.
        
        Args:
            frame: Image de la caméra
            info: Dictionnaire avec les informations à afficher
            
        Returns:
            Image modifiée
        """
        height, width = frame.shape[:2]
        
        # Ajouter une barre d'information en haut
        cv2.rectangle(frame, (0, 0), (width, 100), (0, 0, 0), -1)
        
        # Dessiner la croix du centre
        cv2.line(frame, (width//2 - 30, height//2), (width//2 + 30, height//2), (255, 0, 0), 2)
        cv2.line(frame, (width//2, height//2 - 30), (width//2, height//2 + 30), (255, 0, 0), 2)
        cv2.circle(frame, (width//2, height//2), 50, (0, 255, 200), 2)
        
        # Déterminer la couleur et le mode
        manual_mode = info.get('manual_mode', False)
        mode_color = (0, 0, 255) if manual_mode else (0, 255, 0)  # Rouge si manual, vert si auto
        mode_text = "🎮 MANUEL" if manual_mode else "🤖 SUIVI"
        
        # Afficher le mode
        cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, mode_color, 2)
        
        # Afficher le statut
        if not manual_mode:
            status_color = (0, 255, 0) if info.get('object_found') else (0, 0, 255)
            status_text = "OBJET DÉTECTÉ ✓" if info['object_found'] else "En recherche..."
            cv2.putText(frame, status_text, (width - 350, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                       status_color, 2)
        
        # Afficher les angles des servos
        pan_text = f"Pan:  {info['pan_angle']:.0f}°"
        tilt_text = f"Tilt: {info['tilt_angle']:.0f}°"
        cv2.putText(frame, pan_text, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, tilt_text, (200, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Afficher la vitesse en mode manuel
        if manual_mode:
            speed = info.get('manual_speed', 5)
            cv2.putText(frame, f"Vitesse: {speed}", (width - 200, 65), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1)
        
        # Position de l'objet (si trouvé)
        if info['object_found'] and info['object_location']:
            x, y = info['object_location']
            cv2.putText(frame, f"Pos: ({x}, {y})", (width - 200, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        # Barre d'aide en bas
        help_text = "M=Mode | ↑↓←→=Déplacer | +/-=Vitesse | SPACE=Pause | Q=Quitter"
        cv2.putText(frame, help_text, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, 
                   (100, 100, 100), 1)
        
        return frame
    
    def run(self):
        """Exécuter la boucle principale."""
        print("\n" + "="*50)
        print("APPLICATION DE SUIVI D'OBJET")
        print("="*50)
        
        # Initialiser la caméra
        if not self.setup_camera():
            return
        
        # Initialiser les servomoteurs
        print("\nConnexion aux servomoteurs...")
        if not self.servo.connect():
            print("⚠ Continuant sans servomoteurs...")
            self.servo.connected = False
        else:
            self.servo.center()
        
        self.running = True
        smooth_factor = config.TRACKING_CONFIG['smooth_factor']
        last_pan = 90
        last_tilt = 90
        manual_mode = False
        manual_speed = 5
        
        print("\n" + "="*60)
        print("INTERFACE DE SUIVI D'OBJET - Retour caméra activé")
        print("="*60)
        print("\n📹 MODES:")
        print("   🤖 SUIVI AUTO (défaut) - Suit l'objet automatiquement")
        print("   🎮 MANUEL - Contrôle manuel complet des servos")
        print("\n⌨️  CONTRÔLES SUIVI AUTO:")
        print("   ESPACE  = Pause/Reprise du suivi")
        print("   C       = Calibrer (centrer les servos)")
        print("   R       = Réinitialiser (position par défaut)")
        print("\n⌨️  CONTRÔLES MANUEL:")
        print("   M       = Basculer Mode Manuel ↔ Mode Suivi")
        print("   W/↑     = Monter la caméra")
        print("   S/↓     = Descendre la caméra")
        print("   A/←     = Tourner caméra à gauche")
        print("   D/→     = Tourner caméra à droite")
        print("   +       = Augmenter la vitesse de déplacement")
        print("   -       = Réduire la vitesse de déplacement")
        print("\n🔴 GÉNÉRAL:")
        print("   Q       = Quitter l'application")
        print("="*60 + "\n")
        
        try:
            while self.running:
                ret, frame = self.camera.read()
                
                if not ret:
                    print("✗ Erreur de lecture de la caméra")
                    break
                
                # Redimensionner si nécessaire
                frame = cv2.resize(frame, (config.CAMERA_CONFIG['width'], 
                                          config.CAMERA_CONFIG['height']))
                
                # Tracker l'objet (si pas en mode manuel)
                if not self.paused and not manual_mode:
                    frame, center = self.tracker.track_by_color_range(
                        frame,
                        config.HSV_LOWER,
                        config.HSV_UPPER
                    )
                    
                    # Si objet trouvé, contrôler les servos
                    if center and self.servo.connected:
                        error_x, error_y = self.tracker.calculate_error(
                            center,
                            (config.CAMERA_CONFIG['width'], config.CAMERA_CONFIG['height'])
                        )
                        
                        target_pan, target_tilt = self.tracker.convert_error_to_angle(
                            error_x, error_y,
                            self.servo.pan_angle,
                            self.servo.tilt_angle
                        )
                        
                        # Lissage du mouvement
                        smooth_pan = last_pan + (target_pan - last_pan) * smooth_factor
                        smooth_tilt = last_tilt + (target_tilt - last_tilt) * smooth_factor
                        
                        # Appliquer les mouvements
                        self.servo.pan(smooth_pan)
                        self.servo.tilt(smooth_tilt)
                        
                        last_pan = smooth_pan
                        last_tilt = smooth_tilt
                
                # Préparer les informations pour l'affichage
                info = {
                    'object_found': self.tracker.object_found,
                    'object_location': self.tracker.object_location,
                    'pan_angle': self.servo.pan_angle if self.servo.connected else 0,
                    'tilt_angle': self.servo.tilt_angle if self.servo.connected else 0,
                    'manual_mode': manual_mode,
                    'manual_speed': manual_speed,
                }
                
                # Ajouter l'interface
                frame = self.draw_interface(frame, info)
                
                # Afficher l'image
                cv2.imshow('ObjectTracker - Camera Feed', frame)
                
                # Gestion des touches
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n✓ Quitter...")
                    self.running = False
                elif key == ord(' '):
                    self.paused = not self.paused
                    print(f"{'⏸ En pause' if self.paused else '▶ Reprise'}")
                elif key == ord('c'):
                    print("✓ Calibrage: caméra centrée")
                    if self.servo.connected:
                        self.servo.center()
                elif key == ord('r'):
                    print("✓ Réinitialisation des servos")
                    if self.servo.connected:
                        self.servo.center()
                elif key == ord('m'):
                    manual_mode = not manual_mode
                    print(f"{'🎮 Mode MANUEL activé' if manual_mode else '🤖 Mode SUIVI activé'}")
                elif key == ord('+') or key == ord('='):
                    manual_speed = min(20, manual_speed + 1)
                    print(f"Vitesse: {manual_speed}")
                elif key == ord('-') or key == ord('_'):
                    manual_speed = max(1, manual_speed - 1)
                    print(f"Vitesse: {manual_speed}")
                # Contrôles manuels: WASD + Flèches
                elif key == ord('w') or key == ord('W') or key == 82:  # Haut
                    if self.servo.connected and manual_mode:
                        self.servo.tilt(self.servo.tilt_angle - manual_speed)
                elif key == ord('s') or key == ord('S') or key == 84:  # Bas
                    if self.servo.connected and manual_mode:
                        self.servo.tilt(self.servo.tilt_angle + manual_speed)
                elif key == ord('a') or key == ord('A') or key == 81:  # Gauche
                    if self.servo.connected and manual_mode:
                        self.servo.pan(self.servo.pan_angle - manual_speed)
                elif key == ord('d') or key == ord('D') or key == 83:  # Droite
                    if self.servo.connected and manual_mode:
                        self.servo.pan(self.servo.pan_angle + manual_speed)
                
        except KeyboardInterrupt:
            print("\n✓ Interruption clavier")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Nettoyer et fermer les ressources."""
        print("\nNettoyage...")
        self.running = False
        
        if self.servo.connected:
            self.servo.center()
            self.servo.disconnect()
        
        self.release_camera()
        cv2.destroyAllWindows()
        
        print("✓ Application fermée")


def print_menu():
    """Afficher le menu de configuration."""
    print("\n" + "="*50)
    print("CONFIGURATION INITIALE")
    print("="*50)
    print("\n1. Tracker par couleur HSV (défaut)")
    print("2. Tracker par détection de peau")
    print("3. Configuration personnalisée")
    print("4. Lancer l'application")
    print("\nQuelle option? ", end="")


def main():
    """Point d'entrée principale."""
    app = ObjectTrackingApp()
    
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == '1':
            app.detection_color_type = 'hsv'
            print("✓ Mode HSV sélectionné")
            
        elif choice == '2':
            print("✓ Mode détection de peau (visage) sélectionné")
            # Les gammes de peau seront utilisées
            
        elif choice == '3':
            print("\nConfiguration personnalisée")
            print(f"Port série actuel: {config.SERVO_CONFIG['port']}")
            port = input("Nouveau port (ENTRÉE pour garder): ").strip()
            if port:
                config.SERVO_CONFIG['port'] = port
            print("✓ Configuration mise à jour")
            
        elif choice == '4':
            break
        else:
            print("✗ Option invalide")
    
    app.run()


if __name__ == '__main__':
    main()
