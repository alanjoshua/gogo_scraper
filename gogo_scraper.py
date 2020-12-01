import requests
from bs4 import BeautifulSoup
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

BASE_URL = 'https://gogoanime.so/'  # Change this if this link to gogoanime goes down


def __validifyName__(name):
    """

    Inner method used to clean anime search query

    :param name: Anime search query
    :return: Removes white space and adds '-' to better comply with Gogoanime URL specification
    """
    if len(name.split()) > 0:
        name = str(name).lower()
        newName = str(name).replace(' ', '-')
        newName = newName.replace(":", '-')
        newName = newName.replace("--", '-')
    return newName


# Uses selenium with chrome in Headless mode to get last Episode, so make sure
def getLatestEpisode(anime, base_url=BASE_URL):
    """

    Gets the latest episode of the input anime

    This function uses selenium with Chrome in headless mode, so make sure to have chromedriver be installed and added
    to system Path, and have Chrome installed

    :param anime: Exact Gogoanime title/link
    :param base_url: Base Gogoanime URL. Useful if the current default URL gets taken down
    :return: Link and episode number of latest episode, or None if anime or episode was not found
    """
    anime = __validifyName__(anime)
    print(anime)
    newUrl = base_url + "category/" + anime

    driver = webdriver.Chrome(options=options)
    driver.get(newUrl)

    try:
        episodes_list = driver.find_element_by_css_selector("ul[id='episode_related']")
        lastEpisode = episodes_list.find_element_by_css_selector("a")
        lastEpisode_num = int(lastEpisode.find_element_by_class_name("name").text.split()[1])
        lastEpisode_num_part_link = lastEpisode.get_attribute("href")
        lastEpisode_link = lastEpisode_num_part_link
    except:
        driver.close()
        return None

    driver.quit()
    return {"num": lastEpisode_num, "link": lastEpisode_link}


def getEpisode(anime, re_ep, base_url=BASE_URL):
    """
    Get specific episode of input anime

    :param anime: Exact Gogoanime title/link
    :param re_ep: Specific episode number of the anime to retrieve
    :param base_url: Base Gogoanime URL. Useful if the current default URL gets taken down
    :return: Link to requested episode, or None if episode or anime is not found
    """
    anime = __validifyName__(anime)
    episodeUrl = base_url + anime + '-episode-' + str(re_ep)
    page_response = requests.get(episodeUrl)
    master_page = BeautifulSoup(page_response.content, "html.parser")

    try:
        master_page.find('h1', class_='entry-title').text
        print('episode not found')
        return None
    except:
        return episodeUrl


def search(anime, base_url=BASE_URL):
    """
    Uses Gogoanime's (limited) search functionality to find the exact anime or anime the user wants to get info about.
    This is required because the other functions in this bot require the user to input the exact title used in Gogoanime.

    :param anime: Search query
    :param base_url: Base Gogoanime URL. Useful if the current default URL gets taken down
    :return: List of search results
    """

    anime = __validifyName__(anime)
    searchUrl = base_url + '/search.html?keyword='+anime

    page_response = requests.get(searchUrl)
    page = BeautifulSoup(page_response.content, "html.parser")

    items = page.find('div', class_='last_episodes').findAll('li')
    res = []

    for item in items:
        info = {}
        info['name'] = item.find('p', class_='name').find('a').text
        info['link'] = base_url + item.find('p', class_='name').find('a').get('href')
        info['released'] = item.find('p', class_='released').text.strip()
        res.append(info)

    return res