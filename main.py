from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

'''
    Define "Read SDN-R Connection List" request body 
    example:
    {
  "data-provider:input": {
    "filter": [{
      "property": "status",
      "filtervalue": "Connected"
      }
    ],
    "pagination": {
      "size": 10,
      "page": 1
     }
  }
}
'''
class DataProviderInputFilterObj(BaseModel):
    property: str
    filtervalue: str

class DataProviderInputPaginationObj(BaseModel):
    size: int
    page: int

class DataProviderInputObj(BaseModel):
    filter: List[DataProviderInputFilterObj]
    pagination: DataProviderInputPaginationObj

class ConnectListReqItem(BaseModel):
    data_provider_input: DataProviderInputObj = Field(alias="data-provider:input")


'''
    Verify username and password with basic oauth
'''
def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/v1/status")
def get_status(credentials: HTTPBasicCredentials = Depends(verify_user)):
    return {"status": "ok"}

@app.post("/rests/operations/data-provider:read-network-element-connection-list")
def read_network_elements(item: ConnectListReqItem, credentials: HTTPBasicCredentials = Depends(verify_user)):
    return item
    #pass