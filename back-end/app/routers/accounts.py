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
    dependencies=[Depends(verify_token)],
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
    except IntegrityError:
        raise HTTPException(400, detail="pseudo or email already used...")
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/")
async def create_account(new_account: Account) -> str:
    """
    create a new account !
    """
    async with get_session() as session:
        return await session.run_sync(bd_account.create, obj_in=new_account)


@router.get("/{pseudonym}")
async def read_account(pseudonym: str) -> Account:
    """
    return the accounts
    """
    try:
        async with get_session() as session:
            results = await session.run_sync(bd_account.get, pseudonym)
        if results is None:
            raise HTTPException(404)
        res: Account = results[0]
        res.password = "..."
        return res
    except Exception as e:
        raise HTTPException(500, str(e))
