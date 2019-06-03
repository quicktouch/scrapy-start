import scrapy

class QuotesSpider(scrapy.Spider):
    # 标识Spider。 它在项目中必须是唯一的，也就是说，不能为不同的Spider设置相同的名称。
    name = "quotes"

    #必须提供一个Spider开始抓取的迭代请求（你可以返回一个请求列表或者编写一个生成器函数）。 
    # 随后的请求将从这些初始请求中接连生成。
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    #一个用来处理每个请求下载的响应的方法。 
    # response参数是TextResponse的一个实例，它包含了页面内容以便进一步处理。
    def parse(self, response):
        #通常会解析response，将抓到的数据提取为字典，同时找出接下来新的URL创建新的请求（Request）。

        # 存储到本地
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename) 

        #存储为json
        for quote in response.css('div.quote'):
            yield {
                #用法与选择器一致
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }            
        # #跳转到第二页继续进行解析,这里有三种方式,选择一种即可
        # #方式1. 拼接url
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:            
        #     #使用urljoin()方法构建完整的绝对URL（因为链接可以是相对的）
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # #方式2. 调用follow访问相对路径
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:                         
            #response.follow直接支持相对URL - 无需调用urljoin。 
            # 请注意，response.follow只是返回一个Request实例；你仍然需要产生这个请求
            yield response.follow(next_page, callback=self.parse)

        #方式3 对于<a>元素有一个快捷方式：response.follow会自动使用它们的href属性。 因此代码可以进一步缩短：
        # for a in response.css('li.next a'):
        #     # print(a)
        #     yield response.follow(a, callback=self.parse)