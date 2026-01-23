from passlib.context import CryptContext

# Al añadir 'bcrypt_sha256' ayudamos a Passlib a manejar mejor los límites de bytes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_password_hash(password: str) -> str:
    # Si por alguna razón la contraseña es extremadamente larga, 
    # la cortamos para evitar el error de los 72 bytes
    if isinstance(password, str):
        password = password.encode('utf-8')
    return pwd_context.hash(password[:72]) 

def verificar_password(password_plano: str, password_hashed: str) -> bool:
    if isinstance(password_plano, str):
        password_plano = password_plano.encode('utf-8')
    return pwd_context.verify(password_plano[:72], password_hashed)

