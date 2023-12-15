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

# Query Parameter
@app.get("/books/")
async def read_category(category:str):
    books_return=[]
    for book in BOOKS:
        if book.get('category').casefold()==category.casefold():
            books_return.append(book)
    return

# Combination of Path parameter and Query parameter
@app.get("/book/{book_author}")
async def return_books_query(book_author:str , category:str):
    books_return=[]
    for book in BOOKS:
        if book.get('author').casefold()== book_author.casefold() and \
           book.get('category').casefold() == category.casefold():
                books_return.append(book)
    return books_return


