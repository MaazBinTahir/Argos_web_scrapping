import requests
from bs4 import BeautifulSoup
import pandas as pd



base_url = "https://www.argos.co.uk"
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}


# Parsing and generating product links
productlinks = []

for x in range(1,6):
    
    if x==1:
        url = "https://www.argos.co.uk/browse/home-and-furniture/bedding/duvet-cover-sets/c:29474/"
    else:
        url = f"https://www.argos.co.uk/browse/home-and-furniture/bedding/duvet-cover-sets/c:29474/opt/page:{x}/"
    
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.content, "lxml")
    
    productlist = soup.find_all('div', class_ = "styles__ProductList-sc-1rzb1sn-1 hiBlrl")
    
    for item in productlist:
        for link in item.find_all("a",class_="Buttonstyles__Button-sc-42scm2-2 fXjZqi btn-cta" ,href = True):
            productlinks.append(base_url+link['href'])

# link4 and link24 was not added, as there was an article on the location of link4, and Add to trolley
# button was inplace of Choose option incase of link24, so adding it separately            
link4 = 'https://www.argos.co.uk/product/6062815?clickPR=plp:4:258'
link24 = 'https://www.argos.co.uk/product/9442432?clickPR=plp:24:258'

productlinks.insert(3,link4)
productlinks.insert(23,link24)


# Looping through product links and extracting required attributes/features/columns
bedlist = []
for i in productlinks:
    
    test_url = i
    page = requests.get(test_url, headers=agent)
    soup = BeautifulSoup(page.content, "lxml")
    
    # Name
    name = soup.find('div', class_ = "Namestyles__ProductName-sc-269llv-0 kEQsqE bolt-v2").text
    
    # Brand
    brand =soup.find('div', class_ = "Namestyles__ProductName-sc-269llv-0 kEQsqE bolt-v2").text
    brand = brand.split(' ')[0]
    
    # Label
    try:
        label =soup.find('div', {'class': 'Badgesstyles__BadgeWrapper-xfrkcy-1 fHFBWk'}).img.get('alt')
    except:
        label = ""
        
    # Price Feature
    try:
        pfeature = soup.find("span", class_ = "Pricestyles__PriceSave-sc-1oev7i-2 iEECOV").text

    except:
        pfeature = ""
        
        
    # Size and Price
    items = soup.select('option[value]')
    textvalues = [item.text for item in items]
    
    sizes = [i for i in textvalues if "£" in i]
    
    all_sizes = [sizes[i].split("-")[0] for i in range(len(sizes))]
    all_sizes1 = ", ".join([str(i) for i in all_sizes])
    all_prices = [sizes[i].split("-")[1] for i in range(len(sizes))]
    all_prices_float = [float(all_prices[i].strip(" ").strip("£")) for i in range(len(all_prices))]
    
    # Creating a Dictionary 
    dict1 = dict(zip(all_sizes, all_prices_float))
    
    # Sorting values of dictinary according to price
    sort_orders = sorted(dict1.items(), key=lambda x: x[1])
    
    try :
        size1 = sort_orders[0][0]
        price1 = sort_orders[0][1]
    except:
        size1 = "None"
        price1 = "None"

    try :
        size2 = sort_orders[1][0]
        price2 = sort_orders[1][1]
    except:
        size2 = "None"
        price2 = "None"

    try :
        size3 = sort_orders[2][0]
        price3 = sort_orders[2][1]
    except:
        size3 = "None"
        price3 = "None"

    try :
        size4 = sort_orders[3][0]
        price4 = sort_orders[3][1]
    except:
        size4 = "None"
        price4 = "None"
        
        
    # Description
    description  = soup.findAll('p')[4].next
    
    # Creating a list of the texts in li-tags
    litag = soup.find_all("li")
    a = [i.contents[0].text for i in litag]
    
    # Iterating the list and saving texts to corresponding columns
    for i in a:
    
        try:
            if "Finish" in i:
                finish =  i

            elif "%" in i:
                composition = i

            elif "thread" in i:
                thread = i

            elif "Set includes" in i:
                pack = i

            elif "Bed size" in i:
                bed_size = i

            elif "Reversible" in i:
                features = i

            elif "cm" in i:
                dimensions = i

            elif "fastening" in i:
                fastening = i

            elif "pillowcase" in i:
                pillowcase = i

            elif "length" in i:
                pillowcase_dim = i

            elif "washable" in i:
                washing = i

            elif "drying" in i:
                drying = i

            elif "EAN" in i:
                ean = i

        except:
            
            finish = "Nan"
            composition = ""
            thread = ""
            pack = ""
            bed_size = ""
            features = ""
            dimensions = ""
            fastening = ""
            pillowcase = ""
            pillowcase_dim = ""
            washing = ""
            drying = ""
            ean = ""
        
    # Reviews    
    try:
        rev =soup.find("a", class_ = "ReviewsFlagstyles__Link-in5zbx-0 bEmcWa").text
        review = rev.split()
        review = [i.strip("()") for i in review if "(" in i]
        reviews = review[0]
    except:
        reviews = ""
    
    # Ratings
    try:
        ratings = soup.find("div", class_ = "sr-only").text


        for i in ratings.split():
            try:
                if "." in i:
                    ratings =float(i)
            except:
                pass
    except:
        ratings = ""
        
    # Recommendations
    
    try:
        b = soup.find_all("h3")[0].text
        b = b.split()

        recom = [i for i in b if "%" in i]
        recommendation = recom[0]
    except:
        recommendation = ""
    
    
        
        
    bed = {
        "Link-href" : test_url,
        "Brand" : brand,
        "Name" : name,
        "Label" : label,
        "Price Feature" : pfeature,
        "All Sizes" : all_sizes1,
        "Size 1" : size1,
        "Price 1" : price1,
        "Size 2" : size2,
        "Price 2" : price2,
        "Size 3" : size3,
        "Price 3" : price3,
        "Size 4" : size4,
        "Price 4" : price4,
        "Description" : description,
        "Finish" : finish,
        "Composition" : composition,
        "Thread ": thread,
        "Pack" : pack,
        "Bed Size" : bed_size,
        "Features" : features,
        "Dimensionns" : dimensions,
        "Fastenings" : fastening,
        "Pillowcase" : pillowcase,
        "Pillowcase Dimensions" : pillowcase_dim,
        "Washing" : washing,
        "Drying" : drying,
        "EAN" : ean,
        "Reviews" : reviews,
        "Ratings" : ratings,
        "Recommendations" : recommendation
    }
    
    bedlist.append(bed)
        
        
df = pd.DataFrame(bedlist)
df.to_csv("Market_Research_Analyst_Maaz.csv", index = False)