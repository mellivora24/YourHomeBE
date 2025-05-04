from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from config.database import supabase
from routes.auth import get_current_user

router = APIRouter()

@router.get("/account")
async def get_account(user_id: str = Depends(get_current_user)):
    user = supabase.table("users").select("*").eq("auth_id", user_id).single().execute().data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/account")
async def update_account(user_data: dict, user_id: str = Depends(get_current_user)):
    response = supabase.table("users").update(user_data).eq("auth_id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Update failed")
    return response.data[0]