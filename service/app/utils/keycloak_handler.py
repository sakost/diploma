import os

# import requests
import yaml
from dotenv import load_dotenv
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID


load_dotenv()
# from fastapi_keycloak import (
#     FastAPIKeycloak,
#     HTTPMethod,
#     KeycloakGroup,
#     KeycloakUser,
#     OIDCUser,
#     UsernamePassword,
# )


parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..", "configs")
)

with open(os.path.join(parent_dir, "keycloak-cfg.yaml")) as f:
    config = yaml.safe_load(f)

SERVER_URL = os.getenv("SERVER_URL")
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ADMIN_CLIENT_SECRET = os.getenv("ADMIN_CLIENT_SECRET")

keycloak_openid = KeycloakOpenID(
    server_url=SERVER_URL,
    client_id="login-app",
    realm_name="master",
    client_secret_key="3iQeeYeDrOqG1RqyoVEPVFwWwM47J2j2",
    # verify=True,
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{SERVER_URL}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{SERVER_URL}realms/{REALM}/protocol/openid-connect/token",
)


# try:
#     r = requests.get(f"{server_url}/realms/{realm}", timeout=3)
#     r.raise_for_status()
#     response_json = r.json()
# except requests.exceptions.HTTPError as errh:
#     print("Http Error:", errh)
# except requests.exceptions.ConnectionError as errc:
#     print("Error Connecting:", errc)
# except requests.exceptions.Timeout as errt:
#     print("Timeout Error:", errt)
# except requests.exceptions.RequestException as err:
#     print("OOps: Something Else", err)
# print(response_json)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# # oauth2_scheme = OAuth2AuthorizationCodeBearer(
# #     authorizationUrl=f"{server_url}realms/{realm}/protocol/openid-connect/auth",
# #     tokenUrl=f"{server_url}realms/{realm}/protocol/openid-connect/token",
# # )

# SECRET_KEY = f'-----BEGIN PUBLIC KEY-----\r\n{response_json["public_key"]}\r\n-----END PUBLIC KEY-----'

# keycloak_handler = FastAPIKeycloak(
#     server_url=f"{server_url}",
#     client_id=client_id,
#     client_secret=client_secret,
#     admin_client_secret=admin_client_secret,
#     realm=realm,
#     callback_uri=f"{server_url}/callback",
# )
# print(keycloak_handler)
# keycloak_openid = KeycloakOpenID(
#     server_url=config["server_url"],
#     client_id=config["client_id"],
#     realm_name=config["realm"],
#     client_secret_key=config.get("client_secret"),
# )

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl=f"{server_url}/realms/{realm}/protocol/openid-connect/auth",
#     tokenUrl=f"{server_url}/realms/{realm}/protocol/openid-connect/token",
# )
# print(oauth2_scheme)
