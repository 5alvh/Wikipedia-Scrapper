import requests
from datetime import date
from bs4 import BeautifulSoup
from Managers.DbManager import dbService 

class ScrappingManager:

    db = dbService()

    def __init__(self):
        print("Initializing the Scrapping MANGEEEEEER...")
        
    def checkUrlInDb(self, url):
        found = self.db.searchUrlInDb(url)
        if found == True:
            return False
        return url 
    
    def checkUrl(self, url):
        if "wikipedia" not in url:
            return False
        else:
            return True
        
    def checkResponse(self, url):

        try:
            response = requests.get(url)
            response.raise_for_status()       
            if response.status_code != 200:
                #print("The resource was not found. Link Not Valid")
                return False
            
            return True
        
        except requests.exceptions.RequestException as e:
            return False
        
    def theScrapper(self, url):
        try:
            response = requests.get(url) 
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
            main_content = soup.find('div', {'id': 'mw-content-text'})
            current_section = ""
            content = []
            
            for element in main_content.find_all(['h2', 'h3', 'p', 'ul']):
                if element.name in ['h2', 'h3']:
                    if current_section and content:
                        self.db.addScrappedWeb(
                            title=f"{title} - {current_section}",
                            url=url,
                            content='\n'.join(content),
                            content_type=element.name
                        )
                    current_section = element.text.replace('[editar]', '').strip()
                    content = []
                elif element.name in ['p', 'ul']:
                    text = element.text.strip()
                    if text: 
                        content.append(text)
            
            if current_section and content:
                self.db.addScrappedWeb(
                    title=f"{title} - {current_section}",
                    url=url,
                    content='\n'.join(content),
                    content_type=element.name
                )
            return True
        except Exception as e:
            print(f"Error scraping Wikipedia: {str(e)}")
            return False
        
    def scrape_url(self, url):
        print("Scraping Wikipedia...")

        if not self.checkUrlInDb(url):
            return {"success":False, "message": "URL already scrapped and exists in the database"}
        
        if not self.checkUrl(url):
            return {"success":False, "message": "URL NOT VALID"}
        
        url = str(url)
        if self.checkResponse(url):
            if self.theScrapper(url):
                return {"success": True, "message": "URL scrapped successfully and saved in the database"}
            else:
                return {"success": False, "message": "Failed to scrape URL"}
        else:
            return {"success":False, "message": "URL NOT VALID"}