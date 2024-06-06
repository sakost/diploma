from fastapi import HTTPException, Security, status

from app.utils.keycloak_handler import keycloak_openid, oauth2_scheme


async def get_idp_public_key():

    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


async def get_auth(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(token, key=await get_idp_public_key())
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# async def get_current_user_role(payload: dict = Depends(get_auth)) -> str:
#     role = payload.get("role")  # TODO: return role. Need to test with real keycloak
#     return "admin"  # for now it's fake role
async def get_current_user_role() -> str:
    # TODO: return role. Need to test with real keycloak
    return "admin"


async def requires_role(user_role: dict, required_role: str):

    if user_role != required_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to perform this action",
        )
