from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, time, json, os, pytz

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
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

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
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
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
    
    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
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
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

    async def user_login(self, address: str, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/auth/generateToken"
        data = json.dumps({"wallet_address":address})
        headers = {
            **self.headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 404:
                    return self.print_message(self.mask_account(address), proxy, Fore.RED, f"GET Access Token Failed: {Fore.YELLOW+Style.BRIGHT}Join Testnet & Complete Required Tasks First")
                    
                response.raise_for_status()
                result = response.json()
                return result['token']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(self.mask_account(address), proxy, Fore.RED, f"GET Access Token Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")

    async def wallet_details(self, address: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://naorisprotocol.network/testnet-api/api/testnet/walletDetails"
        data = json.dumps({"walletAddress":address})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Token": token
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    continue

                response.raise_for_status()
                result = response.json()
                return result['details']
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(self.mask_account(address), proxy, Fore.RED, f"GET Wallet Details Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def add_whitelisted(self, address: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/api/addWhitelist"
        data = json.dumps({"walletAddress":address, "url":"naorisprotocol.network"})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Token": token
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    continue
                elif response.status_code == 403:
                    return self.print_message(self.mask_account(address), proxy, Fore.RED, f"Add to Whitelist Failed: {Fore.YELLOW+Style.BRIGHT}Already Exists In Whitelist")

                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                return self.print_message(self.mask_account(address), proxy, Fore.RED, f"Add to Whitelist Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def toggle_activated(self, address: str, token: str, state: str, device_hash: int, proxy=None, retries=5):
        url = "https://naorisprotocol.network/sec-api/api/switch"
        data = json.dumps({"walletAddress":address, "state":state, "deviceHash":device_hash})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
        
                return self.print_message(self.mask_account(address), proxy, Fore.RED, f"Turn On Protection Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
    
    async def send_heartbeats(self, address: str, token: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://beat.naorisprotocol.network/api/ping"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, json={}, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 401:
                    token = await self.process_get_access_token(address, use_proxy)
                    headers["Authorization"] = f"Bearer {token}"
                    continue
                elif response.status_code == 410:
                    return self.print_message(self.mask_account(address), proxy, Fore.GREEN, f"{response.text}")

                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                
                if "502" in str(e):
                    return self.print_message(self.mask_account(address), proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}Server Down")
                
                self.rotate_proxy_for_account(address) if use_proxy else None
                return self.print_message(self.mask_account(address), proxy, Fore.RED, f"PING Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}")
            
    async def process_get_access_token(self, address: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None
        token = None
        while token is None:
            token = await self.user_login(address, proxy)
            if not token:
                proxy = self.rotate_proxy_for_account(address) if use_proxy else None
                await asyncio.sleep(5)
                continue

            self.print_message(address, proxy, Fore.GREEN, "GET Access Token Success")
            return token
            
    async def process_user_earnings(self, address: str, token, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            today_earning = "N/A"
            total_earning = "N/A"
            total_uptime = "N/A"

            wallet = await self.wallet_details(address, token, use_proxy, proxy)
            if wallet:
                today_earning = wallet.get("todayEarnings")
                total_earning = wallet.get("totalEarnings")
                total_uptime = wallet.get("totalUptimeMinutes")

            self.print_message(address, proxy, Fore.WHITE, 
                f"Earning Today: {today_earning} PTS "
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} Total: {total_earning} PTS {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Uptime: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{total_uptime} Minutes{Style.RESET_ALL}"
            )

            await asyncio.sleep(10 * 60)

    async def process_activate_toggle(self, address, device_hash, token, use_proxy):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        whitelist = await self.add_whitelisted(address, token, use_proxy, proxy)
        if whitelist and whitelist.get("message") == "url saved successfully":
            self.print_message(address, proxy, Fore.GREEN, "Add to Whitelist Success")

        while True:
            deactivate = await self.toggle_activated(address, token, "OFF", device_hash, proxy)
            if deactivate and deactivate.strip() in ["Session ended and daily usage updated", "No action needed"]:
                activate = await self.toggle_activated(address, token, "ON", device_hash, proxy)
                if activate and activate.strip() == "Session started":
                    self.print_message(address, proxy, Fore.GREEN, "Turn On Protection Success")
                    return True
                else:
                    continue
            else:
                continue

    async def process_send_heatbeats(self, address, token, use_proxy):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            heartbeat = await self.send_heartbeats(address, token, use_proxy, proxy)
            if heartbeat:
                self.print_message(address, proxy, Fore.GREEN, "PING Success")

            await asyncio.sleep(10)

    async def process_accounts(self, address: str, device_hash: int, use_proxy: bool):
        token = await self.process_get_access_token(address, use_proxy)
        if token:
            
            tasks = []
            tasks.append(asyncio.create_task(self.process_user_earnings(address, token, use_proxy)))

            activate = await self.process_activate_toggle(address, device_hash, token, use_proxy)
            if activate:
                tasks.append(asyncio.create_task(self.process_send_heatbeats(address, token, use_proxy)))

            await asyncio.gather(*tasks)

    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log(f"{Fore.RED}No Accounts Loaded.{Style.RESET_ALL}")
                return

            use_proxy_choice = self.print_question()

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

            while True:
                tasks = []
                for account in accounts:
                    address = account['Address'].lower()
                    device_hash = int(account['deviceHash'])

                    if address and device_hash:
                        tasks.append(asyncio.create_task(self.process_accounts(address, device_hash, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

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