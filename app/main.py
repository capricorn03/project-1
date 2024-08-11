from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True
 
while True:    
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi', 
                                    user='postgres', password='root@localhost',
                                    cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connected to the database")
        break

    except Exception as e:
        print("Connection to the database failed")
        print(f"Error: {e}")
        time.sleep(2)
     
@app.get("/")
def root():
    return {"message": "Hello World"}




@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, 
                   published = %s WHERE id = %s RETURNING *;""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return {"updated post": updated_post}




# after deleting anythonmg form the databse we need send the status code 204 
# and to change the dafault status code we need to pass the status code as argument in the decorator
# if we dont pass the status code then it will be 200 = ok by default
# but i dont know why after chaneg the default status code  return {"delted post ": deleted_post} is 
# not working unlike the case in default one

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    #anytime we making the changes in the database we need to commit the changes
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return {"delted post ": deleted_post}

# @app.get("/posts/latest")
# def latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"latest post": post}

@app.get("/posts/{id}")
def get_post(id : int):    
    #by default the id is of type string so we need to convert it to int to chack
    # that user have interd valid value or not but to
    # pass in databse we need pass it as string so we need to convert it to string
    #find more about str(id),
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was  not found")
    return {"post details": post}
    


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  
def create_posts( post : Post):
    # this will also work but dont use like this because this will cause the potential sql injection
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES (
    #     {post.title}, {post.content}, {post.published})")  
    # as this %s which is used for sanitizarion so that there no sql command input in the database
    
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
     #just doing these is not enough we need to commit the changes in datbse to save it using :-
    # connection.commit()
    connection.commit()
    return {"data": new_post}
   