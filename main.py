from fastapi import FastAPI
from pydantic import BaseModel

class Model(BaseModel):
    name: str
    phoneNumber: int


app = FastAPI()

@app.get("/")
def 이름():
  return '보낼 값'

@app.post("/send")
def data받기(data : Model):
  print(data)
  return '전송완료'