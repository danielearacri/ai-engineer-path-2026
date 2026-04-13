import asyncio
import time
import requests
import httpx

URL = "https://httpbin.org/delay/1"
N = 5

# VERSIONE SYNC
def sync_requests():
    start = time.time()
    for i in range(N):
        requests.get(URL)
        print(f"Richiesta sync {i+1} completata")
    end = time.time()
    print(f"\nTempo SYNC: {end - start:.2f} secondi\n")

# VERSIONE ASYNC
async def fetch(client, i):
    await client.get(URL)
    print(f"Richiesta async {i+1} completata")

async def async_requests():
    start = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        await asyncio.gather(*[fetch(client, i) for i in range(N)])
    end = time.time()
    print(f"Tempo ASYNC: {end - start:.2f} secondi")

# ESEGUI ENTRAMBE
sync_requests()
asyncio.run(async_requests())



