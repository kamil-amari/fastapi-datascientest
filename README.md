# Introduction

Cette application a été créée dans le cadre d'une formation avec Datascientest. Elle utilise le framework Python FastAPI pour exposer des points de terminaison pour des requêtes HTTP.

# Fonctionnement

`main.py` contient une API permettant de créer des questionnaires à partir d'une liste de questions. La liste de questions se trouve dans le fichier `questions.csv`.

Pour lancer l'API, entrez dans le terminal :
```bash
uvicorn --reload --port PORT main:api
```
où PORT est le numéro de port exposé (8000 par défaut).

## Authentification
Pour accéder aux fonctionnalités, il faut s'authentifier lors de la requête avec un en-tête de la forme `Authorization: Basic username:password.`

Les utilisateurs déjà renseignés sont :
- `alice:wonderland`
- `bob:builder`
- `clementine:mandarine`

Les administrateurs peuvent ajouter des questions à la liste déjà existante en se connectant avec `admin:4dm1n.`

## Endpoints
L'API pour la création de questionnaires est accessible à l'adresse :
- `http://127.0.0.1:8000` ou `http://127.0.0.1:PORT` (si vous avez précisé un port différent).

## /create-questionnaire (GET)
### Description
Pour la création de questionnaires.

### Requête
```bash
curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic username:password' \
-d '{
    "qestion_num": x,
    "subject": ["Sub1", "Sub2"],
    "use": "Use"
}'
```
### Paramètres
- `question_num` : Nombre de questions que le questionnaire va contenir.
- `subject` : Liste de catégories (peut être une simple chaîne de caractère).
- `use` : Type de test.

### Exemple
```bash
curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic alice:wonderland' \
-d '{
    "qestion_num": 5,
    "subject": ["BDD", "Systèmes distribués"],
    "use": "Test de positionnement"
}'
```

## /add-question (PUT)
### Description
Pour ajouter des questions à la liste existante (réservé aux administrateurs).

### Requête
```bash
curl -X 'PUT' 'http://127.0.0.1:8000/add-question' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic admin:4dm1n' \
-d '{
    "question": "Question",
    "subject": "Sub",
    "use": "Use",
    "correct": "X",
    "responseX": "La réponse X",
    "remark": "Une remarque"
}'
```

### Paramètres
- `question` : La question à poser.
- `subject` : La catégorie de la question.
- `use` : Le type de test pour lequel cette question peut être posée.
- `correct` : La lettre de la bonne réponse.
- `responseX` : Ensemble des réponses parmi lesquelles on peut choisir (chacune de ces informations peut être laissée vide).
- `remark` : Une remarque sur la question.

### Exemple
```bash
curl -X 'PUT' 'http://127.0.0.1:8000/add-question' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H 'Authorization: Basic admin:4dm1n' \
-d '{
    "question": "Comment je m'appelle ?",
    "subject": "BDD",
    "use": "Test de positionnement",
    "correct": "A",
    "responseA": "La réponse A",
    "responseB": "La réponse B",
    "responseC": "La réponse C"
}'
```
