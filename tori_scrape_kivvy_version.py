from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.label = Label(size_hint=(1, None), height=Window.height)
        self.layout.add_widget(self.label)

    def set_text(self, text):
        self.label.text = text


class ToriScraperApp(App):
    def __init__(self, **kwargs):
        super(ToriScraperApp, self).__init__(**kwargs)
        self.url_input = None
        self.result_label = None

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        self.url_input = TextInput(multiline=False)
        layout.add_widget(self.url_input)

        btn = Button(text='Scrape', size_hint=(1, 0.5))
        btn.bind(on_press=self.scrape_tori)
        layout.add_widget(btn)

        self.result_label = ScrollableLabel()
        layout.add_widget(self.result_label)

        return layout

    def scrape_tori(self, instance):
        url = self.url_input.text.strip()
        if not url:
            return

        x = 1.1
        lOfLists = []
        current_date = time.strftime("%d %b %y", time.gmtime())

        r = re.findall("o=(\d+)$", url)
        rStr = str(int(r[0]))
        del_from_end = len(r[0])
        clean_url = url[:-del_from_end]

        while int(rStr) >= 1:
            website = requests.get(clean_url + rStr)
            soup = BeautifulSoup(website.content, "lxml")

            for item in soup.find_all('div', attrs={"class": "ad-details-left"}):
                paramsText = None

                try:
                    paramsNum = item.find_all('p', attrs={'class': "param"})[1].get_text()
                    paramsText = item.find_all('p', attrs={'class': "param"})[0].get_text()
                except:
                    try:
                        paramsNum = item.find_all('p', attrs={'class': "param"})[0].get_text()
                    except:
                        paramsNum = None

                name = item.find('div', attrs={"class": "li-title"}).get_text()
                price = item.find('p', attrs={"class": "list_price ineuros"}).get_text()

                lOfLists.append([name, price, paramsNum, paramsText, current_date])

            print("Finished databasing page {}".format(rStr))
            rStr = str(int(rStr) - 1)

            time.sleep(x)

        print("Scraping finished")
        df = pd.DataFrame(lOfLists, columns=["name", "price", "numParam", "textParam", "date"])
        self.result_label.set_text(df.to_string(index=False))


if __name__ == '__main__':
    ToriScraperApp().run()
