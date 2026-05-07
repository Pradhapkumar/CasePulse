from fastapi import APIRouter
from ..schemas import TranslateRequest
from ..services.translation_service import translate_text

router = APIRouter(prefix="/api/translate", tags=["translation"])

@router.post("")
def translate_content(request: TranslateRequest):
    return {
        "translated_text": translate_text(request.text, request.target_language)
    }
