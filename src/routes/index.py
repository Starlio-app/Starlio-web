"""
This module defines API routes for serving static HTML files.
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/')
async def main():
    """Returns the main HTML page."""
    return FileResponse('./src/web/html/index.html')
