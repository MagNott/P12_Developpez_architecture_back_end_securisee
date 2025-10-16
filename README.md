# Secure Back-End Architecture for CRM Management


## Description

This project is a secure, modular command-line application.  
It allows a company to manage its collaborators, customers, contracts, and events while enforcing strict permissions based on user roles.

The application uses a PostgreSQL database, SQLAlchemy for ORM, and JWT for user authentication.  
It follows best practices in code architecture and access control, providing a clear separation of concerns and reusable utilities.

## Features

Liste des fonctionnalités principales du projet.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MagNott/P12_Developpez_architecture_back_end_securisee

2. Create a virtual environment and activate it:
Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```


## Usage

To start the application, run the following command:

```bash
python main.py
```

Once launched, you will see a menu with the following options:

- Sign in: Log in with your credentials to access features based on your department.
- Sign up: Register a new collaborator account (requires department ID).
- Log out: Exit the current session securely.

After signing in, the app will display a department-specific menu:

Management:
- Create and modify contracts
- Manage collaborators (create, update, delete)
- Assign support staff to events

Support:
- View and update your assigned events

Sales:
- Create and modify customers and contracts
- Create an event for a signed customer

You can navigate through the menu using the keyboard, and each command will guide you through the required inputs.

## Configuration

Détails sur la configuration (comme la connexion à la base de données, variables d’environnement).

## Authentication and Permissions

Explication rapide de la gestion des utilisateurs, sécurité, et permissions.

## Logging

Présentation de l’intégration avec Sentry ou autres outils de journalisation.

## Author

This project was developed by Magnott in October 2025 as part of the Python Application Developer program at OpenClassrooms.
