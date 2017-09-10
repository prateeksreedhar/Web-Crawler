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
                self.log("hh")
                self.log(url)
                yield response.follow(url, callback=self.parse_post_pages)

    def organize_posts(self, list_of_posts):
        i  = 0
        j = i+1
        clist = []
        while i < len(list_of_posts):
           temp = ""
           while j < len(list_of_posts):
               if '\n' in list_of_posts[j]:
                   temp += list_of_posts[j]
                   j += 1
               else:
                   break
           clist.append(list_of_posts[i]+temp)
           i = j
           j = i+1
        return clist

    def parse_post_pages(self, response): 
        self.log("------------------------")
        user_list = response.xpath('//td[@class="post-name"]/a[contains(@title, "view")]/text()').extract()
        posts_list_in_one_page = response.xpath('//td[@class="post-content"]/text()').extract()
        posts_list_in_one_page_organized = self.organize_posts(posts_list_in_one_page)
        post_upvotes = response.xpath('//div[@class="postModerateSpan"]/span/span/text()').extract()
        user_upvotes = response.xpath('//div[@class="postModpointsWrapper"]/a[@class="postModpoints"]/text()').extract()
        time_stamps = response.xpath('//td[@class="post-date"]/span/@title').extract()
        #self.log("posttttttttt"+str(posts_list_in_one_page_organized))
        #self.log(str(len(user_list))+" "+str(len(posts_list_in_one_page_organized))+ " "+str(len(post_upvotes))+" "+str(len(user_upvotes))+" "+str(len(time_stamps)))
        for post_number, each_user,his_post,post_upvote,user_upvote,time_stamp in zip(post_numbers, user_list, posts_list_in_one_page_organized,post_upvotes, user_upvotes, time_stamps):
            yield{
                #'POST-NUMBER' : post_number,
                'USER' : each_user,
                'POST' : his_post,
                'POST-UPVOTES' : post_upvote,
                'USER-UPVOTES' : user_upvote,
                'TIME-STAMPS' : time_stamp,
            }
        prev_page_link = response.xpath('//a[@class="link-thread-left"]/@href').extract()
        if len(prev_page_link) > 0: 
            yield response.follow(prev_page_link[0],callback=self.parse_post_pages)

if __name__ == "__main__":
    spider = ElementSpider()