import httpx
import logging

from pydantic import BaseModel


class Generation(BaseModel):
    name: str

class PokemonResponse(BaseModel):
    id: int
    name: str
    generation: Generation

class PokeapiClient():
    async def retrieve_pokemon_info(pokemon_name: str):
        try:
            async with httpx.AsyncClient() as client:
                logging.info(f"Retrieving info for {pokemon_name}")
                result = await client.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/")
            result.raise_for_status()
        except httpx.HTTPError as err:
            logging.error('http error while retrieving pokemon species')
            return str(err)
        logging.info(f"HTTP RESULT -> {result}")
        return PokemonResponse(**dict(result.json()))