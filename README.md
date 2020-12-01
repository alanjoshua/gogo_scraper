# gogo_scrapper
A simple python goganime scrapper


## Usage
<br />
<br />

```import gogo_scraper as gogo  # import module```
<br />
<br />
<br />

<p> Gets list of Gogoanime search results for the query "naruto" </p>

```search = gogo.search("naruto")```
<br />
<br />
<br />

<p> Get link to naruto episode 10</p>
<p> Here, "naruto" is the exact the anime title/link in Gogoanime. Other anime might have complicated titles, so first use gogo.search() to get exact title</p>

```link = gogo.getEpisode("naruto", 10)```

<br />
<br />
<br />

<p> Get latest episode from naruto </p>
<p> Returns a dictionary {ep_num: 220, link: ...} </p>

<p> This function uses requires selenium with chrome in headless mode, so make sure to have chromedrivers installed and added to system path </p>

```latest_episode = gogo.getLatestEpisode("naruto")```
