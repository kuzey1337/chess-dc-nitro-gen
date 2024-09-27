import os, re, sys, time, json, base64, random, string, ctypes, getpass, threading

try:
    import requests
    import tls_client
    import datetime
    import colorama
    import pystyle
    import uuid
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install tls_client")
    os.system("pip install datetime")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install uuid")

from pystyle import Write, System, Colors, Colorate, Center
from datetime import datetime, timezone
from colorama import Fore, Style, init
from tls_client import Session
from loguru import logger

init()


class Config:
    config = json.load(open("config.json"))
    threads = config['threads']

class Promos:
    promos = []



class Stats:
    created = 0
    failed = 0
    start = time.time()
    working = True

class Chess:
    def __init__(self) -> None:
        self.client = requests.Session()

        with open("proxies.txt", "r", encoding='utf-8') as f:
            proxies = f.read().splitlines()
            self.proxy = random.choice(proxies)

        self.client.proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}"
        }

    def __randomEmail__(self) -> str:
        name_length = random.randint(5, 10)
        random_name = ''.join(random.choices(string.ascii_lowercase, k=name_length))
        
        domain_length = random.randint(3, 6)
        random_domain = ''.join(random.choices(string.ascii_lowercase, k=domain_length))
        
        random_number = random.randint(1111111111, 999999999999999)
        
        return f"{random_name}{random_number}@{random_domain}.com"
    
    def __randomPassword__(self) -> str:
        name_length = random.randint(5, 10)
        random_name = ''.join(random.choices(string.ascii_lowercase, k=name_length))
        
        random_number = random.randint(111111, 999999)
        
        return f"{random_name}{random_number}clown"
    
    def __randomUsername__(self) -> str:
        name_length = random.randint(5, 10)
        random_name = ''.join(random.choices(string.ascii_lowercase, k=name_length))
        
        # Generate a random number for the username
        random_number = random.randint(111111, 999999)
        
        # Return the full random username
        return f"{random_name}{random_number}"

    def __register__(self) -> None:
        try:
            email, password, username = self.__randomEmail__(), self.__randomPassword__(), self.__randomUsername__()
            
            r = self.client.get(f"https://www.chess.com/service/gamelist/top?limit=50&from={random.randint(1, 1000)}").json()

            for game in r:
                for user in game["players"]:
                    user_uuid = user["uuid"]
                    logger.warning(f"Successfully Scraped UUID,{user_uuid},{username}")
                    return user_uuid, email
        except Exception as e:
            logger.error("c1121f", "!", f"ERROR,{e},Exception")
    
    def __fetchPromoCode__(self) -> None:
        try:
            user_uuid, email = self.__register__()

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES;q=0.8, en;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://www.chess.com',
                'priority': 'u=1, i',
                'referer': 'https://www.chess.com/play/computer/discord-wumpus?utm_source=chesscom&utm_medium=homepagebanner&utm_campaign=discord2024',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            }

            payload = {
                'userUuid': user_uuid,
                'campaignId': '4daf403e-66eb-11ef-96ab-ad0a069940ce',
            }

            while True:
                r = self.client.post(
                    'https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode',
                    headers=headers,
                    json=payload,
                )

                promo = r.json()['codeValue']

                if promo not in Promos.promos:
                    Promos.promos.append(promo)
                    logger.info(f"Fetched Promo Code,{email},{promo}")
                    logger.success(f"Successfully Saved Promo,{promo},promos.txt")
                    with open("promos.txt", "a+", encoding="utf-8") as f:
                        f.write(f"https://discord.com/billing/promotions/{promo}" + "\n")
                    
                    Stats.created += 1
                    break
                else:
                    time.sleep(1)

            self.__fetchPromoCode__()
        except Exception as e:
            None

if __name__ == "__main__":
    try:
        print(Fore.MAGENTA +"discord.gg/clown / https://t.me/clownshub" + Style.RESET_ALL)
        print(Fore.MAGENTA +"@cinali / @kuzey1337" + Style.RESET_ALL)
        while True:
            while threading.active_count() - 1 < Config.threads:
                chess = Chess()
                threading.Thread(target=chess.__fetchPromoCode__).start()
            time.sleep(1)
    except:
        pass