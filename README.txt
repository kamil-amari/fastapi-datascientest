main.py contient une API permettant de créer des questionnaires à partir d'une liste de questions.
Pour accéder à cette fonctionnalité, il faut s'authentifier avec un en-tête de la forme Authorization: Basic username:password
(les comptes déjà créés sont alice:wonderland, bob:builder, clementine:mandarine)

Les administrateurs peuvent aussi ajouter des questions à la liste dejà existante (en se connectant avec admin:4dm1n)

L'API pour la création de questionnaire est accessible à l'adresse : http://127.0.0.1:8000
Elle a deux endpoint:
    /create-questionnaire (méthode GET)
        pour la création de questionnaire
        cet endpoint est accessible avec les données suivantes:
        curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic username:password' -d '{"qestion_num": x, "subject": ["Sub1", "Sub2"], "use": "Use"}'
        question_num correspond au nombre de question que le questionnaire va contenir
        subject est une liste de catégories (peut être une simple chaîne de caractère)
        use est le type de test
    
    /add-question (méthode PUT)
        cet endpoint est accessible avec les données suivantes:
        curl -X 'PUT' 'http://127.0.0.1:8000/add-question' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic admin:4dm1n' -d '{"question": "Question", "subject": "Sub", "use": "Use", "correct": "X", "responseX": "La réponse X", remark: "Une remarque"}'
        question correspond à la question à poser
        subject est la catégorie de la question
        use est le type de test pour lequel cette question peut être posée
        correct est la lettre de la bonne réponse
        responseX (avec X dans A, B, C, D) est l'ensemble des réponses parmis lesquelles on peut choisir (chacune de ces informations peut être laissée vide)
        remark est une remarque sur la question

Exemples de requêtes:
curl -X 'GET' 'http://127.0.0.1:8000/create-questionnaire' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic alice:wonderland' -d '{"qestion_num": 5, "subject": ["BDD", "Systèmes distribués"], "use": "Test de positionnement"}'
curl -X 'PUT' 'http://127.0.0.1:8000/add-question' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Basic admin:4dm1n' -d '{"qestion": "Comment je m appelle ?", "subject": "BDD", "use": "Test de positionnement", "correct": "A", "responseA": "La réponse A", "responseB": "La réponse B", "responseC": "La réponse C"}'