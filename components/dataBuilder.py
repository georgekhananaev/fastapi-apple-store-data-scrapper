from components.webScrapper import scrapper
from components.supportFunctions import *


# fetching single app, will keep app in cache to avoid similar requests to apple server
def single_app(**kwargs) -> list or dict:
    app_id = kwargs["url"].partition("id")[2]
    country = kwargs["country_code"]
    cache_file = f"./cache/apps/{app_id}{country}.json"

    # loading local file as cache if exist
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            data = json.load(f)
            print('local file was loaded')

            # after using the file will check if the file is older than 30 days. if yes then removing it.
            # the next time the end user will use the API it will be regenerated with new data.
            if check_if_expired(cache_file):
                os.remove(cache_file)

            # data output, to api
            return data

    else:
        try:
            results = scrapper(kwargs["url"]).find("dl",
                                                   class_="information-list information-list--app medium-columns l-row")
            job_elements = results.find_all("div",
                                            class_="information-list__item l-column small-12 medium-6 large-4 small-valign-top")

            # creating json format from the fetched data for the API
            scrapped_data = [Convert(" ".join(i.text.split()).split(" ", 1)) for i in job_elements]

            # peer39 request, to find the type of the app. for example if this is app for TV, music or game.
            def type_of_the_app() -> str:
                if find_if_value_exist("tv", scrapped_data[3]) and find_if_value_exist("entertainment",
                                                                                       scrapped_data[2]):
                    return "TV"
                elif find_if_value_exist("music", scrapped_data[2]):
                    return "Music"

                elif find_if_value_exist("game", scrapped_data[2]):
                    return "Game"
                else:
                    return "Other"

            # peer39 request, if this is kids friendly or not.
            def kids_friendly() -> str:
                try:
                    age_criteria = str(scrapped_data[5].values()).split()
                    age_as_int = int(age_criteria[1][:1])
                    if age_as_int <= 12 and len(age_criteria) < 3:
                        return "Yes"
                    else:
                        return "No"
                except Exception as Er:
                    print(Er)
                    return "Unknown, check the age criteria"

            # modified data that should be returned to API.
            app_data = [{"id": app_id}, {"KidsFriendly": kids_friendly()}, {"Type": type_of_the_app()},
                        {"url": kwargs["url"]},
                        {"scrappedData": scrapped_data}]

            # save to cache file if not empty.
            if len(app_data) > 2:
                cache_file = cache_file
                with open(cache_file, "w") as outfile:
                    json.dump(app_data, outfile)
            else:
                raise Exception("The data is empty, error will be thrown")
            # new fetched data output to API
            return app_data

        # handing exception
        except Exception as Err:
            print(Err)  # print the error to console
            return {
                "Error": "Data returned empty from origin server"}  # throw the error to API interface instead of returning empty array


# this function receiving parameters from-outside and building dictionaries from it without return value.
def top_100(**kwargs) -> None:
    filename = "top_free" if top_hundred_free_memory is kwargs["dict"] else "top_paid"
    cache_file = f"./cache/top100/{filename}.json"

    try:
        results = scrapper(kwargs["url"]).find(id="charts-content-section")

        # will find classes with the input below
        job_elements = results.find_all("li",
                                        class_="l-column--grid small-valign-top we-lockup--in-app-shelf l-column small-6 medium-3 large-2")

        # looping the HTML code from the fetched URL
        for i in job_elements:
            # removing all spaces, separating text
            without_spaces = " ".join(i.text.split()).split(" ", 1)

            # updating selected dictionary
            kwargs["dict"].update({without_spaces[0]: {without_spaces[1]: i.select_one('a')['href']}})

        # handling cache files, if error above it will be skipped.
        with open(cache_file, "w") as outfile:
            json.dump(kwargs["dict"], outfile)
            print(f"new {filename} cache file is saved")

            # insert update date into dictionary
            kwargs["dict"].update({"LastUpdate": now})
            print("Insert update time")

    # handing exception
    except Exception as Err:
        # throw the error to API interface instead of returning empty array
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                kwargs["dict"].update(data)
                print('Due to an error, cache file been loaded')

        else:
            # throw the error to API interface instead of returning empty array
            kwargs["dict"].update({"Error": "Remote server returned error, try again"})
        print(Err)  # print the error to console


# scanning every single product in top100 list and building cache data from it.
# this function basically is a clone of the function above with minor changes. Can make the code shorter by migrating these.
def top_100_detailed(**kwargs) -> None:
    filename = "top_free_detailed" if top_hundred_detailed_free_memory is kwargs["dict"] else "top_paid_detailed"
    cache_file = f"./cache/top100/{filename}.json"

    try:
        results = scrapper(kwargs["url"]).find(id="charts-content-section")

        # will find classes with the input below
        job_elements = results.find_all("li",
                                        class_="l-column--grid small-valign-top we-lockup--in-app-shelf l-column small-6 medium-3 large-2")

        # looping the HTML code from the fetched URL
        for i in job_elements:
            # removing all spaces, separating text
            without_spaces = " ".join(i.text.split()).split(" ", 1)

            # updating selected dictionary
            kwargs["dict"].update({without_spaces[0]: [{without_spaces[1]: i.select_one('a')['href']},
                                                       single_app(url=f"{i.select_one('a')['href']}",
                                                                  country_code="us")]})

        # handling cache files, if error above it will be skipped.
        with open(cache_file, "w") as outfile:
            json.dump(kwargs["dict"], outfile)
            print("new cache file created")

            # insert update date into dictionary
            kwargs["dict"].update({"LastUpdate": now})
            print("Insert update time")

    # handing exception
    except Exception as Err:
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                # if error, it will try to load cache file.
                data = json.load(f)
                kwargs["dict"].update(data)
                print('Due to an error, cache file been loaded')
        else:
            # throw the error to API interface instead of returning empty array
            kwargs["dict"].update({"Error": "Remote server returned error, try again"})
        print(Err)  # print the error to console
