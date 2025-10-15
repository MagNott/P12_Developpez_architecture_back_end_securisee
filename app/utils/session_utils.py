import jwt
import datetime
import os

SECRET_KEY = "ma_cle_secrete"  # à protéger dans .env plus tard
SESSION_FILE = ".session"


# A TESTER HAPPY 
def generate_token(collaborator):
    """
    Create a JWT token for a collaborator with an expiration time
   """
    today = datetime.datetime.now()
    payload = {
        "login": collaborator.login,
        "exp": today + datetime.timedelta(minutes=1),
        "department": collaborator.department.name
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_token(token):
    """
    Save the token in a local text file (.session)
    """
    with open(SESSION_FILE, "w", encoding="utf-8") as file:
        file.write(token)


def is_authenticated():
    """
    Check if the user is authenticated by verifying the token's existence and
    validity
    """
    if not os.path.exists(SESSION_FILE):
        return False
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as file:
            token = file.read()
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False


def load_token():
    pass


def delete_token():
    pass


def is_token_expired():
    pass
