from fastapi import Header, HTTPException
import jwt

SECRET = "YOUR_SECRET_KEY"

def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload  # {"user_id": 123}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
