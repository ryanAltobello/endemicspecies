from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from unidecode import unidecode
"""
index_url = 'https://en.wikipedia.org/wiki/Category:Endemic_birds_by_country'
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

filename = "endemicspecies2.csv"
f = open(filename, "a")

for countries in country_table:
    partial_link = countries.find("a")
    get_country_link = partial_link.get("href")
    full_country_link = "https://en.wikipedia.org" + get_country_link
"""
filename = "endemicspecies2.csv"
f = open(filename, "a")

country_url = uReq('https://en.wikipedia.org/wiki/Category:Telespiza')
page_html2 = country_url.read()
country_url.close()
page_soup2 = soup(page_html2, "html.parser")

country_name = page_soup2.find("h1", {"id": "firstHeading"})
country = country_name.text
species_table = page_soup2.find("div", {"id": "mw-pages"})
count = 0
if species_table is not None:
    li = species_table.findAll("li")
    lis = li[0]
    for lis in li:
        count += 1
        print(count)
        a = lis.find("a")
        species = unidecode(a.text)
        get_species_link = a.get("href")
        full_species_link = "https://en.wikipedia.org" + get_species_link

        species_url = uReq(full_species_link)
        page_html3 = species_url.read()
        species_url.close()
        page_soup3 = soup(page_html3, "html.parser")

        order_td = page_soup3.find("td", text="Order:")
        class_td = page_soup3.find("td", text="Class:")
        phylum_td = page_soup3.find("td", text="Phylum:")
        if order_td is None and class_td is None:
            order_span = page_soup3.find("span", {"class": "order"})
            class_span = page_soup3.find("span", {"class": "class"})
            phylum_span = page_soup3.find("span", {"class": "phylum"})
            if order_span is None and class_span is None:
                print(country + "," + species + "," + "" + "," + "" + "," + "" + "," + full_species_link + "\n")
                f.write(country + "," + species + "," + "" + "," + "" + "," + "" + "," + full_species_link + "\n")
            elif order_span is None and class_span is not None:
                category = class_span.a.get("title")
                supercategory = phylum_span.a.get("title")
                print(country + "," + species + "," + "" + "," + category + "," + supercategory + "," + full_species_link + "\n")
                f.write(country + "," + species + "," + "" + "," + category + "," + supercategory + "," + full_species_link + "\n")
            elif order_span is not None and class_span is not None:
                subcategory = order_span.a.get("title")
                category = class_span.a.get("title")
                print(country + "," + species + "," + subcategory + "," + category + "," + "" + "," + full_species_link)
                f.write(country + "," + species + "," + subcategory + "," + category + "," + "" + "," + full_species_link + "\n")
            else:
                subcategory = order_span.a.get("title")
                supercategory = phylum_span.a.get("title")
                print(country + "," + species + "," + subcategory + "," + "" + "," + supercategory + "," + full_species_link)
                f.write(country + "," + species + "," + subcategory + "," + "" + "," + supercategory + "," + full_species_link + "\n")
        elif order_td is None and class_td is not None:
            category = class_td.find_next_sibling().a.get("title")
            supercategory = phylum_td.find_next_sibling().a.get("title")
            print(country + "," + species + "," + "" + "," + category + "," + supercategory + "," + full_species_link + "\n")
            f.write(country + "," + species + "," + "" + "," + category + "," + supercategory + "," + full_species_link + "\n")
        elif order_td is not None and class_td is not None:
            subcategory = order_td.find_next_sibling().a.get("title")
            category = class_td.find_next_sibling().a.get("title")
            print(country + "," + species + "," + subcategory + "," + category + "," + "" + "," + full_species_link)
            f.write(country + "," + species + "," + subcategory + "," + category + "," + "" + "," + full_species_link + "\n")
        else:
            subcategory = order_td.find_next_sibling().a.get("title")
            supercategory = phylum_td.find_next_sibling().a.get("title")
            print(country + "," + species + "," + subcategory + "," + "" + "," + supercategory + "," + full_species_link)
            f.write(country + "," + species + "," + subcategory + "," + "" + "," + supercategory + "," + full_species_link + "\n")

f.close()
