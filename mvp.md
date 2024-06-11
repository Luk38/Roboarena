# Minimum Viable Product für Roboarena
### Spielkonzept:
- Spieler steuern einen Roboter Charakter.
- Kollisionen mit Objekten und anderen Robotern möglich.
- Gegnerische Roboter können abgeschossen werden.
- Mehrere Maps und verschiedene Gegnertypen
- Menü zum Starten und Beenden des Spiels.

### Technische Umsetzung:
- Bibliothek: Pygame https://www.pygame.org/
- Programmiersprache: Python
- Grafik: 2D-Grafik in Vogelperspektive
- Physik: Einfache Kollisionserkennung mit Pygame

## Features:
### Spielercharakter:
- Einfaches Robotermodell mit grundlegender Steuerung (WASD, Maus zum Zielen und Schießen)
- Lebensanzeige 
- Munitionsanzeige
- Möglichkeit zum Sammeln von Power-Ups oder Upgrades (z. B. zusätzliche Munition, erhöhte Geschwindigkeit)

### Gegner:
- Verschiedene Robotertypen mit unterschiedlichen Verhaltensweisen (z. B. patrouillieren, schießen, auf den Spieler zulaufen)
- Einfache Gegnerbewegungen und Angriffe
- Schadensystem für Treffer und Tod

### Umgebung:
- Mehrere Maps mit unterschiedlichen Layouts und Hindernissen (z. B. Wände, Kisten)
- Grafik Tiles für die Objekte
- Interaktive Objekte (z. B. Power-Ups)
- Einfache Soundeffekte und Musik

### Menü:
- Hauptmenü mit Optionen zum Starten eines neuen Spiels und Beenden des Spiels
- Einstellungsmenü zum Anpassen von Audiolautstärke

### Erweiterungen für die Zukunft / stretch goals:
- Mehrspielermodus
- Verschiedene Spielmodi (z. B. Deathmatch, Capture the Flag)
- Level-Editor zum Erstellen eigener Maps
- Speicherbarer Spielstand
- Verbesserte Grafik und Soundeffekte
- Einstellungen zum Anpassen von Grafik und Steuerung

### Ressourcen:
- Pygame Dokumentation: https://www.pygame.org/docs/
- Python Tutorial: https://docs.python.org/3/tutorial/