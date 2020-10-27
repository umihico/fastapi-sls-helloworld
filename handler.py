import requirements
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def hello_world():
    return {"hello": "world"}


handler = Mangum(app, enable_lifespan=False)
