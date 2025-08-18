from fastapi import APIRouter, Query
from typing import Optional
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/by-date", summary="Report expenses by date")
async def report_by_date(
    start_date: Optional[str] = Query(None, example="2025-08-01"),
    end_date: Optional[str] = Query(None, example="2025-08-31"),
    group_by: str = Query("month", enum=["day", "month", "year"]),
    category: Optional[str] = Query(None, example="Mano de obra")
):
    return await report_service.report_by_date(start_date, end_date, group_by, category)


@router.get("/by-category", summary="Report expenses by category")
async def get_report_by_category(
    start_date: Optional[str] = Query(None, example="2025-08-01"),
    end_date: Optional[str] = Query(None, example="2025-08-31"),
    category: Optional[str] = Query(None, example="Insumos")
):
    return await report_service.report_by_category(start_date, end_date, category)
