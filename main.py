from fastapi import FastAPI
from src.routers import employee_router, partner_router

app = FastAPI(title="Partners APP")

app.include_router(employee_router)
app.include_router(partner_router)
