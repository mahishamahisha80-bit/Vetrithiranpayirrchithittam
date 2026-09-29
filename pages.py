from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..auth import current_user

router=APIRouter()
templates=Jinja2Templates(directory="app/templates")

def page(request, template, **context):
    return templates.TemplateResponse(template,{"request":request,"user":current_user(request),**context})

@router.get("/")
def index(request: Request): return page(request,"index.html")
@router.get("/login")
def login_page(request: Request): return page(request,"login.html")
@router.get("/register")
def register_page(request: Request): return page(request,"register.html")
@router.get("/dashboard")
def dashboard(request: Request):
    if not current_user(request): return RedirectResponse("/login",303)
    return page(request,"dashboard.html")
@router.get("/planner/home")
def home_page(request: Request):
    if not current_user(request): return RedirectResponse("/login",303)
    return page(request,"home.html")
@router.get("/planner/party")
def party_page(request: Request):
    if not current_user(request): return RedirectResponse("/login",303)
    return page(request,"party.html")
@router.get("/planner/jewelry")
def jewelry_page(request: Request):
    if not current_user(request): return RedirectResponse("/login",303)
    return page(request,"jewelry.html")
@router.get("/history")
def history_page(request: Request):
    if not current_user(request): return RedirectResponse("/login",303)
    return page(request,"history.html")

@router.get("/testimonials")
def testimonials(request: Request): return page(request,"testimonials.html")
