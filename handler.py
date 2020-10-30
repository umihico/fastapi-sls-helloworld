import requirements
from fastapi.responses import RedirectResponse
import base64
import datetime
import secrets
from fastapi import FastAPI, Request
from mangum import Mangum

app = FastAPI()


@app.get("/login")
def login(path: str = ""):
    return RedirectResponse("/" + path)


def any(request: Request):
    if not _auth(request.headers):
        return RedirectResponse("/login?path=" + request.url.path[1:])
    return request.url.path


app.get("/{any}")(any)
app.get("/")(any)


def _auth(headers):
    if 'Authorization' not in headers:
        return False
    username, password = base64.standard_b64decode(
        headers['Authorization'][6:]).decode("utf-8").split(":")
    correct_username = secrets.compare_digest(username, "hoge")
    correct_password = secrets.compare_digest(
        password, str(datetime.datetime.now().minute))
    return all([correct_username, correct_password])


handler = Mangum(app, enable_lifespan=False)


def auth(event, context):
    if _auth(event['headers']):
        return {
            "principalId": 1,
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "*",
                        "Effect": "Allow",
                        "Resource": "*"
                    }
                ]
            }
        }
    raise Exception('Unauthorized')  # 401
