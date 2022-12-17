import requests
from bs4 import BeautifulSoup
from retrying import retry


# Specify an exception you need. or just True"""
def retry_if_connection_error(exception) -> bool:

    # return True
    return isinstance(exception, ConnectionError)


# if exception retry with 3 second wait
@retry(retry_on_exception=retry_if_connection_error, wait_fixed=3000)
def safe_request(url, headers, **kwargs) -> object:
    return requests.get(url, headers, **kwargs)


# # In case if you need to scrap free proxies and to test them before using, can use this multi-thread functions.
# # I created most of it, but this is too much work messing with free proxy servers. I decided to leave it as it for now, there also some risks involved using free proxies.
#
# from lxml.html import fromstring
# from itertools import cycle
# import concurrent.futures
# import random
#
# def get_proxies():
#     free_proxy_url = 'https://free-proxy-list.net/'
#     response = requests.get(free_proxy_url)
#     parser = fromstring(response.text)
#     set_proxies = set()
#     for i in parser.xpath('//tbody/tr')[:100]:
#         if i.xpath('.//td[7][contains(text(),"yes")]'):
#             # Grabbing IP and corresponding PORT
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             set_proxies.add(proxy)
#
#     return set_proxies
#
#
# proxies = get_proxies()
# proxy_pool = cycle(proxies)
# my_ip = 'https://httpbin.org/ip'
#
# good_proxies = []
#
#
# def check_if_good_proxy(proxy):
#     try:
#         response = requests.get(my_ip, proxies={"http": proxy, "https": proxy})
#         # good_proxies.append(response.json()['origin'])
#         print(response.json())
#         good_proxies.append(proxy)
#
#         print(len(good_proxies))
#         if len(good_proxies) > 10:
#             exit()
#     except:
#         # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
#         # We will just skip retries as it's beyond the scope of this tutorial, and we are only downloading a single url
#         print("Skipping. Connection error")
#
#
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = executor.map(check_if_good_proxy, proxies)

# default proxies list

select_proxies = {
    "https": '34.175.45.228:3128',
    "SOCKS5": '173.212.195.109:3481'
}


# main scrapper
def scrapper(*args):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    url = args[0]
    try:
        # timeout for proxy is 2 seconds
        # req = requests.get(url, headers, proxies=select_proxies, timeout=5)
        req = safe_request(url, headers, proxies=select_proxies, timeout=5)
    except Exception as Err:
        # if failed to use proxy, will try to connect with local IP
        print(f"Proxy servers is down, Error: {Err}, local host IP being used")
        try:
            # trying to connect with from local host if timeout.
            req = requests.get(url, headers)

        except Exception as Err:
            print("Failed to connect to remote server", Err)

    response = BeautifulSoup(req.content, 'html.parser')

    return response
