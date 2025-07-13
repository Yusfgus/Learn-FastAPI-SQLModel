from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using a secure hashing algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def rebuld_models():

    from .models import subject_model, GP_model, email_model

    subject_model.rebuld_models()
    GP_model.rebuld_models()
    email_model.rebuld_models()