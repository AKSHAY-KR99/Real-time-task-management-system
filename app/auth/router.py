from fastapi import APIRouter, HTTPException, status, Depends
from app.auth.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.auth.services import create_user, authenticate_user
from app.core.dependencies import get_current_user
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=UserResponse,
             responses={400: {"model": UserResponse}, 422: {"description": "Validation Error"}})
async def register(user: UserCreate):
    new_user = await create_user(user.email, user.password, user.full_name, user.role)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    try:
        user = await authenticate_user(data.email, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token_data = {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        }

        token = create_access_token(token_data)
        return {"access_token": token}

    except HTTPException:
        raise
    except Exception as e:
        print("Login Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user