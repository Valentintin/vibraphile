import jwt
import datetime

SECRET_KEY : str = None

from logging import getLogger
logger = getLogger("musehik")

async def initSECRET_KEY(secret_key : str):
    """ init the SECRET_KEY used for security of token """
    global SECRET_KEY
    SECRET_KEY = secret_key
    logger.info("SECRET_KEY init")

def generate_token(pseudonym : str) -> str:
    """ generate a new token for a pseudonym """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
    payload = {
        'pseudonym': pseudonym,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logger.debug(f"token generate for {pseudonym} ")
    return token

def verify_token(token: str) -> bool:
    if not isinstance(token, str):
        logger.error("Token insn't init => user is not connected")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        pseudonym = payload.get("pseudonym")
        if not pseudonym:
            logger.error("pseudonym doesn't exist")
            return ""
        logger.info("token is valid")
        return pseudonym
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        return ""
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        return ""