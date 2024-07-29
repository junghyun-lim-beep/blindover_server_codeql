from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from torchvision.transforms import ToTensor
from PIL import Image
import torch
import os
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from inference import inference
from inference import load_image

from inference import quantized_load_image
from inference import modelReturn
from paramiko.client import SSHClient, AutoAddPolicy, RejectPolicy
import time

# from colabcode import ColabCode
# cc = ColabCode(port=8000, code=False)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/photo")
async def create_upload_file(file: UploadFile = File(...)):

  ################################파일 업로드 부분#####################################
  # UPLOAD_DIR = "./photo"  # 이미지를 저장할 서버 경로
    
  # content = await file.read()
  # filename = "test.jpg"  # uuid로 유니크한 파일명으로 변경
  # with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
  #     fp.write(content)
  # print("@@@@@@@@@@이미지 업로드 완료!! @@@@@@@@@@@")
  ####################################################################################
  # image = ToTensor()(Image.open(file.file))
  # output = model(image)
  # logger.info("Classify Result = {}", output)

  model = modelReturn(False, "shufflenet", "./weights/shufflenet_weight.pt")
  start = time.time()
  # img = load_image(file)
  img = load_image(file)
  result = inference(img, model)
  print(result)
  print(time.time() - start)
  return


class Model(BaseModel):
    name: str
    phoneNumber: int

@app.get("/")
def 이름():
  return '보낼 값'

def unsafe_connect():
    client = SSHClient()
    client.set_missing_host_key_policy(RejectPolicy)
    client.connect("example.com")

    # ... interaction with server

    client.close()

@app.post("/send")
def data받기(data : Model):
  print(data)
  return '전송완료'

# cc.run_app(app=app)
