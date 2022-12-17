from components.webScrapper import scrapper
from components.dataBuilder import *


print(single_app(url="https://apps.apple.com/us/app/netflix/id363590051"))

top_hundred_free_memory = {}


def top_100_free_builder_test():
    try:
        results = scrapper("https://apps.apple.com/us/charts/iphone/top-free-apps/36").find(id="charts-content-section")

        # print(results)

        job_elements = results.find_all("li",
                                        class_="l-column--grid small-valign-top we-lockup--in-app-shelf l-column small-6 medium-3 large-2")
        # print(job_elements)

        zero = 0

        for i in job_elements:
            without_spaces = " ".join(i.text.split()).split(" ", 1)
            zero += 1
            top_hundred_free_memory.update({zero: {without_spaces[1]: i.select_one('a')['href']}})

        # for line in results.find_all('a'):
        #     print(line.get('href'))

    except Exception as Err:
        print(Err)


# run top_100_free_builder_test()
top_100_free_builder_test()
print(top_hundred_free_memory)

# print
# print(top_hundred_free_memory)

# # soup = BeautifulSoup(page.content, "html.parser")
# #
# # results = soup.find(id="charts-section")


# URL = "https://apps.apple.com/us/charts/iphone/top-free-apps/36"
# page = requests.get(URL)
# session = re.Session()
#
#
# container = page.find_all(["h2", "h3"],
#                           class_=lambda x: x != 'hidden')
# for lines in container:
#     if lines.name == 'h2':
#         province = lines.text
#         print('In', province, "\n")
#     if lines.name == 'h3':
#         foundation = lines.text
#         print('Foundation name:', foundation)
#         print('Foundation url:', lines.find_all("a", href=re.compile("cfc_locations"))[0].get('href'), "\n")
#
# # soup = BeautifulSoup(page.content, "html.parser")
# #
# # results = soup.find(id="charts-section")
# #
# # # print(soup)
# # print(results.prettify())
# # #
# # # job_elements = results.find_all("div", class_="card-content")
# # #
# #
# # for job_element in job_elements:
# #     title_element = job_element.find("h2", class_="title")
# #     company_element = job_element.find("h3", class_="company")
# #     location_element = job_element.find("p", class_="location")
# #     print(title_element.text)
# #     print(company_element.text)
# #     print(location_element.text)
# #     print()
