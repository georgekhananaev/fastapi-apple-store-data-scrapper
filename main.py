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
        "name": "Single App Requests",
        "description": "Get everything you need in BULK such as hot products",
    },

]

app = FastAPI(title="Apple Store Scrapper",  # noqa
              description=description,
              version="1.0.0",
              terms_of_service="https://github.com/georgekhananaev/fastapi-apple-store-data-scrapper/blob/master/LICENSE",
              openapi_tags=tags_metadata,
              contact={"name": "George Khananaev", "url": "https://george.khananaev.com", "email": "george.khananaev@gmail.com"})

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


@app.get('/app/{app_id}', tags=["Single App Requests"])
async def top_free_apps(app_id: int, country_code: str | None = Query(default="us")):
    """
        Insert "APP ID" such as: 1643890882, the value should be numbers only.
        The country code can be "us, gb, il" or anything else supported by Apple.
       """
    return single_app(url=f"https://apps.apple.com/{country_code}/app/id{app_id}", country_code=country_code)


@app.get('/top100-free-apps', tags=["Top Apps"])
async def top_free_apps():

    # checking if value exist in memory and not older than 1 day before running the fetch.
    if len(top_hundred_free_memory) < 100 and check_date_in_dictionary(top_hundred_free_memory):
        top_100(url="https://apps.apple.com/us/charts/iphone/top-free-apps/36", dict=top_hundred_free_memory)

    return top_hundred_free_memory


@app.get('/top100-paid-apps', tags=["Top Apps"])
async def top_paid_apps():

    # checking if value exist in memory and not older than 1 day before running the fetch.
    if len(top_hundred_paid_memory) < 100 and check_date_in_dictionary(top_hundred_paid_memory):
        top_100(url="https://apps.apple.com/us/charts/iphone/top-paid-apps/36", dict=top_hundred_paid_memory)

    return top_hundred_paid_memory


@app.get('/top100-free-apps-detailed', tags=["Top Apps"])
async def top_free_apps_with_information_for_every_single_app():
    """
             Please note: first run might take several minutes. As it scrapping data for every single APP in this list. Once loaded, cache is generated. Next fetches will be much quicker.
            """
    if len(top_hundred_detailed_free_memory) < 100 and check_date_in_dictionary(top_hundred_detailed_free_memory):
        top_100_detailed(url="https://apps.apple.com/us/charts/iphone/top-free-apps/36",
                         dict=top_hundred_detailed_free_memory)
    return top_hundred_detailed_free_memory


@app.get('/top100-paid-apps-detailed', tags=["Top Apps"])
async def top_paid_apps_with_information_for_every_single_app():
    """
             Please note: first run might take several minutes. As it scrapping data for every single APP in this list. Once loaded, cache is generated. Next fetches will be much quicker.
            """

    if len(top_hundred_detailed_paid_memory) < 100 and check_date_in_dictionary(top_hundred_detailed_paid_memory):
        top_100_detailed(url="https://apps.apple.com/us/charts/iphone/top-paid-apps/36",
                         dict=top_hundred_detailed_paid_memory)
    return top_hundred_detailed_paid_memory


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
