from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from .database import engine
from .models import Base
from .routers import admin, auth, todos, users

app = FastAPI()

#kresne automatski kad pokrenemo app, iz database i modela uzima šta treba i napravi DB file, ako DB file postoji
# onda se funkcije ne pokreće
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="ToDoApp/templates")

#test endpoint
@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(request, "home.html", {"request": request})

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
