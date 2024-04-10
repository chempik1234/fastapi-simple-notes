from fastapi import FastAPI
from api.routes.routes_note import router as note_router
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
app.include_router(note_router)
# app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
