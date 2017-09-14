import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.http import FormRequest
from loginform import fill_login_form
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class ElementSpider(scrapy.Spider):
    name = 'simple'
    start_urls = ['http://forum.nafc.org/login/']
    def __init__(self, *args, **kwargs):
                super(ElementSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'registerUserName': 'helloworld123', 'registerPass': 'helloworld123'},
                    callback=self.after_main_login)]

    def after_main_login(self, response):
        '''uuurl = response.xpath('//div[@class="moreThreads"]/a[contains(@onclick,"refresh")]/@href').extract()
        self.log(uuurl)
        if len(uuurl) > 0:
            yield response.follow(uuurl[0], callback=self.after_main_login)
        else:'''
        url_list = response.xpath('//a[contains(@href, "topic")]/@href').extract()
        
        for url in url_list:
            split_url = url.split('/')
            if split_url[2] != 'page':
                # self.log("hh")
                # self.log(url)
                yield response.follow(url, callback=self.parse_post_pages)

    def parse_post_pages(self, response): 
        self.log("------------------------")
        posts_ids = response.xpath('//div[contains(@class, "post-container")]/@id').extract()
        subject = response.xpath('//h1[@class="thread-title-headline left"]/text()').extract()
        for post_id in posts_ids:
            post_container = '//div[contains(@class,"post-container")][@id = "' + post_id
            post_content_in_list = response.xpath( post_container +'"]//tr[2]/td//text()').extract()
            post_content = ''.join(post_content_in_list)
            post_number = response.xpath(post_container + '"]/table[@class="post-table"]//tr[3]/td[@class="post-share"]/text()').extract()
            yield{
                'PAGE_NUMBER_OF_THE_POST' : response.xpath('//div[@class="pages-thread-right"]//text()').extract()[-1],
                'SUBJECT' : subject[0].strip(),
                'POST_NUMBER' : post_number[0][0:8].replace("\x95",""),
                'USER' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-name"]/a[contains(@href, "profile")]/text()').extract()[0],
                'POST' : post_content,
                'POST-UPVOTES' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-moderate"]/div/span/span/text()').extract()[0],
                'USER-UPVOTES' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-avatar"]/div/a[@class="postModpoints"]/text()').extract()[0],
                'TIME-STAMPS' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[3]/td[@class="post-date"]/span/@title').extract()[0],
            }
        prev_page_link = response.xpath('//a[@class="link-thread-left"]/@href').extract()
        if len(prev_page_link) > 0: 
            yield response.follow(prev_page_link[0],callback=self.parse_post_pages)

if __name__ == "__main__":
    spider = ElementSpider()