from fastapi import APIRouter, HTTPException
from app.schemas.sync import SyncRequest, SyncResponse
from pipeline.sync import run_sync

router = APIRouter()


@router.post("", response_model=SyncResponse)
def sync(req: SyncRequest):
    try:
        result = run_sync(lms_id=req.lms_id, cookie_str=req.cookie_str)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
