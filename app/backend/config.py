"""
Configuration settings for the backend application
"""
import os
from pathlib import Path

# Get the project root (app folder's parent)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "Data"
INPUTFILES_ROOT = PROJECT_ROOT / "Inputfiles"
RESULTS_ROOT = PROJECT_ROOT / "Results"

# Simple settings class (avoiding pydantic_settings dependency for MVP)
class Settings:
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX = "/api/v1"
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:3001"]
    
    # Data Paths
    DATA_ROOT = DATA_ROOT
    INPUTFILES_ROOT = INPUTFILES_ROOT
    RESULTS_ROOT = RESULTS_ROOT
    
    # Model Settings
    MODEL_TYPE = "delgado_venezian"  # delgado_venezian, baseline, optimized_actual, bax_fixed
    GUROBI_LOG_TO_CONSOLE = False
    
    # Google Sheets (optional)
    GOOGLE_SHEETS_CREDENTIALS_PATH = None
    GOOGLE_SHEETS_ENABLED = False

settings = Settings()

