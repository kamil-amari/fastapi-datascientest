from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Annotated, Optional, Union
import pandas as pd
import numpy as np
import random as rd

api = FastAPI()

data = pd.read_csv('questions.csv').replace(np.nan, None)
data_dict = data.to_dict()

users = {
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}

class QCM(BaseModel):
    question: Optional[str] = None
    number: Optional[int] = None
    subject: Union[list, str]
    use: str
    correct: Optional[str] = None
    responseA : Optional[str] = None
    responseB : Optional[str] = None
    responseC : Optional[str] = None
    responseD : Optional[str] = None
    remark: Optional[str] = None

def authenticate_user(auth_header):
    auth_scheme, auth_token = auth_header.split()

    if auth_scheme.lower() != 'basic':
        raise HTTPException(
            status_code=401,
            detail="Schéma d'authentification non pris en charge",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # auth_token_decoded = b64decode(auth_token).decode()
    username, password = auth_token.split(':')
    if not users.get(username):
        raise HTTPException(
            status_code=401,
            detail="Identifiant incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not users[username] == password:
        raise HTTPException(
            status_code=401,
            detail="Mot de passe incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

def authenticate_admin(auth_header):
    auth_scheme, auth_token = auth_header.split()

    if auth_scheme.lower() != 'basic':
        raise HTTPException(
            status_code=401,
            detail="Schéma d'authentification non pris en charge",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # auth_token_decoded = b64decode(auth_token).decode()
    username, password = auth_token.split(':')
    if not username == "admin":
        raise HTTPException(
            status_code=401,
            detail="Identifiant incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not password == "4dm1n":
        raise HTTPException(
            status_code=401,
            detail="Mot d epasse incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@api.get('/', name='Home')
async def get_index():
    return {'message': 'API powered by FastAPI'}

@api.get('/create-questionnaire', responses={200: {"description": "Questionniare created successfully"}, 401: {"description": "Incorrect username or password"}})
async def create_questionnaire(qcm: QCM, authorization: Annotated[str | None, Header()] = None):
    """
    Route pour créer un questionnaire sachant les éléments suivants:
    use, subject, nombre de questions
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if authenticate_user(authorization):
        number = qcm.question
        use = qcm.use
        subject = qcm.subject
        indices = [key for key, value in data_dict['use'].items() if value == use and data_dict['subject'][key] in subject]
        random_indices = rd.sample(indices, number)
        questions = {}
        for i, j in enumerate(random_indices, 1):
            question = {key: data_dict[key][j] for key in data_dict if key not in ["correct", "remark", "use", "subject"]}
            questions[i] = question
        return questions

@api.put('/add-question', responses={200: {"description": "Questionniare created successfully"}, 401: {"description": "Incorrect username or password"}, 501: {"descriptions": "Error while adding question"}})
async def put_question(qcm: QCM, authorization: Annotated[str | None, Header()] = None):
    """
    Route pour ajouter une question au questionnaire sachant les éléments suivants:
    question, use, subject, correct, responseA, responseB, responseC, responseD
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    expected_keys = ['question', 'use', 'number', 'subject', 'correct', 'responseA', 'responseB', 'responseC', 'responseD', 'remark']
    for key in qcm.model_dump():
        if key not in expected_keys:
            raise HTTPException(
                status_code=501,
                detail="Unexpected entry",
            )
        
    if authenticate_admin(authorization):
        question = qcm.question
        use = qcm.use
        subject = qcm.subject
        correct = qcm.correct
        responseA = qcm.responseA
        responseB = qcm.responseB
        responseC = qcm.responseC
        responseD = qcm.responseD
        remark = qcm.remark

        number = len(data_dict['question'])
        data_dict['question'][number] = question
        data_dict['use'][number] = use
        data_dict['subject'][number] = subject
        data_dict['correct'][number] = correct
        data_dict['responseA'][number] = responseA
        data_dict['responseB'][number] = responseB
        data_dict['responseC'][number] = responseC
        data_dict['responseD'][number] = responseD
        data_dict['remark'][number] = remark

    data = pd.DataFrame(data_dict)
    data.to_csv('questions.csv', index=False)

    return "Question added successfully"
