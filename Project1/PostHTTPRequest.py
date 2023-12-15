from fastapi import Body, FastAPI
app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'Science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'Science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'History'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'Math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'Math'},
    {'title': 'Title Six', 'author': 'Author Six', 'category': 'Math'}
]


@app.post("/books/create_book")
async def post_create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.get("/books")
async def request_book():
    return BOOKS