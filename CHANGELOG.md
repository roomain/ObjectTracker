# CHANGELOG

## Version 1.1.0 - Contrôle Manuel + Interface Améliorée

### ✨ Nouvelles fonctionnalités

- **Mode Manuel** (M): Contrôle complet des servomoteurs au clavier
  - Touches WASD pour déplacer la caméra
  - Touches +/- pour ajuster la vitesse
  - Flèches directionnelles supportées

- **Interface améliorée**:
  - Affichage retour caméra en temps réel
  - Barre d'info avec mode actuel (SUIVI/MANUEL)
  - Affichage des angles Pan/Tilt
  - Affichage de la vitesse en mode manuel
  - Aide visuelle en bas de l'écran

### 🎮 Contrôles clavier

**Mode Suivi Auto:**
- ESPACE = Pause/Reprise
- C = Calibrer
- R = Réinitialiser
- M = Basculer en mode Manuel

**Mode Manuel:**
- W/Haut = Monter caméra
- S/Bas = Descendre caméra
- A/Gauche = Tourner à gauche
- D/Droite = Tourner à droite
- +/- = Ajuster vitesse (1-20°)
- M = Revenir au mode Suivi

**Général:**
- Q = Quitter

### 🔧 Améliorations techniques

- Meilleure gestion des états (suivi/manuel/pause)
- Interface visuelle plus professionnelle
- Messages d'aide sur l'écran

### 📝 Notes

- Mode manuel utile pour tester les servos
- Vitesse ajustable pour précision ou rapidité
- Passage fluide entre modes auto et manuel

---

## Version 1.0.0 - Version initiale

- Application de suivi d'objet basée sur HSV
- Contrôle de servomoteurs via port série
- Interface basique avec OpenCV
- Configuration centralisée
