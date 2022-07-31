from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re
import time

def tori_scrape(url, x=1.1):
    """Returns a pandas DataFrame from Tori.fi search
    scrapes all pages from first to input url page
    optional second argument x for sleep time between page loads"""
    
    lOfLists = []
    current_date = time.strftime("%d %b %y",time.gmtime())
    
    #picks the page number and cleans url for loop purposes
    r = re.findall("o=(\d+)$", url)

    rStr = (str(int(r[0])))
    del_from_end = len(r[0])
    clean_url = (url[:-del_from_end])
    
    #loop until search results page 1 has been collected
    while(int(rStr) >= 1):

        website = requests.get(clean_url+rStr)
        soup = BeautifulSoup(website.content, "lxml")


        for item in soup.find_all('div', attrs = {"class" : "ad-details-left"}):

            paramsText = None
            
            #try to collect optional data
            
            try: 
                paramsNum = item.find_all('p', attrs = {'class' : "param"})[1].get_text()
                paramsText = item.find_all('p', attrs = {'class' : "param"})[0].get_text()
            except:
                try:
                    paramsNum = item.find_all('p', attrs = {'class' : "param"})[0].get_text()
                except:
                    paramsNum = None

                
            
            name = item.find('div', attrs = {"class" : "li-title"}).get_text()
            price = item.find('p', attrs = {"class" : "list_price ineuros"}).get_text()

            lOfLists.append([name, price, paramsNum, paramsText, current_date])


        print("finished databasing page {}".format(rStr))
        rStr = str(int(rStr)-1)
        
        time.sleep(x)
    print("all finish")
    return(pd.DataFrame(lOfLists, columns = ["name", "price", "numParam", "textParam", "date"]))
