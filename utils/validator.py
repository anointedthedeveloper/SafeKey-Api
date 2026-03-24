from fastapi import HTTPException

def validate_params(length: int, uppercase: bool, lowercase: bool, numbers: bool, symbols: bool, count: int):
    if length < 6 or length > 64:
        raise HTTPException(status_code=400, detail="Length must be between 6 and 64.")
    if not any([uppercase, lowercase, numbers, symbols]):
        raise HTTPException(status_code=400, detail="At least one character type must be selected.")
    if count < 1 or count > 20:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 20.")
