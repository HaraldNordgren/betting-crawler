import database
import logging
import re
import scrapy
from scrapy.selector import Selector

logging.getLogger('scrapy').setLevel(logging.WARNING)


class QuotesSpider(scrapy.Spider):
    name = "betwaySpider"
    start_urls = [
        "https://sports.betway.com/se?u=/types/3466397537+485674815+1725672712+3268826934+1360997+3507086274+3704679353+3078022958+2870643102+1524192404+1843621643+729817025+4055737068+1820518234+1802141606+1458319990+366154464+1423887585+3102040550+569127004+2746096394+3674556069+3026886452+761515662+813669588+2603733622+2592227149+3602800179+1904582849+3031711876+930117341+338310381+1400761215+3999403102+3328173141+429341966+1087056776+2782025423+3287197706+963501417+1881534845+2669591541+818093756+2152014868+3390411067+3525448603+2663891652+2775370273+2726698235+4037689422+1346358958+2477406238+1048302583+2008947264+2090991074+3137633102+3009078487+2029342244+324223667+3967268438+3036977201+3664293364+3936237159+1760968083+2142016243+568953445+1355916803",
        "https://sports.betway.com/se?u=/soccer/panama/liga-de-ascenso",
    ]

    match_regex = '([0-9:]+).*\+[0-9]+ (.*) - (.*) ([0-9.]+) ([0-9.]+) ([0-9.]+)'

    db = database.match_database()

    def parse(self, response):
        matchodds = False
        date = None

        sel = Selector(response)
        oddsbrowser = sel.xpath("//table[@class='odds-browser']")

        # TODO: get competition

        for tr in oddsbrowser.xpath("tbody/tr"):
            element_class = tr.xpath("@class").extract_first()
            if element_class == 'header ':
                header = tr.xpath("th/text()")[0].extract()
                matchodds = (header == 'Matchodds')
                continue

            if not matchodds:
                continue
            if element_class == 'date':
                # TODO: Extract match date
                date = tr.xpath(".//text()").extract_first()
                continue

            # Ignore if match is already in progress
            style = tr.xpath("./td")[0].xpath("./div/@style")
            if style.extract_first().split(";")[1].split(":")[0] != 'color':
                continue

            text = " ".join(tr.xpath(".//text()").extract())
            m = re.match(self.match_regex, text)
            if m is None:
                continue

            self.db.process_match(
                comp="(Unknown)",
                home_team=m.group(2),
                away_team=m.group(3),
                sql_date=date,
                clock_time=m.group(1),
                site='Betway',
                odds={
                    '1': m.group(4),
                    'X': m.group(5),
                    '2': m.group(6),
                },
            )

            yield {'match': {
                'date': date,
                'time': m.group(1),
                'home': m.group(2),
                'away': m.group(3),
                '1': m.group(4),
                'X': m.group(5),
                '2': m.group(6),
            }}
