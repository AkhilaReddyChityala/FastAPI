from fastapi import FastAPI

app=FastAPI()

BOOKS=[
    {'title':'Title One','author':'Author One','category':'Science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'Science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'History'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'Math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'Math'},
    {'title': 'Title Six', 'author': 'Author two', 'category': 'Math'}
]

@app.get("/books/book_details/{author_name}")
async def book_details(author_name:str):
    books_to_return=[]
    for book in BOOKS:
        if book.get('author').casefold()==author_name.casefold():
             books_to_return.append(book)
    return books_to_return