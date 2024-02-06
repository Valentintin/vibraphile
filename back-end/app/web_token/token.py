""" this file permit to configure a token per connection.
It's permit to keep the connection """
# import
import jwt
from datetime import datetime, timezone, timedelta
import uuid
from logging import getLogger

SECRET_KEY: str = None


# logger
logger = getLogger("vibraphile")


async def init_SECRET_KEY(secret_key: str = str(uuid.uuid4())):
    """ init the SECRET_KEY used for security of token """
    global SECRET_KEY
    SECRET_KEY = secret_key
    logger.info("SECRET_KEY init")


def generate_token(pseudonym: str) -> str:
    """ generate a new token for a pseudonym """
    expiration_time = (datetime.now(tz=timezone.utc)
                       + timedelta(hours=1, minutes=30)).timestamp()
    logger.debug("expiration_time: " + str(expiration_time))
    payload = {
        'pseudonym': pseudonym,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logger.debug(f"token generate for {pseudonym} ")
    return token


def verify_token(token: str) -> str:
    """ vérify the token and return the pseudonym if the token is correct """
    if not isinstance(token, str):
        logger.error("Token insn't init => user is not connected")
        return ""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        pseudonym = payload.get("pseudonym")
        if not pseudonym:
            logger.error("pseudonym doesn't exist")
            return ""
        logger.info("token is valid")
        return pseudonym
    except jwt.ExpiredSignatureError:
        logger.exception("Token has expired")
        return ""
    except jwt.InvalidTokenError:
        logger.exception("Invalid token")
        return ""
