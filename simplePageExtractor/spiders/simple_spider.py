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
        base_url = 'http://forum.nafc.org/'
        url_list = response.xpath('//a[contains(@href, "topic")]/@href').extract()
        
        for url in url_list:
            split_url = url.split('/')
            if split_url[2] != 'page':
                self.log("hh")
                self.log(url)
                yield response.follow(url, callback=self.parse_post_pages)

    def parse_post_pages(self, response): 
        self.log("------------------------")
        #xxx = response.xpath('//td[@class="post-content"]/text()').extract()
        #self.log(response.xpath('//td[@class="post-content"]/text()').extract())
        #self.log(response.xpath('//td[@class="post-name"]/a[contains(@title, "view")]/text()').extract())
        #self.log(response.xpath('//td[@class="post-content"]/text()').extract())
        user_list = response.xpath('//td[@class="post-name"]/a[contains(@title, "view")]/text()').extract()
        posts_list_in_one_page = response.xpath('//td[@class="post-content"]/text()').extract()
        for each_user,his_post in zip(user_list, posts_list_in_one_page):
            yield{
                'USER' : each_user,
                'POST' : his_post,
            }
        prev_page_link = response.xpath('//a[@class="link-thread-left"]/@href').extract()
        if len(prev_page_link) > 0: 
            yield response.follow(prev_page_link[0],callback=self.parse_post_pages)
            #self.log(prev_page_link)
        #page_list = response.xpath('//div[contains(@class,"link-thread-right")]/@href').extract()
        #self.log(response.body)
        '''self.log("in parse_data")
        url_list = response.xpath('//a[contains(@href, "topic")]/@href').extract()
        for urls in url_list
        hxs = HtmlXPathSelector(response.body)
        filename = 'responses3.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            #f.write(response.body.selector.xpath('//a[contains(@href, "topic")]@href').extract())
            #f.write(response.xpath('//a').extract())
        self.log('Saved file' + filename)
        #self.log("td is" + str(response.css('td.title')))
        #for title in response.css('td.title'):'''



if __name__ == "__main__":
    spider = ElementSpider()