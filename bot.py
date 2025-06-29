from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class NaorisProtocol:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "chrome-extension://cpikalnagknmlfhnilhfelifgbollmmp",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://naorisprotocol.network"
        self.PING_API = "https://beat.naorisprotocol.network"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.refresh_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}Naoris Protocol Node - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "accounts.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
    
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
         schemes = ["http://", "https://", "socks4://", "socks5://"]
         if any(proxies.startswith(scheme) for scheme in schemes):
             return proxies
         return f"http://{proxies}"
 
    def get_next_proxy_for_account(self, account):
         if account not in self.account_proxies:
             if not self.proxies:
                 return None
             proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
             self.account_proxies[account] = proxy
             self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
         return self.account_proxies[account]
 
    def rotate_proxy_for_account(self, account):
         if not self.proxies:
             return None
         proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
         self.account_proxies[account] = proxy
         self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
         return proxy
    
    def mask_account(self, account):
        mask_account = account[:6] + '*' * 6 + account[-6:]
        return mask_account
    
    def print_message(self, address, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def generate_token(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/sec-api/auth/gt-event"
        data = json.dumps({"wallet_address":address})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                if response.status_code == 404:
                    self.print_message(address, proxy, Fore.RED, f"Generate Token Failed: {Fore.YELLOW+Style.BRIGHT}Join Testnet & Complete Required Tasks First")
                    return None
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Generate Token Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")

        return None
    
    async def refresh_token(self, address: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/sec-api/auth/refresh"
        data = json.dumps({"refreshToken":self.refresh_tokens[address]})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                if response.status_code == 401:
                    await self.process_generate_token(address, use_proxy, rotate_proxy)
                    data = json.dumps({"refreshToken":self.refresh_tokens[address]})
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Refreshing Token Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")

        return None
            
    async def wallet_details(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/sec-api/api/wallet-details"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"GET Wallet Details Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")

        return None
    
    async def add_whitelist(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/sec-api/api/addWhitelist"
        data = json.dumps({"walletAddress":address, "url":"naorisprotocol.network"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                if response.status_code == 409:
                    self.print_message(address, proxy, Fore.RED, f"Add to Whitelist Failed: {Fore.YELLOW+Style.BRIGHT}URL Already Exists In Whitelist")
                    return None
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Add to Whitelist Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")

        return None
    
    async def toggle_activation(self, address: str, device_hash: int, state: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/sec-api/api/switch"
        data = json.dumps({"walletAddress":address, "state":state, "deviceHash":device_hash})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.BLUE, "Device Hash"
                    f"{Fore.WHITE + Style.BRIGHT} {device_hash} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Activate Protection Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )

        return None
    
    async def initiate_msg_product(self, address: str, device_hash: int, proxy=None, retries=5):
        url = f"{self.PING_API}/sec-api/api/htb-event"
        data = json.dumps({"inputData":{"walletAddress":address, "deviceHash":device_hash}})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.BLUE, "Device Hash"
                    f"{Fore.WHITE + Style.BRIGHT} {device_hash} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Initiate Production Message Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )

        return None
    
    async def perform_ping(self, address: str, device_hash: int, proxy=None, retries=5):
        url = f"{self.PING_API}/api/ping"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, json={}, proxy=proxy, timeout=60, impersonate="chrome110", verify=False)
                if response.status_code == 410:
                    return response.text
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.BLUE, "Device Hash"
                    f"{Fore.WHITE + Style.BRIGHT} {device_hash} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} PING Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )

        return None
        
    async def process_generate_token(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            token = await self.generate_token(address, proxy)
            if token:
                self.access_tokens[address] = token["token"]
                self.refresh_tokens[address] = token["refreshToken"]

                self.print_message(address, proxy, Fore.GREEN, "Generate Token Success")
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)

            await asyncio.sleep(5)
            continue

    async def process_refresh_token(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            await asyncio.sleep(30 * 60)
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            while True:
                token = await self.refresh_token(address, use_proxy, rotate_proxy, proxy)
                if token:
                    self.access_tokens[address] = token["token"]
                    self.refresh_tokens[address] = token["refreshToken"]

                    self.print_message(address, proxy, Fore.GREEN, "Refreshing Token Success")
                    break

                await asyncio.sleep(5)
                continue

    async def process_add_whitelist(self, address: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        whitelist = await self.add_whitelist(address, proxy)
        if whitelist and whitelist.get("message") == "url saved successfully":
            self.print_message(address, proxy, Fore.GREEN, "Add to Whitelist Success")

        return True

    async def process_get_wallet_details(self, address: str, use_proxy: bool):
        await self.process_add_whitelist(address, use_proxy)

        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            wallet = await self.wallet_details(address, proxy)
            if wallet:
                total_earning = wallet.get("message", {}).get("totalEarnings") or 0

                self.print_message(address, proxy, Fore.WHITE, f"Earning Total: {total_earning} PTS")

            await asyncio.sleep(15 * 60)

    async def process_deactivate_toggle(self, address: str, device_hash: int, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            deactivate = await self.toggle_activation(address, device_hash, "OFF", proxy)
            if deactivate and deactivate.strip() in ["Session ended and daily usage updated", "No action needed"]:
                return True
        
            await asyncio.sleep(5)
            continue

    async def process_activate_toggle(self, address: str, device_hash: int, use_proxy: bool):
        deactivated = await self.process_deactivate_toggle(address, device_hash, use_proxy)
        if deactivated:
            while True:
                proxy = self.get_next_proxy_for_account(address) if use_proxy else None

                activate = await self.toggle_activation(address, device_hash, "ON", proxy)
                if activate and activate.strip() == "Session started":
                    self.print_message(address, proxy, Fore.BLUE, "Device Hash "
                        f"{Fore.WHITE + Style.BRIGHT}{device_hash}{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}Protection Activated Successfully{Style.RESET_ALL}"
                    )
                    return True
                
                await self.process_deactivate_toggle(address, device_hash, use_proxy)
                await asyncio.sleep(5)
                continue

    async def process_send_ping(self, address: str, device_hash: int, use_proxy: bool):
        while True:
            await asyncio.sleep(10)
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            ping = await self.perform_ping(address, device_hash, proxy)
            if ping and ping.strip() == "Ping Success!!":
                self.print_message(address, proxy, Fore.BLUE, "Device Hash "
                    f"{Fore.WHITE + Style.BRIGHT}{device_hash}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}PING Success{Style.RESET_ALL}"
                )

    async def process_initiate_msg_product(self, address: str, device_hash: int, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            initiate = await self.initiate_msg_product(address, device_hash, proxy)
            if initiate:
                self.print_message(address, proxy, Fore.BLUE, "Device Hash "
                    f"{Fore.WHITE + Style.BRIGHT}{device_hash}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}Production Message Initiated Successfully{Style.RESET_ALL}"
                )
                return True
            
            await asyncio.sleep(5)
            continue

    async def looping_initiate_msg_product(self, address: str, device_hash: int, use_proxy: bool):
        while True:
            await asyncio.sleep(10 * 60)
            await self.process_initiate_msg_product(address, device_hash, use_proxy)

    async def process_perform_ping(self, address: str, device_hash: int, use_proxy: bool):
        activated = await self.process_activate_toggle(address, device_hash, use_proxy)
        if activated:
            tasks = [
                asyncio.create_task(self.looping_initiate_msg_product(address, device_hash, use_proxy)),
                asyncio.create_task(self.process_send_ping(address, device_hash, use_proxy)),
            ]
            await asyncio.gather(*tasks)
        
    async def process_accounts(self, address: str, device_hash: int, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_generate_token(address, use_proxy, rotate_proxy)
        if logined:
            tasks = [
                asyncio.create_task(self.process_refresh_token(address, use_proxy, rotate_proxy)),
                asyncio.create_task(self.process_get_wallet_details(address, use_proxy)),
                asyncio.create_task(self.process_perform_ping(address, device_hash, use_proxy))
            ]
            await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*65)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    address = account["Address"].lower()
                    device_hash = int(account["deviceHash"])

                    if not address or not device_hash:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Account Data {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    tasks.append(asyncio.create_task(self.process_accounts(address, device_hash, use_proxy, rotate_proxy)))

            await asyncio.gather(*tasks)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = NaorisProtocol()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Naoris Protocol Node - BOT{Style.RESET_ALL}                                       "                              
        )