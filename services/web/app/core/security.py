from app import cruds
from app.core.config import get_settings
from app.database import session
from fastapi_login import LoginManager

loginManager = LoginManager(get_settings().AUTH_SECRET_KEY, token_url="/api/admin/login")

class PasswordManager:
    def __init__(self):
        pass

    def verify(self, password: str, hashed_password: str):
        return loginManager.pwd_context.verify(password, hashed_password)

    def getPasswordHash(self, password: str):
        return loginManager.pwd_context.hash(password)

passwordManager = PasswordManager()

@loginManager.user_loader()
def load_user(username: str):
    with session.SessionLocal() as db:
        return cruds.CRUDAdmin(db).getByUsername(username)