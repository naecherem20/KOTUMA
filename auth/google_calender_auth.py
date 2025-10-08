import os
import requests
from fastapi import APIRouter, Request,HTTPException,Depends
from dotenv import load_dotenv
from sqlmodel import Session
from core.lawyer_conf import get_current_lawyer
from models.lawyer_models import Lawyer
from database.connection import get_session
import secrets
from uuid import UUID


load_dotenv()
router = APIRouter(tags=["google_calendar"])
REDIRECT_URI=os.getenv("REDIRECT_URI")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

@router.get("/auth/google")
async def auth_google(current_lawyer:Lawyer = Depends(get_current_lawyer)):
    # Next: exchange this code for tokens
    # lawyer_id=db.query(Lawyer).filter(lawyer.id)
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=https://www.googleapis.com/auth/calendar.readonly"
        "&access_type=offline"
        "&prompt=consent"
        f"&state={str(current_lawyer.id)}"
    )
    
    return{"auth_url":auth_url}


@router.get("/auth/callback")
async def google_callback(request:Request, db:Session=Depends(get_session)):
    
    code = request.query_params.get("code")
    lawyer_id = request.query_params.get("state")

    
    if not code or not lawyer_id:
        return {"message": "Callback endpoint hit without code or state "}

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/auth/callback",
        "grant_type": "authorization_code",
    }

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    tokens = response.json()
    print("Google token response:", tokens)

    if "access_token" not in tokens:
        return {"error": "Token exchange failed", "details": tokens}

    lawyer = db.query(Lawyer).filter(Lawyer.id == lawyer_id).first()
    if not lawyer:
        return {"error": "Lawyer not found"}

    lawyer.google_access_token = tokens["access_token"]
    lawyer.google_refresh_token = tokens.get("refresh_token")
    db.commit()
    db.refresh(lawyer)

    return {"message": "Authentication successful", "tokens": tokens}

    