import gogo_scraper as gogo

# Gets list of Gogoanime search results for the query "naruto"
search = gogo.search("naruto")

# Get link to naruto episode 10
# Here, "naruto" is the exact the anime title/link in Gogoanime. Other anime might have complicated titles, so first use
# gogo.search() to get exact title

link = gogo.getEpisode("naruto", 10)

# Get latest episode from naruto
# Return a dictionary {ep_num: 220, link: ...}
latest_episode = gogo.getLatestEpisode("naruto")