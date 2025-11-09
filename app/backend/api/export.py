"""
API endpoints for exporting results
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schemas import OptimizationResult
from services.google_sheets import GoogleSheetsService

router = APIRouter()
sheets_service = GoogleSheetsService()

class ExportToSheetsRequest(BaseModel):
    """Request to export to Google Sheets"""
    result: OptimizationResult
    spreadsheet_id: str
    worksheet_name: str = "Optimization Results"

@router.post("/sheets")
async def export_to_google_sheets(request: ExportToSheetsRequest):
    """
    Export optimization result to Google Sheets
    
    Args:
        request: ExportToSheetsRequest with result and spreadsheet ID
    
    Returns:
        Success status
    """
    if not sheets_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Google Sheets export is not configured. Please set up credentials."
        )
    
    try:
        success = sheets_service.export_optimization_result(
            result=request.result,
            spreadsheet_id=request.spreadsheet_id,
            worksheet_name=request.worksheet_name
        )
        
        if success:
            return {
                'success': True,
                'message': f'Results exported to Google Sheets worksheet: {request.worksheet_name}'
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to export to Google Sheets")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting to Google Sheets: {str(e)}")

@router.get("/sheets/status")
async def get_sheets_status():
    """
    Check if Google Sheets export is available
    
    Returns:
        Status information
    """
    return {
        'available': sheets_service.is_available(),
        'configured': sheets_service.is_available()
    }

