from fastapi import FastAPI

from pokeapi_client import (
    PokeapiClient,
    PokemonResponse
)

app = FastAPI()

@app.get("/pokemon/{pokemon_name}")
async def get_pokemon_info(pokemon_name: str):
    return await PokeapiClient.retrieve_pokemon_info(pokemon_name)
