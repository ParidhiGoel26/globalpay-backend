from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, wallet, extras
from db.database import engine
from db import table

table.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vave Bharat", version="0.0.0")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])
app.include_router(extras.router, tags=["Extra"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
