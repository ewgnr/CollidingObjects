import rncryptor, uuid, sqlite3, os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from app.auth import Authorization
from app.crypto import Crypto

conn = sqlite3.connect("datenbank.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        fileId TEXT PRIMARY KEY,
        fileContent TEXT
    )
''')
conn.commit()
conn.close()

crypto = Crypto()
auth = Authorization()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()

class Anonymize(BaseModel):
    values: list[str]

password = os.getenv("PASSWORD")
passwordstr = os.getenv("PASSWORDSTR")

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    cryptor = rncryptor.RNCryptor()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        user = cryptor.decrypt(bytes.fromhex(password), passwordstr)
        return user
    except:
        raise credentials_exception

@app.post("/login")
async def login_for_access_token(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth.authenticate_user(password, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token = auth.create_access_token(data={"sub": user})
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/saveSession")
async def save_session(
    current_user: Annotated[str, Depends(get_current_user)], password: str = Form(...), file: UploadFile = File(...)
):
    file_content = await file.read()
    encrypted_content = crypto.encrypt(file_content.decode(), password)
    file_id = str(uuid.uuid4())

    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (fileId, fileContent) VALUES (?, ?)
    ''', (file_id, encrypted_content))
    conn.commit()
    conn.close()

    return {"encrypted_file": encrypted_content, "file_id": file_id}

@app.post("/getSession")
async def get_session(
    current_user: Annotated[str, Depends(get_current_user)], password: str = Form(...), file_id: str = Form(...)
):
    conn = sqlite3.connect("datenbank.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fileContent FROM files WHERE fileId = ?
    ''', (file_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    encrypted_content = row[0]
    decrypted_content = crypto.decrypt(encrypted_content, password)
    
    return Response(content=decrypted_content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_id}.csv"})
