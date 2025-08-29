# 📅 Système de Gestion d'Événements

## 📋 Table des matières
1. [Aperçu](#aperçu)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Structure du Projet](#structure-du-projet)
5. [Base de Données](#base-de-données)
6. [API Routes](#api-routes)
7. [Fonctionnalités](#fonctionnalités)
8. [Déploiement](#déploiement)

## 🎯 Aperçu
Application web de gestion d'événements permettant de gérer des événements, des participants et des organisateurs. Développée avec Flask et PostgreSQL.

## 💻 Technologies
- **Backend**: Python 3.11+ avec Flask
- **Base de données**: PostgreSQL 14+
- **Frontend**: 
  - HTML5
  - TailwindCSS
  - JavaScript
- **Templates**: Jinja2

## ⚙️ Installation

### Prérequis
- Python 3.11 ou supérieur
- PostgreSQL 14 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

```bash
# 1. Cloner le repository
git clone <repository-url>
cd event_management_system_main

# 2. Créer un environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la base de données
psql -U postgres
CREATE DATABASE event_management;
```

### Configuration
Créer un fichier `.env` à la racine du projet :
```env
DB_NAME=event_management
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
FLASK_SECRET_KEY=votre_clé_secrète
```

## 📁 Structure du Projet
```
event_management_system_main/
├── templates/
│   ├── base.html
│   ├── events.html
│   ├── view_event.html
│   ├── create_event.html
│   ├── edit_event.html
│   ├── organizers.html
│   ├── create_organizer.html
│   ├── edit_organizer.html
│   ├── attendees.html
│   ├── create_attendee.html
│   ├── view_attendee.html
│   ├── register_event.html
│   ├── unregister_event.html
│   └── index.html
│   ├── attendees.html
│   └── stats.html
├── database/seed/
│   |       ├── index.sql
│   └── index.py
├── index.py
├── requirements.txt
└── README.md
```

## 🗄️ Base de Données

### Schéma
```sql
-- Table des organisateurs
CREATE TABLE organizers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Table des événements
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT,
    organizer_id INTEGER REFERENCES organizers(id)
);

-- Table des participants
CREATE TABLE attendees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Table des inscriptions
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    attendee_id INTEGER REFERENCES attendees(id) ON DELETE CASCADE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, attendee_id)
);
```

## 🛣️ API Routes

### Événements
```python
@app.route("/events")                                  # Liste des événements
@app.route("/events/<int:event_id>")                  # Détails d'un événement
@app.route("/create_event", methods=["GET", "POST"])  # Créer un événement
@app.route("/events/update/<int:event_id>")          # Modifier un événement
@app.route("/events/delete/<int:event_id>")          # Supprimer un événement
```

### Participants
```python
@app.route("/attendees")                              # Liste des participants
@app.route("/create_attendee")                        # Créer un participant
@app.route("/attendees/<int:attendee_id>")           # Détails d'un participant
@app.route("/register_event/<int:event_id>")         # Inscrire à un événement
@app.route("/unregister_event/<int:event_id>/<int:attendee_id>") # Désinscrire
```

### Organisateurs
```python
@app.route("/organizers")                             # Liste des organisateurs
@app.route("/create_organizer")                       # Créer un organisateur
@app.route("/organizers/update/<int:organizer_id>")  # Modifier un organisateur
@app.route("/organizers/delete/<int:organizer_id>")  # Supprimer un organisateur
```

## ✨ Fonctionnalités

### Gestion des Événements
- Création, modification et suppression d'événements
- Vue détaillée des événements
- Liste des participants inscrits
- Statistiques des événements

### Gestion des Participants
- Inscription/désinscription aux événements
- Profils détaillés des participants
- Historique des participations

### Gestion des Organisateurs
- Création et gestion des profils organisateurs
- Suivi des événements par organisateur
- Tableau de bord des statistiques


# Installation production
pip install -r requirements.txt



## 📞 Support

Pour toute question ou assistance :
- 📧 Email : anasserghini00@gmail.com
- 📚 Documentation : `ReadMe.MD`

---
© 2025 Event Management System. Tous droits réservés ANAS SERGHINI.