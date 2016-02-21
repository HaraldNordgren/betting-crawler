#!/usr/bin/env python3

import splinter, time

br = splinter.Browser('chrome')

br.visit("https://sports.betway.com/se#/types/1725672712+3268826934+1360997+3507086274+3704679353+3078022958+2870643102+1524192404+1843621643+729817025+4055737068+1820518234+1802141606")

oddsbrowsers = br.find_by_xpath("//table[@class='odds-browser']")
trs = oddsbrowsers[0].find_by_xpath(".//tr")

market_title = trs[4].find_by_xpath("./td[@class='market_title']")

market_title.find_by_xpath("./a")['text']
