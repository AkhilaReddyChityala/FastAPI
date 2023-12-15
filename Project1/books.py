from fastapi import FastAPI

app=FastAPI()

BOOKS=[
    {'title':'Title One','author':'Author One','category':'Science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'Science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'History'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'Math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'Math'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'Math'}
]

# @app.get("/api-endpoint")
# async def first_api():
#     return {'message':'Hello Akhila!'}

@app.get("/books")
async def read_all_books():
    return BOOKS

# # Dynamic Paramter

# @app.get("/books/{dynamic_parameter}")
# async def read_all_books(dynamic_parameter):
#     return {'dynamic_paramter': dynamic_parameter}

# # Order matters with path_parameters
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'book title':'Favourite Book'}
#
#
# @app.get("/books/{dynamic_parameter}")
# async def read_all_books(dynamic_parameter):
#     return {'dynamic_paramter': dynamic_parameter}
# #
# #path_Parameters
#
@app.get("/books/{book_title}")
async def read_books(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold()==book_title.casefold():
            return book

