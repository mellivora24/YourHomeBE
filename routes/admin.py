from fastapi import APIRouter, Depends, HTTPException
from services.email.email_service import email_service
from config.database import supabase
from routes.auth import get_current_user

router = APIRouter()


async def is_admin(user_id: str):
    user = supabase.table("users").select("role").eq("auth_id", user_id).single().execute().data
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return True


@router.get("/admin/homes")
async def get_homes(user_id: str = Depends(get_current_user)):
    # chỉ admin
    await is_admin(user_id)

    homes = supabase.table("home").select("*").execute().data
    return homes


@router.post("/admin/send-email")
async def send_admin_email(receiver_email: str, subject: str, content: str, user_id: str = Depends(get_current_user)):
    # chỉ admin
    await is_admin(user_id)

    await email_service.send_email(receiver_email, subject, content)
    return {"message": "Email sent"}
