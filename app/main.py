# SWIFT Python API Web app 
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel #data validation
from typing import Optional
from random import randrange


app = FastAPI()

class validate_createposts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "my favorite foods", "content": "Biryani", "id": 1}, {"title": "likedfoods", "content": "Food made of egg", "id": 2}]

def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i
        
def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "We are in the home page"}

@app.get("/posts")
def getposts():
    return {"data": my_posts}

@app.post("/posts")
def createposts(post_payload: validate_createposts):
    post_payload_v1 = post_payload.model_dump()
    post_payload_v1['id'] = randrange(1, 1000000)
    my_posts.append(post_payload_v1)
    return {"data": post_payload_v1}

@app.get("/posts/{id}")
def getpost(id: int):
    post = find_post(int(id))
    if not post:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "post with id: {id} was not found"}
    return {"data": post}

@app.delete("/posts/{id}")
def deletepost(id: int):
    index = find_index(id)
    my_posts.pop(index)
    return {"message": "{id}"}