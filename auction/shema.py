from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class AddAuctionShema(BaseModel):
    title: str
    description: str
    srart_price: Optional[Decimal] = 0.00
    curr_price: Optional[Decimal] = 0.00
    start_at: datetime
    finish_at: datetime

class AuctionUpdateShema(BaseModel):
    id:int
    title: Optional[str] = None
    description: Optional[str] = None
    srart_price: Optional[Decimal] = None
    start_at: Optional[datetime] = None
    finish_at: Optional[datetime] = None

class AddCommentShema(BaseModel):
    coment:str
    id_auction:int

class AddCategorieShema(BaseModel):
    categorie:str
    id_auction:int

