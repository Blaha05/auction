from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select, delete
from auction.shema import AddAuctionShema, AddCategorieShema, AddCommentShema, AuctionUpdateShema
from auction.model import Auction, Categorie, Coment, History
from auction.wsmenger import ConnectionManager
from auth.model import User
from auth.token import get_current_user
from database import async_session_maker


router = APIRouter(
    tags=['auction']
)


manager = ConnectionManager()


@router.post('/add_auction')
async def add_auction(data:AddAuctionShema, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:
        data = data.dict()
        data['id_user'] = user['id']
        stmt = Auction(**data)
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt


@router.put('/change_auction')
async def change_auction(data:AuctionUpdateShema, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:

        stmt = select(Auction).filter(Auction.id == data.id)
        res = await session.execute(stmt)
        auctoion = res.scalars().first()

        if data.title is not None:
            auctoion.title = data.title
        if data.description is not None:
            auctoion.description = data.description
        if data.srart_price is not None:
            auctoion.srart_price = data.srart_price
        if data.start_at is not None:
            auctoion.start_at = data.start_at
        if data.finish_at is not None:
            auctoion.finish_at = data.finish_at
        
        await session.commit()
        await session.refresh(auctoion)

        return auctoion
    

@router.delete('/delete_auction')
async def delete_auction(id:int, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:

        stmt = delete(Auction).where(Auction.id == id)
        auction = await session.execute(stmt)
        await session.commit()
        return auction


@router.post('/add_comment')
async def add_comment(data:AddCommentShema, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:
        data = data.dict()
        data['id_user'] = user['id']
        stmt = Coment(**data)
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt


@router.delete('/delete_comment')
async def delete_comment(id:int, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:

        stmt = delete(Coment).where(Coment.id == id)
        auction = await session.execute(stmt)
        await session.commit()
        return auction


@router.post('/add_categorie')
async def add_comment(data:AddCategorieShema, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:
        data = data.dict()
        stmt = Categorie(**data)
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt


@router.delete('/delete_categorie')
async def delete_comment(id:int, user:User = Depends(get_current_user)):
    async with async_session_maker() as session:

        stmt = delete(Categorie).where(Categorie.id == id)
        auction = await session.execute(stmt)
        await session.commit()
        return auction


def AddHistory(bit:int, id_user:int, id_auction:int):
    stmt = History(**{
        'id_user':id_user,
        'id_auction':id_auction,
        'bit':bit
    })
    return stmt


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, id:int, token):
    async with async_session_maker() as session:
        stmt = select(Auction).filter(Auction.id == id)
        auction = await session.execute(stmt)
        auction = auction.scalars().first()
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                if int(data) - auction.curr_price > auction.step_bit:
                    auction.curr_price = int(data)
                    stmt = AddHistory(int(data), 11, auction.id)
                    session.add(stmt)
                    await manager.broadcast(f"Bit now: {auction.curr_price}")
                    await session.commit()
                    await session.refresh(auction)
                    await session.refresh(stmt)               
        except WebSocketDisconnect:
            manager.disconnect(websocket)