import time
from fastapi import HTTPException, Request, status
from collections import defaultdict
from app.common.config import settings

# Rate limit configurations
RATE_LIMIT = settings.RATE_LIMIT_MAX_REQUESTS
RATE_LIMIT_PERIOD = settings.RATE_LIMIT_WINDOW

# Dictionary to store IP request timestamps
request_times = defaultdict(list)

def rate_limiter(request: Request):
    """
    Middleware to enforce a rate limit on incoming requests.

    This middleware records the time of each incoming request and blocks
    requests that exceed the rate limit.

    :param request: The incoming request
    :type request: fastapi.Request
    :raises HTTPException: If the rate limit is exceeded
    """
    client_ip = request.client.host
    current_time = time.time()

    # Remove requests older than RATE_LIMIT_PERIOD
    request_times[client_ip] = [
        timestamp for timestamp in request_times[client_ip]
        if current_time - timestamp < RATE_LIMIT_PERIOD
    ]

    # Check if client has exceeded the rate limit
    if len(request_times[client_ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )

    # Record the new request
    request_times[client_ip].append(current_time)
