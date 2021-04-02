import bs4
from bs4 import BeautifulSoup
import requests
import re
import urllib
import pprint

def github_api  (search_term, num_pages=1):
    """Scrapes github repos from the given search term

    Args:
        search_term (str): The search term for the github repo
        num_pages (int, optional): The number of pages required to query for repos. Defaults to 1.

    Returns:
        list: A list of dictionaries containing the required infos
    """

    prep_search = search_term.replace(" ","+") 
    page = "https://api.github.com/search/repositories?q=" + str(prep_search) + "in:name+in:description&per_page=" + str(10*num_pages) + "&page=1"
    response = requests.get(str(page))
    response_json = response.json()

    repos = response_json['items']
    scraped_info = []

    for repo in repos:
        scraped_info.append(extract_API(repo))

    return scraped_info

def extract_API(repository):
    repo_dict = {}
    
    repo_dict["Name"] = repository['full_name']
    repo_dict["Description"] = repository['description']
    repo_dict["Stars"] = repository['stargazers_count']
    repo_dict["Language"] = repository['language']
    repo_dict["Last Update"] = repository['updated_at']
    repo_dict["Issues"] = repository['has_issues']
    
    if not (repository['license'] == None):
        repo_dict["License"] = repository['license']['name']
    else:
        repo_dict["License"] = None
    
    return repo_dict

def scrape_github (search_term, num_pages = 1):
    """Scrapes github repos from the given search term

    Args:
        search_term (str): The search term for the github repo
        num_pages (int, optional): The number of pages required to query for repos. Defaults to 1.

    Returns:
        list: A list of dictionaries containing necessary infos from scraped repos.
    """
    prep_search = search_term.replace(" ","+") 
    page = "https://github.com/search?q=" + str(prep_search)
    response= requests.get(str(page))
    soup = BeautifulSoup(response.content,"html.parser")

    results = soup.findAll("li",class_=re.compile("repo-list-item"))

    scraped_info = []

    for result in results:
        scraped_info.append(extract_Scraper(result))

    return scraped_info


def extract_Scraper(search_result):
    result_dict = {}

    extractor("Name", search_result.find("a", class_="v-align-middle"), result_dict)
    extractor("Description", search_result.find('p', class_="mb-1"), result_dict)
    extractor("Stars", search_result.find("a", class_="Link--muted"), result_dict)
    extractor("Language", search_result.find("span", itemprop="programmingLanguage"), result_dict)
    extractor("Last Update", search_result.find("relative-time"), result_dict)
    extractor("Issues", search_result.find("a", class_="Link--muted f6"), result_dict)
    extractor("License", search_result.findAll("div", class_="mr-3"), result_dict)
    extractor("Tags", search_result.findAll("a", class_=re.compile("topic-tag")), result_dict)

    return result_dict
 

def extractor (category, tags, diction):
    if category == "License":
        result = None
        if tags != None:
            for tag in tags:
                if "license" in tag.text:
                    result = tag            
                    break
        util_extractor(category, result, diction)

    elif category == "Tags":
        if len(tags) == 0:
            util_extractor(category,None,diction)
        else:
            tag_list = []
            for tag in tags:
                raw = tag.text
                result = " ".join(raw.split()).encode("ascii", "ignore")
                tag_list.append(result)
            diction[category] = tag_list
    
    else:
        util_extractor(category, tags, diction)

def util_extractor (category, find_tag, diction):
    if find_tag == None:
        result = None
    else:
        raw = find_tag.text
        result = " ".join(raw.split()).encode("ascii", "ignore")

    diction[category] = result

    return result