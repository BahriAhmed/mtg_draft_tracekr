from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
import yaml

def load_credentials():
    with open("conf/local/credentials.yml", "r") as file:
        return yaml.safe_load(file)
    
creds = load_credentials()

SECRET_KEY = creds["credentials"]["jwt"]["secret_key"]
ALGORITHM = creds["credentials"]["jwt"]["algorithm"]
EXPIRES_MINUTES = creds["credentials"]["jwt"]["expires_minutes"]



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None