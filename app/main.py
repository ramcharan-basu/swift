# MDM Integration Python API Web app 
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel #input data validation
from typing import Optional #input data validation
from random import randrange #generates random number & can be used for ID columns

app = FastAPI()

class validate_createcustomers(BaseModel):
    customerid: int
    firstname: str
    lastname: str
    city: str
    state: str
    postalcode: Optional[int] = None
    country: str = 'US'

    

my_customers = [{"customerid": 1, "firstname": "Bruce", "lastname": "Willis", "city": "Austin", "state": "TX", "postalcode": "12345", "country": "US"},
            {"customerid": 2, "firstname": "Akshay", "lastname": "Patel", "city": "San Jose", "state": "CA", "postalcode": "12345", "country": "US"},
            {"customerid": 3, "firstname": "Baskar", "lastname": "Jollu", "city": "Louisville", "state": "KY", "postalcode": "12345", "country": "US"}
            ]

def find_post(customerid):
    for i in my_customers:
        if i['customerid'] == customerid:
            return i
        
def find_index(customerid):
    for i, p in enumerate(my_customers):
        if p['customerid'] == customerid:
            return i

@app.get("/")
def read_root():
    return {"message": "You are in the home page"}

@app.get("/customers")
def getcustomers():
    return {"data": my_customers}

@app.get("/customers/{customerid}")
def getcustomerbyid(customerid: int):
    post = find_post(int(customerid))
    if not post:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Cusomer with rid: {customerid} was not found"}
    return {"data": post}

@app.post("/customers")
def createcustomers(post_payload: validate_createcustomers):
    post_payload_v1 = post_payload.model_dump()
#   post_payload_v1['customerid'] = randrange(1, 1000000)
    my_customers.append(post_payload_v1)
    return {"data": post_payload_v1}


@app.put("/customers/{customerid}")
def updatecustomers(customerid: int, post_payload: validate_createcustomers):
    index = find_index(customerid)
    post_dict = post_payload.model_dump()
    post_dict['customerid'] = customerid
    my_customers[index] = post_dict
    return {"message": post_dict}

@app.delete("/customers/{customerid}")
def deletecustomers(customerid: int):
    index = find_index(customerid)
    my_customers.pop(index)
    return {"message": "Custumer with id {customerid} has been deleted"}