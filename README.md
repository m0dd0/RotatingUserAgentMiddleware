# RotatingUserAgentMiddleware
Dowloader middleware for scrapy to allow rotating user agent strings.

## Usage
0. Create a scrapy project with `scrapy startproject <project_name>`
1. Copy/Paste the content of `rotatinguseragent.py` (from this repo) into the `middlewares.py` file of your scraper project.
2. In the `settings.py` file of your scraper project add the following lines:
``` 
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "<your_crawler_name>.middlewares.RotatingUserAgentsMiddleware": 500,
}
ROTATING_USER_AGENTS = ["user_agent_1", "user_agent_2", "user_agent_3", "user_agent_4"]
ROTATING_USER_AGENTS_SHUFFLE = False
```

## Settings
With the ROTATING_USER_AGENTS setting you can define the user agents which are rotated.
You can either simply specify a list of user agent strings or you can pass the path
(as pathlib.Path or str) to a file which contains the user agent strings.
The file should contain exactly one user_Agetn per line or shouuld be a json in the
form of [{'os': ..., 'software': ..., 'user_agent_string': ...}, ...].

## Getting user agents
This repository also contains a simple crawler which gets you a list of popular useragents
from `https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1` and the following pages.
You can filter the user agents which are scraped by passing the following arguments:

`wanted_oss`: A list of strings (passed as single string seperated by commas) which the OS column must contain. By default all oss are wanted.

`wanted_softwares`: A list of strings (passed as single string seperated by commas) which the software column must contain. By default all softwares are wanted.

`pages`: The number of pages which are used to get user_agents.

Example: `scrapy crawl wimb -O useragents_sample.json -a wanted_oss=ios,windows -a wanted_softwares=chrome,firefox -a pages=5`

## Related projects
This repo was inspired by the folloeing projects:
https://github.com/scrapedia/scrapy-useragents
https://github.com/rejoiceinhope/crawler-demo/tree/master/crawling-basic/scrapy_user_agents