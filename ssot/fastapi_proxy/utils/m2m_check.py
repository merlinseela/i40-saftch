from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security_scheme = HTTPBearer()

def m2m_check(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
):
    ssot_context = request.app.state.ssot_context
    expected_token = ssot_context.ssot_environment["M2M_SECRET_KEY"]
    
    if not expected_token:
        raise HTTPException(status_code=500, detail="Server Error: M2M_BEARER_TOKEN not configured in .env.")
        
    if credentials.credentials != expected_token:
        print("TEST UNAUTHORIZED")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Token")
        
    return credentials.credentials