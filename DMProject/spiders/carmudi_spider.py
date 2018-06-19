import scrapy
import json


class CarmudiSpider(scrapy.Spider):
    name = "vehicles"

    url_prefix = "https://www.carmudi.lk/all/distance:30km/?sort=suggested&page="

    start_urls = []

    for i in range(1, 50):
        start_urls.append(url_prefix + str(i))

    def parse(self, response):
        print("parsing")
        for href in response.css(
                "div.catalog-listing-description-data h3.item-title a::attr(href)"):
            print(href)
            yield response.follow(href, self.parse_item)

    def parse_item(self, response):
        data = {}

        data["seller"] = response.xpath("//*[@id=\"seller-details\"]/div[1]/p/strong/text()").extract_first()
        data["type"] = response.xpath("//*[@id=\"seller-details\"]/ul/li/text()").extract_first()
        data["address"] = response.xpath("//*[@id=\"addressBlock\"]/address/text()").extract_first()
        data["name"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[1]/span/text()").extract_first()
        data["price"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[2]/div[1]/div/text()").extract_first()
        data["millage"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[4]/div/div[1]/span/text()").extract_first()
        data["transmission"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[4]/div/div[2]/span/text()").extract_first()
        data["fuel"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[4]/div/div[3]/span/text()").extract_first()
        data["capacity"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[1]/div[4]/div/div[4]/span/text()").extract_first()
        data["description"] = response.xpath(
            "/html/body/div[2]/main/div[1]/section[1]/section/div[2]/div[2]/div[2]/p/text()").extract_first()

        for key, value in data.items():
            if value is not None:
                data[key] = value.strip('\n').strip('\t'.strip(' '))

        file_name = response.url.split("/")[-1][:-5]

        with open("data/" + file_name + ".json", "w+") as outfile:
            json.dump(data, outfile,
                      indent=2,
                      sort_keys=True)

        yield data
