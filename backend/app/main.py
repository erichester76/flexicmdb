from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import entity, ipam, itil, user
from .config import settings

app = FastAPI(title="FlexiCMDB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

app.include_router(entity.router, prefix="/entities", tags=["Entities"])
app.include_router(ipam.router, prefix="/ip_addresses", tags=["IPAM"])
app.include_router(itil.router, prefix="/itil", tags=["ITIL"])
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")

def root():
    return {"message": "FlexiCMDB API"}
