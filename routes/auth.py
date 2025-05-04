from fastapi import APIRouter, HTTPException, Depends
from models.user import UserCreate
from config.database import supabase
from jose import jwt
from config.settings import settings
from typing import Optional
from gotrue.errors import AuthApiError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    try:
        if not settings.SECRET_KEY or not isinstance(settings.SECRET_KEY, str):
            raise HTTPException(status_code=500, detail="Invalid or missing SECRET_KEY")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        auth_id = payload.get("sub")
        if not auth_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return auth_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register")
async def register(user: UserCreate):
    existing = supabase.table("users").select("email").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered in database")

    try:
        auth_response = supabase.auth.sign_up({"email": user.email, "password": user.password})
    except AuthApiError as e:
        if "User already registered" in str(e):
            raise HTTPException(status_code=400, detail="User already registered with this email")
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

    if not auth_response.user:
        raise HTTPException(status_code=400, detail="Failed to register with Supabase Auth")

    auth_id = auth_response.user.id
    print(f"Supabase Auth ID: {auth_id}")

    user_data = user.dict()
    user_data["auth_id"] = auth_id
    response = supabase.table("users").insert(user_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to insert user into database")

    print(f"Inserted user: {response.data}")
    return {"message": "User registered", "user_id": response.data[0]["user_id"]}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username  # OAuth2 sử dụng 'username' field cho email
    password = form_data.password

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not response.user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not settings.SECRET_KEY or not isinstance(settings.SECRET_KEY, str):
        raise HTTPException(status_code=500, detail="Invalid or missing SECRET_KEY")

    token = jwt.encode({"sub": response.user.id}, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@router.delete("/account")
async def delete_account(email: str, password: str, current_user_id: str = Depends(get_current_user)):
    # Tìm user trong bảng users dựa trên email
    user = supabase.table("users").select("*").eq("email", email).single().execute().data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Xác minh email và mật khẩu
    try:
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {str(e)}")

    if not auth_response.user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Kiểm tra quyền: Chỉ chính user hoặc admin được xóa
    user_auth_id = user["auth_id"]
    current_user = supabase.table("users").select("role").eq("auth_id", current_user_id).single().execute().data
    if not current_user:
        raise HTTPException(status_code=404, detail="Current user not found")

    if current_user_id != user_auth_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to delete this account")

    # Xóa user khỏi bảng users
    response = supabase.table("users").delete().eq("email", email).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to delete user from database")

    # Lưu ý: Xóa khỏi Supabase Auth cần Admin API, chưa hỗ trợ trực tiếp
    print(f"Account deleted from database: {email}")

    return {"message": "Account deleted successfully", "email": email}