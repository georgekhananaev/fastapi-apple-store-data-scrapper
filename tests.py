from components.dataBuilder import *

# raw scrapper data test
print(scrapper("https://apps.apple.com/us/charts/iphone/top-paid-apps/36"))

# top 100 free elements test
top_100_detailed(url="https://apps.apple.com/us/charts/iphone/top-paid-apps/36", dict=top_hundred_detailed_free_memory)
print([i for i in top_hundred_detailed_free_memory])

# single product test
print(single_app(url="https://apps.apple.com/us/app/id317809458", country_code="us"))

# print local memory to see what is keeping.
print(top_hundred_free_memory)
print(top_hundred_paid_memory)
print(top_hundred_detailed_free_memory)
print(top_hundred_detailed_paid_memory)


# for more deep tests you can remove local cache files.
