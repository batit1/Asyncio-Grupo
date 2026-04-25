import asyncio
import aiohttp
import json
from datetime import datetime

APIS = [
    {
        "nombre": "Chuck Norris",
        "url": "https://api.chucknorris.io/jokes/random",
        "parser": lambda d: f"  {d['value']}",
    },
    {
        "nombre": "Foto de perro",
        "url": "https://dog.ceo/api/breeds/image/random",
        "parser": lambda d: f"  {d['message']}",
    },
    {
        "nombre": "Dato sobre gatos",
        "url": "https://catfact.ninja/fact",
        "parser": lambda d: f"  {d['fact']}",
    },
    {
        "nombre": "Dad Joke",
        "url": "https://icanhazdadjoke.com/",
        "parser": lambda d: f"  {d['joke']}",
        "headers": {"Accept": "application/json"},
    },
    {
        "nombre": " Chiste oficial",
        "url": "https://official-joke-api.appspot.com/random_joke",
        "parser": lambda d: f"  {d['setup']}\n  → {d['punchline']}",
    },
    {
        "nombre": "Predicción de edad (Fausto)",
        "url": "https://api.agify.io?name=fausto",
        "parser": lambda d: f"  El nombre '{d['name']}' tiene edad estimada: {d['age']} años",
    },
    {
        "nombre": "Albur picante",
        "url": "https://alburapi.picante.biz/",
        "parser": lambda d: f"  {d.get('albur') or d.get('text') or json.dumps(d)}",
    },
]

TIMEOUT = aiohttp.ClientTimeout(total=8)


async def fetch(session: aiohttp.ClientSession, api: dict) -> tuple[str, str]:
    headers = api.get("headers", {})
    try:
        async with session.get(api["url"], headers=headers, timeout=TIMEOUT) as resp:
            if resp.status != 200:
                return api["nombre"], f"  Error HTTP {resp.status}"
            data = await resp.json(content_type=None)
            return api["nombre"], api["parser"](data)
    except asyncio.TimeoutError:
        return api["nombre"], " Timeout: la API tardó demasiado"
    except Exception as e:
        return api["nombre"], f"  Error: {e}"

async def main():
    print("\n" + "═" * 55)
    print("   CLIENTE ASÍNCRONO DE APIS PÚBLICAS")
    print(f"   {datetime.now().strftime('%H:%M:%S')}  |  {len(APIS)} peticiones simultáneas")
    print("═" * 55 + "\n")

    inicio = asyncio.get_event_loop().time()

    async with aiohttp.ClientSession() as session:
        # Todas las peticiones se lanzan a la vez (concurrentes)
        tareas = [fetch(session, api) for api in APIS]
        resultados = await asyncio.gather(*tareas)

    fin = asyncio.get_event_loop().time()

    for nombre, contenido in resultados:
        print(f"┌─ {nombre}")
        print(f"{contenido}")
        print()

    print("═" * 55)
    print(f"  Completado en {fin - inicio:.2f} segundos")
    print("═" * 55 + "\n")

if __name__ == "__main__":
    asyncio.run(main())