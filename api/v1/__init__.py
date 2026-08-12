from fastapi import APIRouter

from .transactions import router as transactions_router

router = APIRouter()

router.include_router(transactions_router)
