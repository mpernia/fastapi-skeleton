from fastapi import HTTPException


def abort(detail: str = "not authorization", status_code: int = 401):
    raise HTTPException(status_code, detail)
