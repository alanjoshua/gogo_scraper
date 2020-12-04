import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")

BASE_URL = 'https://gogoanime.so/'  # Change this if this link to gogoanime goes down


def _validifyName_(name):
    """

    Inner method used to clean anime search query

    :param name: Anime search query
    :return: Replaces special characters with '-' to comply with Gogoanime's URL specifications
    """

    # Replace all special characters and get a normalized name where only - is between words, and words in in lowercase
    newName = re.sub(r' +|:+|#+|%+|\?+|\^+|\$+|\(+|\)+|_+|&+|\*+ |\[+ |]+|\\+|{+|}+|\|+|/+|<+|>+|\.+|\'+', "-",
                     name.lower())
    newName = re.sub(r'-+', "-", newName)

    return newName


# Uses selenium with chrome in Headless mode to get last Episode, so make sure
def getLatestEpisode(anime, base_url=BASE_URL):
    """

    Gets the latest episode of the input anime

    :param anime: Exact Gogoanime title/link
    :param base_url: Base Gogoanime URL. Useful if the current default URL gets taken down
    :return: Link and episode number of latest episode, or None if anime or episode was not found
    """
    anime = _validifyName_(anime)
    newUrl = base_url + "category/" + anime

    page_response = requests.get(newUrl)
    page = BeautifulSoup(page_response.content, "html.parser")

    # Extract variables from website to create ajax request
    startEp = page.find('ul', id='episode_page').find('a', class_='active').get('ep_start')
    endEp = page.find('ul', id='episode_page').find('a', class_='active').get('ep_end')
    id = page.find('input', id='movie_id').get('value')
    default_ep = page.find('input', id='default_ep').get('value')
    alias = page.find('input', id='alias_anime').get('value')

    # Create ajax url and load data
    loadEpisode = f'https://ajax.gogocdn.net/ajax/load-list-episode?ep_start={startEp}&ep_end={endEp}&id={id}&default_ep={default_ep}&alias={alias}'
    episodesData = BeautifulSoup(requests.get(loadEpisode).content, "html.parser")

    # Get last episode num from episodeData, and create episode link
    lastEpisode_num = int(episodesData.find('div', class_='name').text.split()[1])
    lastEpisode_link = base_url[:-1] + str(episodesData.find('a').get('href')).strip()

    return {"num": lastEpisode_num, "link": lastEpisode_link}


def getEpisode(anime, re_ep, base_url=BASE_URL):
    """
    Get specific episode of input anime

    :param anime: Exact Gogoanime title/link
    :param re_ep: Specific episode number of the anime to retrieve
    :param base_url: Base Gogoanime URL. Useful if the current default URL gets taken down
    :return: Link to requested episode, or None if episode or anime is not found
    """
    anime = _validifyName_(anime)
    episodeUrl = base_url + anime + '-episode-' + str(re_ep)
    page_response = requests.get(episodeUrl)
    master_page = BeautifulSoup(page_response.content, "html.parser")

    try:
        master_page.find('h1', class_='entry-title').text
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

    anime = _validifyName_(anime)
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
        info['gogoTitle'] = info['link'][info['link'].find('category') + 9:]
        res.append(info)

    return res