import uvicorn as uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from components.dataBuilder import *

app = FastAPI()


description = '''Top 100 apple store web scrapper with API. Based on Python FastAPI library. This tool was created as a home exercise request from Peer39 for eduction purposes only.'''

tags_metadata = [
    {
        "name": "Top Apps",
        "description": "Get everything you need in BULK such as hot products",
    },
    {
        "name": "Single Request",
        "description": "Get everything you need in BULK such as hot products",
    },


]

app = FastAPI(title="Apple Store Scrapper",  # noqa
              description=description,
              version="1.0.0",
              terms_of_service="https://github.com/georgekhananaev/aliexpress-open-api/blob/main/LICENSE",
              openapi_tags=tags_metadata,
              contact={
                  "name": "George Khananaev",
                  "url": "https://george.khananaev.com", "email": "george.khananaev@gmail.com",
              },
              # license_info={
              #     "name": "Apache 2.0",
              #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              # },
              )  # disable docs add: docs_url=None

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


@app.get('/app/{app_id}', tags=["Single Request"])
async def top_free_apps(app_id: int, country_code: str | None = Query(default="us")):
    """
        Insert "APP ID" such as: 1643890882, the value should be numbers only.
        The country code can be "us, gb, il" or anything else supported by Apple.
       """
    return single_app(url=f"https://apps.apple.com/{country_code}/app/netflix/id{app_id}", country_code=country_code)


@app.get('/top-free-apps', tags=["Top Apps"])
async def top_free_apps():
    top_100(url="https://apps.apple.com/us/charts/iphone/top-free-apps/36", dict=top_hundred_free_memory)
    return top_hundred_free_memory


@app.get('/top-paid-apps', tags=["Top Apps"])
async def top_paid_apps():
    top_100(url="https://apps.apple.com/us/charts/iphone/top-paid-apps/36", dict=top_hundred_paid_memory)
    return top_hundred_paid_memory


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
