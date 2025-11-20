from fastapi import FastAPI, HTTPException, Depends, Header
from authx import AuthX, AuthXConfig, RequestToken
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

class Settings(BaseSettings):
    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

config = AuthXConfig(
    JWT_ALGORITHM = "HS256",
    JWT_SECRET_KEY = settings.jwt_secret_key,
    JWT_TOKEN_LOCATION = ["headers"],
)

auth = AuthX(config=config)
auth.handle_errors(app)

@app.get("/login")
def login(username: str, password: str):
    if username == "xyz" and password == "xyz":
        token = auth.create_access_token(uid=username)
        return {"access_token": token}
    raise HTTPException(401, detail={"message": "Invalid credentials"})

@app.get("/protected")
def get_protected(token: str | None = Header(..., description="The token to access the protected route")):
     try:
          auth.verify_token(token=token)
          return {"message": "Hello world !"}
     except Exception as e:
          raise HTTPException(401, detail={"message": str(e)}) from e