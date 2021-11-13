from fastapi import FastAPI
from pokeapi_client import PokeapiClient, PokemonResponse

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

app = FastAPI()

resource = Resource(attributes={"service.name": "fastapi-tracing-demo"})
tracer = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer)
tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://tempo:4317")))

LoggingInstrumentor().instrument()
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)

@app.get("/pokemon/{pokemon_name}")
async def get_pokemon_info(pokemon_name: str):
    return await PokeapiClient.retrieve_pokemon_info(pokemon_name)
