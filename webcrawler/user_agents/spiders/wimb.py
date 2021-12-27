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
        wanted_os: List = None,
        wanted_softwares: List = None,
        pages: int = 10,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.wanted_os = wanted_os
        self.wanted_softwares = wanted_softwares
        if pages > 10:
            self.logger.warning(
                "The maximum number of pages for user agent lookups is 10."
            )
        self.pages_left = pages

    def _check_desired(self, to_check: str, allowed: List):
        if not allowed:
            return True

        for allowed_str in allowed:
            if allowed_str in to_check.lower():
                return True
        return False

    def parse(self, response: HtmlResponse):
        self.pages_left -= 1

        table_ = response.css(
            ".table.table-striped.table-hover.table-bordered.table-useragents.listing-of-useragents"
        )

        for row_ in table_.css("tr")[1:]:
            cols_ = row_.css("td")
            user_agent_string = cols_[0].css("a::text").get()
            software = cols_[1].css("::text").get()
            os = cols_[2].css("::text").get()
            # layout_engine = cols_[3].css("::text").get()

            if self._check_desired(
                software, self.wanted_softwares
            ) and self._check_desired(os, self.wanted_os):
                yield {"": user_agent_string}

        if self.pages_left > 0:
            # it is simpler to generate the next url like this instead of using a
            # complicated css selector
            url_parts = response.url.split("/")
            current_page = int(url_parts.pop(-1))
            next_page_url = "/".join(url_parts + [str(current_page + 1)])
            yield Request(next_page_url)
