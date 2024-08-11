from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None
 

my_posts = [{
    "title":"this is the title of the new post ",
    "content":"this is the content of the new post",
    "id":1
},{
    "title":"this is the title of the new post ",
    "content":"this is the content of the new post",
    "id":2
}]

# @app.delete("/post/{id}")
# def delete_post(id)


def find_post(id):
    for p in my_posts:
       if p['id'] == id:
          return p
 

@app.get("/")
def root():
    return {"message": "Hello World"}

# order of the decorater matters if we have used some variable
# with same http method like in this case of @app.get("/posts/{id}") 
# and @app.get("/post/latest") otherwise it will give error by 
# treating the latest as and id varible

@app.get("/posts/latest")
def latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest post": post}

 #post id should be converted into integer as the usrl
 #prams always comes as a string 
 
@app.get("/posts/{id}")
def get_post(id : int, response: Response):    
    post = find_post(id)    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id:{id} was not found"}
    print(post)
    return {"post details": post}
    


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  
def create_posts( post : Post):
    
    post_dic = post.model_dump()
    post_dic['id'] = randrange(0, 1000000)
    my_posts.append(post_dic)
    
    print(post)
    print(post.model_dump()) # equals to post.dict() to print post body in dictionary formate
    
    return {"data": post_dic}


# from fastapi.params import Body
# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"newpost": f"title {payload['title']} content {payload['content']}"}

