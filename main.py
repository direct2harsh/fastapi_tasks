from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
from db.connection import DeclarativeBase,engine
from routes import tasks,health,auth
from fastapi.middleware.cors import CORSMiddleware

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

# OTLP URL configuration, it is the service name from docker compose
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)




app = FastAPI(title="Task Management System")
PORT:int = 3216



# Connecting the OpenTelementry with FastAPI
FastAPIInstrumentor.instrument_app(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   
)

 

try:
    # DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)
except Exception as e:
    print("Error creating database metadata")
    print(e)    

app.include_router(router=tasks.router)
app.include_router(router=health.router)
app.include_router(router=auth.router)





if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0",port=PORT, reload=True,workers=10)