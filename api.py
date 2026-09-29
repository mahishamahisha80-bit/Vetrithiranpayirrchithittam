import json
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from ..auth import current_user
from ..database import get_db
from ..models import HomeRequest, PartyRequest, JewelryRequest
from ..services.recommendations import generate_home, generate_party, generate_jewelry

router = APIRouter(prefix="/api", tags=["recommendations"])

def require_user(request: Request):
    user=current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Login required")
    return user

def save_history(user_id, planner, request_data, response_data):
    with get_db() as db:
        db.execute("INSERT INTO recommendations(user_id, planner, request_json, response_json) VALUES(?,?,?,?)",
                   (user_id, planner, json.dumps(request_data, default=str), json.dumps(response_data, default=str)))

@router.post("/generate-home")
def home(data: HomeRequest, request: Request, user=Depends(require_user)):
    result=generate_home(data); save_history(user["id"],"home",data.model_dump(),result); return result

@router.post("/generate-party")
def party(data: PartyRequest, request: Request, user=Depends(require_user)):
    result=generate_party(data); save_history(user["id"],"party",data.model_dump(),result); return result

@router.post("/generate-jewelry")
async def jewelry(request: Request, budget: float, occasion: str, style: str="elegant", metal: str="any", outfit_description: str="", outfit_image: UploadFile|None=File(default=None), user=Depends(require_user)):
    data=JewelryRequest(budget=budget, occasion=occasion, style=style, metal=metal, outfit_description=outfit_description)
    image_bytes=None; mime=None
    if outfit_image:
        allowed={"image/jpeg","image/png","image/webp"}
        if outfit_image.content_type not in allowed: raise HTTPException(400,"Only JPEG, PNG, or WebP images are allowed")
        raw=await outfit_image.read()
        if len(raw)>5*1024*1024: raise HTTPException(400,"Image exceeds 5 MB")
        image_bytes=raw; mime=outfit_image.content_type
    result=generate_jewelry(data,image_bytes,mime); save_history(user["id"],"jewelry",data.model_dump(),result); return result

@router.get("/history")
def history(request: Request, user=Depends(require_user)):
    with get_db() as db:
        rows=db.execute("SELECT id, planner, request_json, response_json, created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 50",(user["id"],)).fetchall()
    return [{"id":r["id"],"planner":r["planner"],"request":json.loads(r["request_json"]),"response":json.loads(r["response_json"]),"created_at":r["created_at"]} for r in rows]

@router.get("/session-info")
def session_info(request: Request, user=Depends(require_user)):
    return {"logged_in":True,"user_id":user["id"],"name":user["name"],"email":user["email"]}

@router.get("/session-data")
def session_data(request: Request, user=Depends(require_user)):
    with get_db() as db:
        count=db.execute("SELECT COUNT(*) FROM recommendations WHERE user_id=?",(user["id"],)).fetchone()[0]
    return {"user":user,"recommendation_count":count}
