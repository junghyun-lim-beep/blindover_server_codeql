from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from torchvision.transforms import ToTensor
from PIL import Image
import torch
import os

from loguru import logger


model = torch.load('shufflenet_weight.pt', map_location=torch.device('cpu'))

app = FastAPI()


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
  image = ToTensor()(Image.open(file.file))
  output = model(image)
  logger.info("Classify Result = {}", output)
  return {
      "content_type": file.content_type,
      "filename": file.filename
  }






class Model(BaseModel):
    name: str
    phoneNumber: int

@app.get("/")
def 이름():
  return '보낼 값'

@app.post("/send")
def data받기(data : Model):
  print(data)
  return '전송완료'