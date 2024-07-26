# Introduction

Cette application a été créée dans le cadre d'une formation avec Datascientest. Elle utilise le framework python FastAPI pour exposer des points de terminaison pour des requêtes HTTP.

# Fonctionnement

main.py contient une API permettant de créer des questionnaires à partir d'une liste de questions. La liste de questions se trouve dans le fichier questions.csv
Pour lancer L'API, entrer dans le terminal : `uvicorn --reload --port PORT main:api`, avec PORT le numéro de port exposé (8000 par défaut)
Pour accéder à ses fonctionnalités, il faut s'authentifier avec un en-tête de la forme `Authorization: Basic username:password` lors de la requête
(les utilisateurs déjà renseignés sont alice:wonderland, bob:builder, clementine:mandarine)

Les administrateurs peuvent aussi ajouter des questions à la liste dejà existante (en se connectant avec admin:4dm1n).

L'API pour la création de questionnaire est accessible à l'adresse : http://127.0.0.1:8000 ou http://127.0.0.1:PORT (si vous avez précisé un port différent).
** Elle a deux endpoint : *
- /create-questionnaire (méthode GET) : 
        pour la création de questionnaire
        cet endpoint est accessible avec les données suivantes:
        curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic username:password' -d '{"qestion_num": x, "subject": ["Sub1", "Sub2"], "use": "Use"}'
        question_num correspond au nombre de question que le questionnaire va contenir
        subject est une liste de catégories (peut être une simple chaîne de caractère)
        use est le type de test

- /add-question (méthode PUT)
        cet endpoint est accessible avec les données suivantes:
        curl -X 'PUT' 'http://127.0.0.1:8000/add-question' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic admin:4dm1n' -d '{"question": "Question", "subject": "Sub", "use": "Use", "correct": "X", "responseX": "La réponse X", remark: "Une remarque"}'
        question correspond à la question à poser
        subject est la catégorie de la question
        use est le type de test pour lequel cette question peut être posée
        correct est la lettre de la bonne réponse
        responseX (avec X dans A, B, C, D) est l'ensemble des réponses parmi lesquelles on peut choisir (chacune de ces informations peut être laissée vide)
        remark est une remarque sur la question

** Exemples de requêtes : *
- curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic alice:wonderland' -d '{"qestion_num": 5, "subject": ["BDD", "Systèmes distribués"], "use": "Test de positionnement"}'
- curl -X 'PUT' 'http://127.0.0.1:8000/add-question' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic admin:4dm1n' -d '{"qestion": "Comment je m appelle ?", "subject": "BDD", "use": "Test de positionnement", "correct": "A", "responseA": "La réponse A", "responseB": "La réponse B", "responseC": "La réponse C"}'
