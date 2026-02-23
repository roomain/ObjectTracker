"""Configuration de l'application de suivi d'objet."""

# Configuration des servomoteurs
SERVO_CONFIG = {
    'port': 'COM3',  # Port série (à adapter selon votre configuration)
    'baudrate': 9600,
    'pan_pin': 3,     # Pin pour le servomoteur horizontal (pan)
    'tilt_pin': 5,    # Pin pour le servomoteur vertical (tilt)
    'min_angle': 0,
    'max_angle': 180,
}

# Configuration de la caméra
CAMERA_CONFIG = {
    'camera_id': 0,  # ID de la caméra (0 = caméra par défaut)
    'width': 640,
    'height': 480,
    'fps': 30,
}

# Configuration du suivi
TRACKING_CONFIG = {
    'detection_method': 'hsv',  # 'color', 'hsv', 'contour'
    'min_area': 500,  # Surface minimale pour détecter un objet
    'smooth_factor': 0.7,  # Facteur de lissage pour éviter les mouvements saccadés
}

# Configuration de couleur pour le suivi HSV (Hue, Saturation, Value)
# Exemple pour tracker du rouge
HSV_LOWER = (0, 100, 100)
HSV_UPPER = (10, 255, 255)

# Configuration BBC Micro:bit (si utilisé)
MICROBIT_CONFIG = {
    'enabled': False,
    'port': 'COM3',
}

# Points de calibrage de la caméra
CAMERA_CENTER = (CAMERA_CONFIG['width'] / 2, CAMERA_CONFIG['height'] / 2)

# Limites de mouvement des servos
PAN_MIN, PAN_MAX = 30, 150
TILT_MIN, TILT_MAX = 60, 150
