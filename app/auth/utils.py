from passlib.context import CryptContext

SECRET_KEY = "tu_llave_secreta_fija_123"
ALGORITHM = "HS256"
# Al añadir 'bcrypt_sha256' ayudamos a Passlib a manejar mejor los límites de bytes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plana, password_hasheada):
    return pwd_context.verify(password_plana, password_hasheada)

def obtener_password_hash(password):
    return pwd_context.hash(password)
