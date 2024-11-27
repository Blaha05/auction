from fastapi import FastAPI
from auth.router import router as router_auth
from auction.router import router as router_auction
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get('/')
async def test():
    return {'data' : 'hello'}

app.include_router(router_auth)
app.include_router(router_auction)

origins = [
    #"http://localhost:3000"
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Дозволити запити з цих оригіналів
    allow_credentials=True,
    allow_methods=["*"],  # Дозволити всі методи (GET, POST тощо)
    allow_headers=["*"],  # Дозволити всі заголовки
)