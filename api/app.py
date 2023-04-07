from fastapi import FastAPI
from pydantic import BaseModel
from assistant import Assistant
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
gpt = Assistant()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SuggestionBody(BaseModel):
    language: str
    source_code: str
    loc: int


@app.get("/")
def home():
    return {"message": "Hello, World!"}


def verify_source_code(source_code: str):
    # TODO: add more conds
    if len(source_code) < 1:
        return False
    return True


@app.post("/get_suggestion")
def get_suggestion(body: SuggestionBody):
    print(body)
    source_code = body.source_code

    if not verify_source_code(source_code):
        return {"message": "Bad Source Code"}

    gpt_response = gpt.write_message(role="user", content=source_code)
    return {"message": gpt_response}
