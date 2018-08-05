from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from unidecode import unidecode

index_url = 'https://en.wikipedia.org/wiki/Category:Endemic_fauna_by_country'
# opening up connection grabbing the page
countries_url = uReq(index_url)
# offload content into variable
page_html = countries_url.read()
# close connection
countries_url.close()
# html parsing
page_soup = soup(page_html, "html.parser")

country_table = page_soup.findAll("div", {"class": "CategoryTreeItem"})
countries = country_table[0]

for countries in country_table:
    partial_link = countries.find("a")
    get_country_link = partial_link.get("href")
    full_country_link = "https://en.wikipedia.org" + get_country_link

    country_url = uReq(full_country_link)
    page_html2 = country_url.read()
    country_url.close()
    page_soup2 = soup(page_html2, "html.parser")

    country_name = page_soup2.find("h1", {"id": "firstHeading"})
    country = country_name.text
    species_table = page_soup2.find("div", {"id": "mw-pages"})
    if species_table is not None:
        li = species_table.findAll("li")
        lis = li[0]
        for lis in li:
            a = lis.find("a")
            species = unidecode(a.text)
            print(country + ", " + species)
            filename = "endemicspecies.csv"
            f = open(filename, "a")
            f.write(country + "," + species + "\n")

f.close()
