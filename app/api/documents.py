from fastapi import APIRouter, File, UploadFile

router=APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
async def upload_document(file: UploadFile=File(...)) -> dict[str,str]:
    return{
        "filename":file.filename or "",
        "content_type":file.content_type or ""
    }