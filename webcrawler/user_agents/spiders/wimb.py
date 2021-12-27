from typing import List
import scrapy
from scrapy.http import HtmlResponse, Request


class WimbSpider(scrapy.Spider):
    name = "wimb"
    start_urls = [
        "https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1"
    ]

    def __init__(
        self,
        wanted_oss: List = None,
        wanted_softwares: List = None,
        pages: int = 10,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.wanted_oss = wanted_oss
        if self.wanted_oss is not None:
            self.wanted_oss = self.wanted_oss.lower().strip().split(",")
        self.wanted_softwares = wanted_softwares
        if self.wanted_softwares is not None:
            self.wanted_softwares = self.wanted_softwares.lower().strip().split(",")

        self.pages_left = int(pages)
        if self.pages_left > 10:
            self.logger.warning(
                f"The maximum number of pages for user agent lookups is 10. You provided {self.pages_left}."
            )

    def parse(self, response: HtmlResponse):
        self.pages_left -= 1

        table_ = response.css(
            ".table.table-striped.table-hover.table-bordered.table-useragents.listing-of-useragents"
        )

        for row_ in table_.css("tr")[1:]:
            cols_ = row_.css("td")
            user_agent_string = cols_[0].css("a::text").get()
            software = cols_[1].css("::text").get().strip().lower()
            os = cols_[2].css("::text").get().strip().lower()
            # layout_engine = cols_[3].css("::text").get()

            wanted = True
            if self.wanted_softwares:
                wanted = software in self.wanted_softwares
            if self.wanted_oss:
                wanted = os in self.wanted_oss

            if wanted:
                yield {
                    "software": software,
                    "os": os,
                    "user_agent_string": user_agent_string,
                }

        if self.pages_left > 0:
            # it is simpler to generate the next url like this instead of using a
            # complicated css selector
            url_parts = response.url.split("/")
            current_page = int(url_parts.pop(-1))
            next_page_url = "/".join(url_parts + [str(current_page + 1)])
            yield Request(next_page_url)
