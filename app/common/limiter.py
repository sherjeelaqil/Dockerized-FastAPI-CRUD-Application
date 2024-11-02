import time
from fastapi import HTTPException, Request, status
from collections import defaultdict

# Rate limit configurations
RATE_LIMIT = 5  # Max requests allowed
RATE_LIMIT_PERIOD = 60  # Time period in seconds

# Dictionary to store IP request timestamps
request_times = defaultdict(list)

def rate_limiter(request: Request):
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
