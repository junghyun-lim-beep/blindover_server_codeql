from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
import os

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

# model = torch.load('your_model.pt')
# model.eval()


@app.post("/photo")
async def create_upload_file(file: UploadFile = File(...)):

  ################################파일 업로드 부분#####################################
  UPLOAD_DIR = "./photo"  # 이미지를 저장할 서버 경로
    
  content = await file.read()
  filename = "test.jpg"  # uuid로 유니크한 파일명으로 변경
  with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
      fp.write(content)
  print(file)
  ####################################################################################

  

  return {
      "content_type": file.content_type,
      "filename": file.filename
  }




# @app.post('/predict')
# def predict(data: YourInputDataModel):
#     # 입력 데이터 처리 및 전처리
#     # ...
#     # 모델에 입력 데이터 전달하여 예측
#     output = model(input_data)
#     # 예측 결과 반환
#     return {'prediction': output}