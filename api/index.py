import logging
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.generator import generate_password, calculate_strength
from utils.validator import validate_params

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="SafeKey API", description="Cryptographically secure password generator", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/generate")
@limiter.limit("10/minute")
def generate(
    request: Request,
    length: int = Query(default=12),
    uppercase: bool = Query(default=True),
    lowercase: bool = Query(default=True),
    numbers: bool = Query(default=True),
    symbols: bool = Query(default=True),
    exclude_similar: bool = Query(default=False),
    count: int = Query(default=1),
):
    validate_params(length, uppercase, lowercase, numbers, symbols, count)

    passwords = [generate_password(length, uppercase, lowercase, numbers, symbols, exclude_similar) for _ in range(count)]
    strength_info = calculate_strength(passwords[0])

    logger.info("Generated %d password(s) | length=%d | ip=%s", count, length, get_remote_address(request))

    return {
        "status": "success",
        "passwords": passwords,
        "strength": strength_info["strength"],
        "entropy": strength_info["entropy"],
    }


@app.get("/")
def root():
    return {"message": "SafeKey API is running. Visit /docs for Swagger UI."}


# Vercel serverless handler
from mangum import Mangum
handler = Mangum(app)
