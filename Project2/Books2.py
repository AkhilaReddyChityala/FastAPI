from typing import Optional
from fastapi import FastAPI,Body,Path,Query,HTTPException,status
from pydantic import BaseModel,Field
from starlette import status
app = FastAPI()


class Book:
    id:int
    title: str
    author: str
    description: str
    rating: int
    published_date:int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date


class BookRequest(BaseModel):
    id:Optional[int]=(None)==Field(title='Id is not needed')
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=1,lt=6)
    published_date:int=Field(gt=1900,lt=3000)
    class Config:
        json_schema_extra={
            'example':{
                'title':'A new book',
                'author':'Author of the Book',
                'description':'Write about book',
                'rating':5,
                'published_date':'Enter an year'
            }
        }

BOOKS=[
    Book(1,'ECE','Akhila','Branch is good',4,2015),
    Book(2, 'ECE', 'Shiva', 'nice good', 4,1998),
    Book(3, 'ECE', 'Nikhila', 'nice ', 2,2015),
    Book(4, 'CSE', 'Saritha', ' good', 3,1997),
    Book(5, 'EEE', 'CTR', 'Excellent', 5,2020),
    Book(6, 'Civil', 'Kushi', 'Beautiful', 5,2080)

]

@app.get("/books/")
async def read_all_books():
    return BOOKS

#Find a Book based on Book ID
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail='Item not found')

#Find the book with rating
@app.get("/book/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int=Query(gt=1,lt=7)):
    book_to_return=[]
    for book in BOOKS:
        if book.rating==book_rating:
            book_to_return.append(book)
    return book_to_return

#Get request filter with published data
@app.get("/books/publish",status_code=status.HTTP_200_OK)
async def read_book_by_publisheddate(book_published_rate:int=Query(gt=1900,lt=3000)):
    book_to_return=[]
    for book in BOOKS:
        if book.published_date==book_published_rate:
            book_to_return.append(book)
    return book_to_return

@app.post("/create_book",status_code=status.HTTP_201_CREATED)
async def create_books(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    print(type(book_request))
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

#Put Request
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed = True
    if not book_changed:
            raise HTTPException(status_code=404,detail='Item not found')

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
            raise HTTPException(status_code=404,detail='Item not found')

def find_book_id(book:Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    # if len(BOOKS)>0:
    #     book.id=BOOKS[-1].id+1
    # else:
    #     book.id=1
    return book

