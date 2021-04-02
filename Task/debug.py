import scraper

#result = scraper.recursive_scrape(search_string = "computer vision")

result = scraper.scrape_github(search_term = "computer vision")

print(result)