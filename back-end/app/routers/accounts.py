from fastapi import APIRouter, Depends, HTTPException
from web_token.token import verify_token
from sqlalchemy.exc import IntegrityError
from database.crud_request.bd_account import Bd_account
from database.model import Account
from database.bd_setup import get_session
from logging import getLogger

logger = getLogger("vibraphile")

bd_account: Bd_account = Bd_account(Account)

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_accounts() -> list[str]:
    """
    return list of all accounts
    """
    try:
        async with get_session() as session:
            results = await session.run_sync(bd_account.get_all)
        if results is None:
            raise HTTPException(404)
        res: list[str] = []
        for row in results:
            tmp_dict = dict(row._mapping)
            res.append("/accounts/"+tmp_dict.get('pseudonym'))
        return res
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/")
async def create_account(new_account: Account) -> str:
    """
    create a new account !
    """
    try:
        async with get_session() as session:
            return await session.run_sync(bd_account.create,
                                          obj_in=new_account)
    except IntegrityError:
        raise HTTPException(400, detail="pseudo or email already used...")
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/login")
async def login(email: str, password: str) -> str:
    try:
        async with get_session() as session:
            return await session.run_sync(bd_account.connection,
                                          email, password)
    except IntegrityError:
        raise HTTPException(400, detail="pseudo or email already used...")
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/{pseudonym}", dependencies=[Depends(verify_token)])
async def read_account(pseudonym: str) -> dict:
    """
    return the accounts
    """
    try:
        async with get_session() as session:
            res: Account = await session.run_sync(bd_account.get, pseudonym)
        if res is None:
            raise HTTPException(404)
        return res.model_dump(exclude={'password': True})
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/{pseudonym}", dependencies=[Depends(verify_token)])
async def update_account(pseudonym: str,
                         obj_in: dict) -> dict:
    """
    update the account
    """
    try:
        async with get_session() as session:
            res: Account = await session.run_sync(bd_account.update,
                                                  pseudonym=pseudonym,
                                                  obj_in=obj_in)
        return res.model_dump(exclude={'password': True})
    except Exception as e:
        raise HTTPException(500, str(e))


@router.delete("/{pseudonym}", dependencies=[Depends(verify_token)])
async def delete_account(pseudonym: str) -> dict:
    """
    delete the account by pseudonym
    """
    try:
        async with get_session() as session:
            res: Account = await session.run_sync(bd_account.remove,
                                                  id=pseudonym)
        return res.model_dump(exclude={'password': True})
    except Exception as e:
        raise HTTPException(500, str(e))
