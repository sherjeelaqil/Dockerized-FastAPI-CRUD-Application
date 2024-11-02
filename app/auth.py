# app/auth.py
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.schemas.token import Token, TokenData
from app.common.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verify that a plaintext password matches a hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """
    Create an access token from a dictionary of data.

    Args:
        data (dict): The data to encode into the token.

    Returns:
        str: The access token as a JSON Web Token (JWT).

    Notes:
        The token will expire after the number of minutes specified in the
        ACCESS_TOKEN_EXPIRE_MINUTES setting.
    """
    
    to_encode = data.copy()
    # Use timezone-aware datetime
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str):
    """
    Decode an access token into its underlying data.

    Args:
        token (str): The access token to decode.

    Returns:
        TokenData: The decoded data.

    Raises:
        ValueError: If the token is invalid or does not contain a username.

    Notes:
        The token is expected to be a JSON Web Token (JWT) signed with the
        SECRET_KEY setting. The decoded data will contain the "sub" claim,
        which should be the username of the user that the token represents.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Token does not contain username")
        return TokenData(username=username)
    except JWTError:
        raise ValueError("Invalid token")