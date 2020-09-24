from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def write_to_csv(result_list):
    header = ["Category", "Brand", "Model", "Cpu", "Ram", "Storage", "Gpu", "Display", "Image", "Link", "Price"]
    with open('fahem_it_test.csv', mode='w', encoding='utf-8', newline='') as data_csv:
        dict_writer = csv.DictWriter(data_csv, fieldnames=header, dialect='excel')
        dict_writer.writeheader()
        dict_writer.writerows(result_list)

def crawl_each_link(inside_url_list):
    base_url = "http://www.fahem-it.com/"
    products = []
    for inside_url in inside_url_list:
        product = {}
        url_path = base_url + inside_url

        try:
            product_page = requests.get(url_path, headers=agent)
            product_soup = BeautifulSoup(product_page.content,"lxml")

            # Product Specs
            product_info = product_soup.find("div", attrs={"id":"desc2"})
            product_info_table = product_info.findChildren("table")[0]
            df = pd.read_html(str(product_info_table))[0]
            spec_values = df[1].tolist()

            # Product Price
            price_div = product_soup.find("div", {"class":"price-animation"})
            price = int(price_div.find("h2").get_text())

            # Product Image
            image = product_soup.find("img", attrs={"class":"product-image-zoom"})



            product["Category"] = spec_values[1][7:]
            product["Brand"] = spec_values[2]
            product["Model"] = spec_values[3]
            product["Cpu"] = spec_values[4] + " " + spec_values[5]
            product["Ram"] = spec_values[8] + " " + spec_values[7]
            product["Storage"] = spec_values[9] + " " + spec_values[10]
            product["Gpu"] = spec_values[12]
            product["Display"] = spec_values[13] + " " + spec_values[14]
            product["Image"] = image["src"]
            product["Link"] = url_path
            product["Price"] = price

            time.sleep(2)
            products.append(product)
            print(product)
        except:
            continue
    
    print("\nDONE\n")

    return True


def product_crawler(url):
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content,"lxml")

    product_list = soup.find_all("a", attrs={"target": "_self"}, href=True)
    links = []
    for product in product_list:
        links.append(product['href'])
    links = list(set(links))
    products = crawl_each_link(links)

    return products



def main():
    laptop_url = "http://www.fahem-it.com/subcategory?id=1&id2=1"
    desktop_url = "http://www.fahem-it.com/subcategory?id=1&id2=46"

    urls = [laptop_url, desktop_url]
    products = []
    for url in urls:
        product = product_crawler(url)
        print("CRAWLER STAGE DONE!\n")
        products.append(product)

    final_product = products[0] + products[1]

    write_to_csv(final_product)

if __name__ == '__main__':
    main()