import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas
from typing import List

app = _fastapi.FastAPI()

_services.create_database()

@app.post("/users/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db:_orm.Session=_fastapi.Depends(_services.get_db)
    ):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="Email already in use"
            )
    return _services.create_user(db=db, user=user)

@app.get("/users/", response_model=List[_schemas.User])
def read_user(
    skip: int=0, limit: int=10, db:_orm.Session=_fastapi.Depends(_services.get_db) 
):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/user/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(user_id=user_id, db=db)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")
    
    return db_user

@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(
    user_id: int,
    post: _schemas.PostCreate,
    db:_orm.Session=_fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user(user_id=user_id, db=db)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")
    
    return _services.create_post(db=db, post=post, user_id=user_id)

@app.get("/posts/", response_model=List[_schemas.Post])
def read_posts(
    skip: int=0, limit: int=10, db:_orm.Session=_fastapi.Depends(_services.get_db) 
):
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_post = _services.get_post(post_id=post_id, db=db)
    if db_post is None:
        raise _fastapi.HTTPException(status_code=404, detail="Post not found")
    
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"Post with id {post_id} has been successfully deleted"}

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    _services.update_post(db=db, post_id=post_id, post=post)
    return {"message": f"Post with id {post_id} has been successfully updated"}