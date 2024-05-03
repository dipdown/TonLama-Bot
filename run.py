import asyncio
import aiohttp
from fake_useragent import UserAgent
import string
import random
import json
import hashlib

user_agent = UserAgent()
random_user_agent = user_agent.random

def rdm_addr(size=64, chars=string.hexdigits):
    return ''.join(random.choice(chars) for _ in range(size))

async def verify_user(mainaddr):
    refaddr = '0:'+rdm_addr()
    url = 'https://lama-backend-qd2o.onrender.com/user'
    headers = {
        'content-type': 'application/json',
        'user-agent': random_user_agent,
        'origin': 'https://www.tonlama.com',
        'referer': 'https://www.tonlama.com/'
    }
    data = {
        'address': refaddr,
        'refby': mainaddr
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('user'): print(f"{refaddr} reff success")
                    else: print(f"{refaddr} not success")
                else: print(f"{refaddr} request failed with status {response.status}")
        except Exception as e: print(f"{refaddr} failed:", e)

async def main():
    while True:
        tasks = []
        with open('data.txt', 'r') as file:
            for line in file:
                mainaddr = line.strip()
                task = asyncio.create_task(verify_user(mainaddr))
                tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    password_hash = "6f9886569c21a0c6c88227b2be83bb6f" 
    input_password = input("Enter password: ")
    if hashlib.md5(input_password.encode()).hexdigest() == password_hash:
        asyncio.run(main())
    else:
        print("Password Salah Blokk!!")
