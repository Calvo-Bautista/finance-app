from fastapi import HTTPException, status
from app.models.user import UserCreate, UserInDB
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.config.database import db

async def register_user(user: UserCreate):
    database = db.get_db()
    
    # 1. Verificar si el email ya existe
    existing_user = await database["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # 2. Hash del password
    hashed_password = get_password_hash(user.password)
    
    # 3. Crear documento
    user_in_db = UserInDB(
        **user.model_dump(), 
        hashed_password=hashed_password
    )
    
    # 4. Insertar en BD
    new_user = await database["users"].insert_one(user_in_db.model_dump())
    
    # 5. Retornar el usuario creado (con el ID generado)
    created_user = await database["users"].find_one({"_id": new_user.inserted_id})
    return created_user

async def login_user(form_data):
    database = db.get_db()
    
    # 1. Buscar usuario
    user = await database["users"].find_one({"email": form_data.username}) # OAuth2 usa 'username' para el email
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Crear token
    access_token = create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}