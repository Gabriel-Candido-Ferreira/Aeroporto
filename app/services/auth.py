from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database import db
from bson import ObjectId
from app.utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="funcionarios/login")

funcionarios_collection = db.funcionarios

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await funcionarios_collection.find_one({"_id": ObjectId(user_id)})
    if user is None or "cargo" not in user:
        raise credentials_exception

    return {
        "id": str(user["_id"]),
        "nome": user["nome"],
        "cargo": user["cargo"],
        "email": user["email"]
    }


async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["cargo"].lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ação permitida apenas para administradores"
        )
    return current_user


async def get_current_non_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["cargo"].lower() == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ação não permitida para administradores nesta rota"
        )
    return current_user
