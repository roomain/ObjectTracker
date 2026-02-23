# ObjectTracker - Application de Suivi d'Objet avec Servomoteurs

Application Python pour tracker un objet désigné en temps réel et contrôler l'orientation d'une caméra via servomoteurs.

## Caractéristiques

- **Suivi d'objet en temps réel** via détection de couleur HSV
- **Contrôle de servomoteurs** (pan/tilt) pour l'orientation de la caméra
- **Interface graphique** avec visualisation en temps réel
- **Lissage des mouvements** pour une cinématique fluide
- **Calibrage et configuration** faciles

## Matériel Requis

- Caméra USB ou intégrée
- 2 servomoteurs (MG90S, SG90 ou similaires)
- Contrôleur de servomoteurs supportant la communication série (Arduino, Raspberry Pi, etc.)
- Câble série USB (CH340, FT232, etc.)

## Installation

### 1. Cloner et installer les dépendances

```bash
cd D:\ProjetsGIT\ObjectTracker
pip install -r requirements.txt
```

### 2. Configuration matérielle

#### Configuration Arduino/Contrôleur:

**Programme Arduino minimal:**

```cpp
#include <Servo.h>

Servo panServo;
Servo tiltServo;

void setup() {
  Serial.begin(9600);
  panServo.attach(3);
  tiltServo.attach(5);
  panServo.write(90);
  tiltServo.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command.startsWith("#1")) {
      int angle = command.substring(2).toInt();
      panServo.write(angle);
    }
    else if (command.startsWith("#2")) {
      int angle = command.substring(2).toInt();
      tiltServo.write(angle);
    }
  }
}
```

### 3. Configuration du port série

Modifier `config.py`:

```python
SERVO_CONFIG = {
    'port': 'COM3',  # Vérifier le bon port (Gestionnaire des appareils)
    'baudrate': 9600,
    ...
}
```

### 4. Vérifier le port de caméra

Si vous avez plusieurs caméras, modifier dans `config.py`:

```python
CAMERA_CONFIG = {
    'camera_id': 0,  # Changer si nécessaire
    ...
}
```

## Utilisation

### Lancer l'application:

```bash
python main.py
```

### Menu de configuration:

1. **Tracker par couleur HSV** (par défaut - pour objets colorés)
2. **Tracker par détection de peau** (pour visages/mains)
3. **Configuration personnalisée** (paramètres avancés)
4. **Lancer l'application**

### Commandes clavier:

| Touche | Action |
|--------|--------|
| **ESPACE** | Mettre en pause / Reprendre |
| **C** | Calibrer (centrer les servos) |
| **R** | Réinitialiser les servosmoteurs |
| **Q** | Quitter l'application |

## Calibrage des couleurs

Pour tracker un objet d'une couleur spécifique:

### Méthode 1: Script de calibrage HSV (à ajouter)

```python
python calibrate_hsv.py
```

### Méthode 2: Modification manuelle

Modifier `config.py`:

```python
# Exemple pour tracker du bleu
HSV_LOWER = (100, 100, 100)
HSV_UPPER = (130, 255, 255)
```

**Valeurs HSV courantes:**
- Rouge: (0, 100, 100) - (10, 255, 255)
- Vert: (50, 100, 100) - (70, 255, 255)
- Bleu: (100, 100, 100) - (130, 255, 255)
- Jaune: (20, 100, 100) - (40, 255, 255)

## Structure du projet

```
ObjectTracker/
├── main.py                 # Application principale
├── config.py              # Configuration centralisée
├── servo_controller.py     # Contrôle des servomoteurs
├── object_tracker.py       # Logique de suivi d'objet
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
```

## Dépannage

### "✗ Erreur de connexion: Port non trouvé"

- Vérifier que le câble série est connecté
- Vérifier le bon port dans Windows (Gestionnaire des appareils > Ports COM)
- Installer les pilotes CH340 ou FT232 si nécessaire

### Servomoteurs ne bougent pas

- Vérifier l'alimentation du contrôleur
- Vérifier le programme Arduino est chargé
- Tester avec le moniteur série d'Arduino IDE

### La caméra n'est pas détectée

- Vérifier que la caméra est bien connectée
- Tester avec une autre application (OBS, etc.)
- Essayer `camera_id: 1` ou `2` dans config.py

### Objet non détecté

- Utiliser le script de calibrage HSV
- Améliorer l'éclairage de la scène
- Augmenter `TRACKING_CONFIG['min_area']` pour les petits objets

## Extensions possibles

- [ ] Sauvegarde des paramètres de configuration
- [ ] Interface GUI avec sliders pour HSV
- [ ] Support de multiples objets
- [ ] Enregistrement vidéo
- [ ] Détection par contour
- [ ] Mode suivi de mouvement prédictif
- [ ] Support de CNN (YOLOv8, etc.)

## Licence

MIT

## Auteur

Généré automatiquement
