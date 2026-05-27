from fastapi import APIRouter, HTTPException
from app.schemas.sync import SyncRequest, SyncResponse
from pipeline.sync import run_sync, run_sync_delta

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


@router.post("/delta", response_model=SyncResponse)
def sync_delta(req: SyncRequest):
    """e-Class 알림 기반 증분 동기화 — 변경된 과목만 처리."""
    try:
        result = run_sync_delta(lms_id=req.lms_id, cookie_str=req.cookie_str)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
