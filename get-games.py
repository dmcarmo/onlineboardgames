import os.path
from os import path
import pprint

import requests
from bs4 import BeautifulSoup

import tabletopia

def bga():
    base_url = "https://boardgamearena.com/gamelist"
    if path.exists("bga.html"):
        with open("bga.html", "r") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
    else:
        soup = getsoup(base_url)
    elements = soup.find("div", {"id": "gamelist_itemrow_inner_all"}).findAll("a")
    games = {}
    for item in elements:
        name = item.text.strip().title()
        #url = base_url[:-9] + item.attrs["href"]
        url = item.attrs["href"]
        games[name] = url
    return games

def boiteajeux():
    base_url = "http://boiteajeux.net/index.php?p=regles"
    soup = getsoup(base_url)
    elements = soup.find("div", {"class": "span7"}).findAll("div", {"class": "jeuxRegles"})
    games = {}
    for item in elements:
        name = item.text.strip().split("\n")[0].title()
        url = "http://boiteajeux.net"
        games[name] = url
    return games

def happymeeple():
    base_url = "https://www.happymeeple.com/en/"
    soup = getsoup(base_url)
    elements = soup.find("div", {"class": "main_div_invisible"}).findAll("div", {"class": "pres_game"})
    games = {}
    for item in elements:
        name = item.div["title"].strip().title()
        url = item.a.attrs["href"]
        games[name] = url
    return games

def tabletopia():
    return tabletopia.main()

def vassal():
    base_url = "http://www.vassalengine.org"
    next_page = "http://www.vassalengine.org/wiki/Category:Modules"
    games = {}
    while next_page is not None:
        soup = getsoup(next_page)
        elements = soup.find("div", {"id": "mw-pages"}).findAll("a")
        for item in elements:
            if "Module:" in item.text:
                name = item.text[len("Module:"):].strip().title()
                url = base_url + item.attrs["href"]
                games[name] = url
        nav = soup.find("div", {"id": "mw-pages"}).findAll("a", recursive = False)
        nav = nav[:-int(len(nav)/2)] # remove duplicate nav links from bottom of the list
        for item in nav:
            if "next page" in item.text:
                next_page = base_url + item.attrs["href"]
            else:
                next_page = None
    return games

def yucata():
    base_url = "https://www.yucata.de"
    soup = getsoup(base_url)
    elements = soup.find("table", {"id": "ctl00_cphRightCol_dlAllGames"}).findAll("a")
    games = {}
    for item in elements:
        name = item.text.strip().title()
        url = base_url + item.attrs["href"]
        games[name] = url
    return games

def getsoup(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    else:
        return None

def games_list(sites):
    games = {}
    for site in sites:
        for game in sites[site]:
            url = sites[site][game]
            if game in games:
                games[game].update( {site: url} )
            else:
                games[game] = {site: url}
    return games

def create_table(games):
    table = ""
    for game in sorted(games):
        link = ""
        first = True
        for site in sorted(games[game]):
            url = games[game][site]
            if first:
                first = False
                link += f"[{site}]({url})"
            else:
                link += f" / [{site}]({url})"
        line = f"{game} | {link}"
        table += line + "\n"
    return table

# list of sites
# implemented:
#   BoardGameArena, Boardgamecore, BoardGamePlay, BoardGamingOnline, Boiteajeux,
#   Happy Meeple, MaBi Web, Online Terra Mystica, Orderofthehammer, rr18xx,
#   SlothNinja, VASSAL, Web Diplomacy, Yucata, Tabletopia
# to implement:
#   http://www.brettspielwelt.de/Spiele/?nation=en, https://triqqy.com/#/games
#   TTS official, TTS workshop (https://steamcommunity.com/workshop/browse/?appid=286160)

sites = {}
sites["Board Game Arena (Rules Enforced)"] = bga()
sites["Boiteajeux (Rules Enforced)"] = boiteajeux()
sites["Happy Meeple (Rules Enforced)"] = happymeeple()
sites["Tabletopia (No Rules Enforcement)"] = tabletopia()
sites["VASSAL (No Rules Enforcement)"] = vassal()
sites["Yucata (Rules Enforced)"] = yucata()

# "manual" lists for smaller sites
sites["Boardgamecore (Rules Enforced)"] = {
    "Antiquity": "http://play.boardgamecore.net/",
    "Food Chain Magnate": "http://play.boardgamecore.net/",
    "The Great Zimbabwe": "http://play.boardgamecore.net/",
    "Wir sind das Volk!": "http://play.boardgamecore.net/"
    }
sites["BoardGamePlay (Rules Enforced)"] = {
    "Rurik: Dawn of Kiev": "https://boardgameplay.com/",
    "The Manhattan Project: Energy Empire": "https://boardgameplay.com/",
    "Montana": "https://boardgameplay.com/",
    "Urbino": "https://boardgameplay.com/"
    }
sites["BoardGamingOnline (Rules Enforced)"] = {
    "Through the Ages: A Story of Civilization": "http://www.boardgaming-online.com/",
    "Through The Ages: A New Story of Civilization": "http://www.boardgaming-online.com/"
    }
sites["MaBi Web (Rules Enforced)"] = {
    "Nations": "http://www.mabiweb.com/modules.php?name=GM_Nations&op=description",
    "In the Year of the Dragon": "http://www.mabiweb.com/modules.php?name=GM_YearDragon&op=description",
    "Mykerinos": "http://www.mabiweb.com/modules.php?name=GM_Mykerinos&op=description",
    "Ur": "http://www.mabiweb.com/modules.php?name=GM_Ur&op=description",
    "Kreta": "http://www.mabiweb.com/modules.php?name=GM_Kreta&op=description",
    "Gods": "http://www.mabiweb.com/modules.php?name=GM_Gods&op=description",
    "In the Shadow of the Emperor": "http://www.mabiweb.com/modules.php?name=GM_ShadowEmperor&op=description",
    "Richelieu": "http://www.mabiweb.com/modules.php?name=GM_Richelieu&op=description"
    }
sites["Online Terra Mystica (Rules Enforced)"] = {"Terra Mystica": "https://terra.snellman.net/"}
sites["Orderofthehammer (Rules Enforced)"] = {"Brass": "http://brass.orderofthehammer.com/"}
sites["rr18xx (Rules Enforced)"] = {"18xx": "http://www.rr18xx.com"}
sites["SlothNinja (Rules Enforced)"] = {
    "After The Flood": "https://www.slothninja.com/",
    "Confucius": "https://www.slothninja.com/",
    "Guild of Thieves": "https://www.slothninja.com/",
    "Indonesia": "https://www.slothninja.com/",
    "Tammany Hall": "https://www.slothninja.com/"
    }
sites["Web Diplomacy (Rules Enforced)"] = {"Diplomacy": "https://www.webdiplomacy.net/"}

games = games_list(sites)
table = create_table(games)

# add date of last check


with open("table.txt", "w") as f:
    f.write(table)
