from fastapi import APIRouter, Depends, HTTPException
from web_token.token import verify_token
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
        logger.debug(type(results))
        res: list[str] = []
        for row in results:
            tmp_dict = dict(row._mapping)
            res.append("/accounts/"+tmp_dict.get('pseudonym'))
        return res
    except Exception as e:
        return HTTPException(500, str(e))


@router.get("/{pseudonym}")
async def read_account():
    """
    return the accounts
    """
    pass
