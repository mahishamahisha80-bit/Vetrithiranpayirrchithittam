from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from ..auth import create_access_token, hash_password, verify_password, current_user
from ..database import get_db

router=APIRouter(tags=["auth"])

@router.post("/register")
def register(name: str=Form(...), email: str=Form(...), password: str=Form(...)):
    email=email.strip().lower()
    with get_db() as db:
        if db.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
            return JSONResponse({"detail":"Email is already registered"},status_code=409)
        cur=db.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",(name.strip(),email,hash_password(password)))
        user_id=cur.lastrowid
    response=RedirectResponse("/dashboard",status_code=303)
    response.set_cookie("access_token",create_access_token(user_id),httponly=True,samesite="lax",secure=False,max_age=86400)
    return response

@router.post("/login")
def login(email: str=Form(...), password: str=Form(...)):
    with get_db() as db: row=db.execute("SELECT id,password_hash FROM users WHERE email=?",(email.strip().lower(),)).fetchone()
    if not row or not verify_password(password,row["password_hash"]):
        return JSONResponse({"detail":"Invalid email or password"},status_code=401)
    response=RedirectResponse("/dashboard",status_code=303)
    response.set_cookie("access_token",create_access_token(row["id"]),httponly=True,samesite="lax",secure=False,max_age=86400)
    return response

@router.get("/logout")
def logout():
    response=RedirectResponse("/",status_code=303); response.delete_cookie("access_token"); return response

@router.post("/token")
def token(email: str=Form(...), password: str=Form(...)):
    with get_db() as db: row=db.execute("SELECT id,password_hash FROM users WHERE email=?",(email.strip().lower(),)).fetchone()
    if not row or not verify_password(password,row["password_hash"]): return JSONResponse({"detail":"Invalid credentials"},status_code=401)
    return {"access_token":create_access_token(row["id"]),"token_type":"bearer"}
