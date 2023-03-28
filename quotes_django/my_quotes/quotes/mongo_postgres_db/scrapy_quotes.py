import json

import scrapy
from scrapy.crawler import CrawlerProcess

from .connect_by_mongo import connect
from .models_mongo import Author, Quote


class FindAuthorsQuotes(scrapy.Spider):
    
    name = "find_authors_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    links_for_authors = set()
    authors = []
    quotes = []
    find_all_links_for_authors = False
        
    def parse(self, response):
        
        next_page = ""
        
        if not self.find_all_links_for_authors:
            
            for quote in response.xpath("/html//div[@class='quote']"):
                self.quotes.append({
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small[@class='author']/text()").get(),
                    "quote": quote.xpath("span[@class='text']/text()").get().strip()
                })
            
            links = response.xpath("//div[@class='quote']/span/a/@href").extract()
            
            [self.links_for_authors.add(self.start_urls[0]+link) for link in links]
            
            next_page = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_page:
            yield scrapy.Request(url=self.start_urls[0]+next_page)
            
        else:
            
            self.find_all_links_for_authors = True
            
            for link_for_author in self.links_for_authors:
                yield scrapy.Request(url=link_for_author)                
                
            author = response.xpath("//h3[@class='author-title']/text()").get()
            
            if author:
                self.authors.append({
                    "fullname": author.strip(),
                    "born_date": response.xpath("//span[@class='author-born-date']/text()").get(),
                    "born_location": response.xpath("//span[@class='author-born-location']/text()").get(),
                    "description": response.xpath("//div[@class='author-description']/text()").get().strip()
                })
                
                
def save_file(name_file: str, list_to_save: list):
    
    with open(name_file+".json", "w") as file:
        json.dump(list_to_save, file)
     

def load_json_file(file: str):    

    with open(file, "r") as fd:
        return json.load(fd)  
       
        
def save_to_mongo():
    
    authors = load_json_file("authors.json") 
    
    [Author(**author).save() for author in authors]
        
    quotes = load_json_file("quotes.json")
    
    for quote in quotes:        
        
        qoute_author = quote.get("author")        
        author_obj = Author.objects(fullname=qoute_author).first()      
        quote["author"] = author_obj
        
        Quote(**quote).save()
        

def main_scrapy():
    
    
    process = CrawlerProcess()
    process.crawl(FindAuthorsQuotes)
    
    process.start()
    process.join()
    
    save_file("authors", FindAuthorsQuotes.authors)    
    save_file("quotes", FindAuthorsQuotes.quotes)    
    save_to_mongo()
        
 
if __name__ == "__main__":    
    main_scrapy()
