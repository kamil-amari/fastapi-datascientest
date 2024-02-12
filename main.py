from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Annotated, Optional
from base64 import b64decode
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

class Questionnaire(BaseModel):
    question: Optional[str] = None
    qestion_num: Optional[int] = 5
    subject: list
    use: str
    correct: Optional[str] = None
    responseA : Optional[str] = None
    responseB : Optional[str] = None
    responseC : Optional[str] = None
    responseD : Optional[str] = None

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
            detail="Mot de passe incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not users[username] == password:
        raise HTTPException(
            status_code=401,
            detail="Identifiant incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@api.get('/', name='Home')
async def get_index():
    return {'message': 'API powered by FastAPI'}

@api.get('/questionnaire')
async def create_qcm(qcm: Questionnaire, authorization: Annotated[str | None, Header()] = None):
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
        question_num = qcm.qestion_num
        use = qcm.use
        subject = qcm.subject
        print(data['use'])
        questions = [value for key, value in data.items() if use in data['use'] and data['subject'] in subject]
        # random_questions = rd.sample(questions, question_num)

        return questions
