import asyncio
import requests
import time
import uuid
import os
from loguru import logger
from requests.exceptions import ProxyError, Timeout
from colorama import init, Fore, Style


init(autoreset=True)

PING_INTERVAL = 30
MAX_RETRIES = 3
MAX_PROXIES = 1000

DOMAIN_API = {
    "SESSION": "https://api.nodepay.ai/api/auth/session",
    "PING": "https://nw2.nodepay.ai/api/network/ping"
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NONE_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NONE_CONNECTION"]
token_info = None
browser_id = None
account_info = {}

def uuidv4():
    return str(uuid.uuid4())

def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp

def load_token():
    global token_info
    try:
        with open('user.txt', 'r') as f:
            token_info = f.readline().strip()
        if not token_info:
            raise ValueError("Token not found in user.txt")
    except Exception as e:
        logger.error(f"Failed to load token: {e}")
        raise SystemExit("Exiting due to failure in loading token")

def clear_terminal():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    """Menampilkan pesan 'BACTIAR' di atas terminal dengan gaya dan warna."""
    clear_terminal()
    print(Fore.GREEN + Style.BRIGHT + "BACTIAR".center(291))  

async def render_profile_info(proxy):
    global browser_id, token_info, account_info

    retries = 0
    while retries < MAX_RETRIES:
        try:
            np_session_info = load_session_info(proxy)

            if not np_session_info:
                response = call_api(DOMAIN_API["SESSION"], {}, proxy)
                valid_resp(response)
                account_info = response["data"]
                if account_info.get("uid"):
                    save_session_info(proxy, account_info)
                    await start_ping(proxy)
                else:
                    handle_logout(proxy)
            else:
                account_info = np_session_info
                await start_ping(proxy)
            break
        except Exception as e:
            retries += 1
            logger.error(f"Error in render_profile_info for proxy {proxy}: {e}, retry {retries}/{MAX_RETRIES}")
            if retries >= MAX_RETRIES:
                logger.error(f"Proxy {proxy} failed after {MAX_RETRIES} retries. Removing proxy from list.")
                remove_proxy_from_list(proxy)
            await asyncio.sleep(5)

def call_api(url, data, proxy):
    headers = {
        "Authorization": f"Bearer {token_info}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=30)
        response.raise_for_status()
    except (requests.RequestException, ProxyError, Timeout) as e:
        logger.error(f"Error during API call with proxy {proxy}: {e}")
        raise ValueError(f"Failed API call to {url}")

    return valid_resp(response.json())

async def start_ping(proxy):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            await ping(proxy)
            break
        except Exception as e:
            retries += 1
            logger.error(f"Ping failed for proxy {proxy}: {e}, retry {retries}/{MAX_RETRIES}")
            if retries >= MAX_RETRIES:
                handle_ping_fail(proxy)
            await asyncio.sleep(5)

async def ping(proxy):
    global RETRIES, status_connect

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time())
        }

        response = call_api(DOMAIN_API["PING"], data, proxy)
        if response["code"] == 0:
            logger.info(f"Ping successful via proxy {proxy}: {response}")
            RETRIES = 0
            status_connect = CONNECTION_STATES["CONNECTED"]
        else:
            handle_ping_fail(proxy, response)
    except Exception as e:
        logger.error(f"Ping failed via proxy {proxy}: {e}")
        handle_ping_fail(proxy, None)

def handle_ping_fail(proxy, response=None):
    global RETRIES, status_connect

    RETRIES += 1
    if RETRIES >= MAX_RETRIES:
        status_connect = CONNECTION_STATES["DISCONNECTED"]
        logger.warning(f"Proxy {proxy} failed after {MAX_RETRIES} retries. Removing proxy from list.")
        remove_proxy_from_list(proxy)

def handle_logout(proxy):
    global token_info, status_connect, account_info

    token_info = None
    status_connect = CONNECTION_STATES["NONE_CONNECTION"]
    account_info = {}
    save_status(proxy, None)
    logger.info(f"Logged out and cleared session info for proxy {proxy}")

def load_proxies(proxy_file):
    try:
        with open(proxy_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except Exception as e:
        logger.error(f"Failed to load proxies: {e}")
        raise SystemExit("Exiting due to failure in loading proxies")

def save_status(proxy, status):
    pass

def save_session_info(proxy, data):
    pass

def load_session_info(proxy):
    return {}

def is_valid_proxy(proxy):
    return True

def remove_proxy_from_list(proxy):
    pass

async def main():
    load_token()
    print_welcome_message()  # Menampilkan pesan "BACTIAR"

    with open('proxy.txt', 'r') as f:
        all_proxies = f.read().splitlines()

    active_proxies = [proxy for proxy in all_proxies[:MAX_PROXIES] if is_valid_proxy(proxy)]
    tasks = {asyncio.create_task(render_profile_info(proxy)): proxy for proxy in active_proxies}

    while True:
        done, pending = await asyncio.wait(tasks.keys(), return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            failed_proxy = tasks[task]
            if task.result() is None:
                logger.info(f"Removing and replacing failed proxy: {failed_proxy}")
                active_proxies.remove(failed_proxy)
                if all_proxies:
                    new_proxy = all_proxies.pop(0)
                    if is_valid_proxy(new_proxy):
                        active_proxies.append(new_proxy)
                        new_task = asyncio.create_task(render_profile_info(new_proxy))
                        tasks[new_task] = new_proxy
            tasks.pop(task)

        for proxy in set(active_proxies) - set(tasks.values()):
            new_task = asyncio.create_task(render_profile_info(proxy))
            tasks[new_task] = proxy

        await asyncio.sleep(3)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program terminated by user.")
