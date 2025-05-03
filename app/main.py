from fastapi import FastAPI
from .import models
from .database import engine
from .routers import posts, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# # we are using alembic to autogenerate the tables from the models defined, so we dont really need this command anymore
models.Base.metadata.create_all(engine) # create all the tables defined in models if they dont exist yet

app = FastAPI()

# a list of domains which are allwed to talk with our api
# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"] # api accessible from any website

app.add_middleware(
    CORSMiddleware, # a function which runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # usually we allow only get requests
    allow_headers=["*"],
)

# # path operation or route
@app.get("/") #decorator using HTTP get method
async def root():  # async keyword performs the tasks asynchrnously (optional)
    return {"message": "Hi this is Adarsh, cool, pushin to ubuntu server"} # python dictionary which is converted to json for handling api calls


app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
  





