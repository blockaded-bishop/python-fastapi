from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    extra: str
    published: bool = True
    rating: Optional[int] = None

# Array of dictionaries
my_posts = [{"title": "Comment va ton francais!", "content": "bien, bien","id": 1}, {"title": "Il n'est pas dans ma veste!", "content": "Il est dans ton main", "id": 2}]

# return a post by id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
# get index of a post by id
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

# @app.post("/createposts")
# def create_posts(payLoad: dict=Body(...)):
#     print(payLoad)
#     return{"New_Post": f"Title: {payLoad['title']} Content: {payLoad['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
 #   return{"New_Post_Created": f"Title: {post.title}, Content: {post.content}, Published: {post.published}, Rating: {post.rating}"}
    return{"New_Post": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with {id} not found" )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"Message" : f"Post with {id} not found"}
    return{"YourPost": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with {id} not found" )
    my_posts.pop(index)  
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with {id} not found" )
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"UpdatedPost" : post_dict}
