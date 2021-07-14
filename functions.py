from bs4 import BeautifulSoup
import pandas as pd
import requests



#returns product name from the page soup
def getName(soup):
    productName = soup.find('span', class_="B_NuCI").text
    return productName

#returns product price from the page soup
def getPrice(soup):
    productPrice = soup.find('div', class_="_30jeq3 _16Jk6d").text[1:]
    return productPrice.replace(',','')

# def getRating(soup):
#     tag = soup.find('div', class_="gUuXy- _16VRIQ")
#     if(tag == None):
#         return 'no rating yet'
#     else:
#         rating = tag.find('div', class_="_3LWZlK").text
#         return float(rating)

#returns product availability from the page soup
def getAvailability(soup):
    if(soup.find('div', class_="_16FRp0") == None):
        return 'available'
    else:
        return 'not available'    
    
#adds the entry using product page url
def addEntry(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    r = requests.get(url, headers)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    name = getName(soup)
    price = getPrice(soup)
    availability = getAvailability(soup)

    df = pd.read_csv('database.csv',index_col=0)
    newEntry = {'product_name':name,
            'price_in_rupees':price,
            'availability':availability,
            'link':url}

    df = df.append(newEntry, ignore_index=True)
    df.to_csv('database.csv')
    print(newEntry['product_name'][:20]+'... added to Database!')
    print('############################################')
    
# gets the links to all the products on section page and calls addEntry for each
def populateDB(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# U L     R C S I G
#  R    P  O E S N

    r = requests.get(url, headers)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
            
    data = soup.find_all('div', class_="_13oc-S")
    
    product_class = data[0].contents[0].div['class'][0]
        
    links = soup.find_all('div', class_=product_class)


    for link in links:
        product_link = 'https://flipkart.com' + link.find('a')['href']
        addEntry(product_link)