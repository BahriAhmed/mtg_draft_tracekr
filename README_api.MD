# API de gestion des utilisateurs

## Vue d’ensemble

Ce projet est une API de gestion des utilisateurs développée avec FastAPI. Elle fournit des fonctionnalités d’authentification, d’autorisation et de gestion complète des utilisateurs à l’aide d’un système de contrôle d’accès basé sur les rôles (RBAC).

Le système prend en charge deux rôles :
- player : accès limité à son propre compte
- admin : accès complet à tous les utilisateurs

---

## Technologies utilisées

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- JWT (JSON Web Token)
- bcrypt / SHA256 (hachage des mots de passe)
- pytest (tests)

---

## Architecture

L’application suit une architecture en couches :
- Routes : gestion des requêtes HTTP
- Services : logique métier
- Modèles : structure de la base de données
- Couche base de données : gestion de la persistance avec SQLAlchemy

Cette séparation améliore la maintenabilité et la scalabilité du projet.

---

## Authentification

### Connexion

POST /login

Requête :
{
  "username": "string",
  "password": "string"
}

Réponse :
{
  "message": "Login successful",
  "access_token": "jwt_token",
  "token_type": "bearer"
}

---

### Utilisation du token

Toutes les routes protégées nécessitent un token dans l’en-tête de la requête :

Authorization: Bearer <token>

---

## Endpoints de l’API

### Création d’un utilisateur
POST /register  
Crée un nouveau compte utilisateur.

---

### Connexion
POST /login  
Authentifie un utilisateur et retourne un token JWT.

---

### Récupérer l’utilisateur connecté
GET /me  
Retourne les informations de l’utilisateur authentifié.

---

### Récupérer tous les utilisateurs (admin uniquement)
GET /users  
Retourne la liste de tous les utilisateurs. Accès réservé à l’administrateur.

---

### Récupérer un utilisateur par ID (admin uniquement)
GET /user/{user_id}  
Retourne les informations d’un utilisateur spécifique. Accès réservé à l’administrateur.

---

### Changer le mot de passe
PUT /change-password  
Permet à un utilisateur de modifier son mot de passe.

Règles :
- player : uniquement son propre compte
- admin : n’importe quel compte

---

### Changer le nom d’utilisateur
PUT /change-username  
Permet de modifier le nom d’utilisateur.

Règles :
- player : uniquement son propre compte
- admin : n’importe quel compte

---

### Supprimer un utilisateur
DELETE /user/{user_id}  
Supprime un compte utilisateur.

Règles :
- player : uniquement son propre compte
- admin : n’importe quel compte

---

## Accès à la base de données

Les opérations sur la base de données sont gérées avec SQLAlchemy :
- session.add() : création
- session.query() : lecture
- session.commit() : sauvegarde
- session.delete() : suppression

Toute la logique d’accès aux données est centralisée dans la couche services.

---

## Validation

Toutes les requêtes entrantes sont validées avec Pydantic afin de garantir :
- la validité des types de données
- la présence des champs obligatoires
- l’intégrité des données avant insertion en base

---

## Autorisation (RBAC)

Rôles :
- player : accès limité à ses propres données
- admin : accès complet à tous les utilisateurs

Permissions :

| Action | Player | Admin |
|--------|--------|--------|
| Création de compte | Oui | Oui |
| Connexion | Oui | Oui |
| Lecture des données personnelles | Oui | Oui |
| Lecture de tous les utilisateurs | Non | Oui |
| Modification du compte personnel | Oui | Oui |
| Modification d’autres utilisateurs | Non | Oui |
| Suppression du compte personnel | Oui | Oui |
| Suppression d’autres utilisateurs | Non | Oui |

---

## Tests

Les tests sont écrits avec pytest et couvrent :
- l’authentification
- les règles d’autorisation
- les opérations CRUD
- les interactions avec la base de données
- la gestion des erreurs

Exécution des tests :
pytest

---

## Documentation de l’API

FastAPI fournit automatiquement une documentation interactive :
- /docs (Swagger UI)
- /redoc (ReDoc)

---

## Conclusion

Cette API fournit un système sécurisé et structuré de gestion des utilisateurs utilisant l’authentification JWT et une autorisation basée sur les rôles. Elle est conçue avec une architecture claire séparant les routes, les services et la logique de base de données afin d’assurer la maintenabilité et la scalabilité du projet.