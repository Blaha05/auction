from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy import delete, select
from auth.model import User
from auth.shemas import AddUserShema, UpdateUserShema
from database import async_session_maker
from fastapi.security import OAuth2PasswordRequestForm
from auth.hashed import HashedPassword
from auth.token import Token, get_current_user

router = APIRouter(
    tags=['auth']
)
token = Token()


@router.post('/register')
async def register(data:AddUserShema):
    async with async_session_maker() as session:

        data = data.dict()
        
        try:
            data['password'] = HashedPassword.hashed_password(data['password']).decode('utf-8')
            stmt = User(**data)
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: this email is already registered. {str(e)}"
            )



@router.post('/login')
async def login(response:Response, data:OAuth2PasswordRequestForm = Depends()):
    async with async_session_maker() as session:
        stmt = select(User).filter(User.email == data.username)
        user = await session.execute(stmt)  
        user = user.scalars().all() 
        if user:
            check = HashedPassword.check_password(data.password, user[0].password)
            if check:
                data_for_token = {
                    'id':user[0].id,
                    'email':user[0].email
                }

                token_ = token.create_token(data_for_token, 'Secret', 15)
                response.set_cookie(key="access_token", value=f'Bearer {token_}', max_age=1800, secure=True, samesite="none")
                return token_
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: пароль не правельний"
                )
        else:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Error: немає такого користувача"
                )



@router.put("/update_user", response_model=dict)
async def update_user_info(
    user_updates: UpdateUserShema,
    user:User = Depends(get_current_user)
):
    async with async_session_maker() as session:
        stmt = select(User).filter(User.id == user['id'])
        result = await session.execute(stmt)
        user = result.scalars().first() 

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_updates.email is not None:
            user.email = user_updates.email
        if user_updates.name is not None:
            user.name = user_updates.name
        
        await session.commit()

        return {"detail": "User information updated successfully"}


@router.delete('/delete_user')
async def dalete_user(user:User = Depends(get_current_user)):
    async with async_session_maker() as session:

        stmt = delete(User).where(User.id == user['id'])
        auction = await session.execute(stmt)
        await session.commit()
        return auction


@router.get('/get_user')
async def get_user():
    async with async_session_maker() as session:
        stmt = select(User)  
        users = await session.execute(stmt)  
        users = users.scalars().all() 
        return users