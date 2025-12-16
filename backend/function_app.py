import os
import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp()

COSMOS_DB_NAME = os.environ.get("COSMOSDB_DATABASE_NAME", "VisitorCounterDb")
COSMOS_CONTAINER_NAME = os.environ.get("COSMOSDB_CONTAINER_NAME", "Counters")
COUNTER_PARTITION_KEY = os.environ.get("COSMOSDB_PARTITION_KEY_VALUE", "1")
COUNTER_ID = os.environ.get("COSMOSDB_COUNTER_ID", "1")

_cosmos_client = None
_container_client = None


def _get_container_client():
    global _cosmos_client, _container_client

    if _container_client is not None:
        return _container_client

    conn_string = os.environ.get("COSMOSDB_CONNECTION_STRING")
    if not conn_string:
        raise RuntimeError(
            "COSMOSDB_CONNECTION_STRING is required. "
            "Set it in local.settings.json or Azure Function App settings."
        )

    _cosmos_client = CosmosClient.from_connection_string(conn_string)
    _container_client = (
        _cosmos_client.get_database_client(COSMOS_DB_NAME).get_container_client(
            COSMOS_CONTAINER_NAME
        )
    )

    return _container_client


def _ensure_counter_document() -> dict:
    container_client = _get_container_client()
    try:
        doc = container_client.read_item(COUNTER_ID, partition_key=COUNTER_PARTITION_KEY)
    except exceptions.CosmosResourceNotFoundError:
        doc = {
            "id": COUNTER_ID,
            "count": 0,
            "_partitionKey": COUNTER_PARTITION_KEY,
        }
        container_client.create_item(doc)
    # Normalize count to integer
    try:
        doc["count"] = int(doc.get("count", 0))
    except (TypeError, ValueError):
        doc["count"] = 0
    return doc


@app.route(route="counter", methods=["GET", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def get_counter(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /api/counter
    Returns the current visitor count stored in Cosmos DB.
    """
    logging.info("get_counter triggered")
    
    # Handle CORS preflight request
    if req.method == "OPTIONS":
        return func.HttpResponse(
            "",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept"
            }
        )
    
    try:
        container_client = _get_container_client()
        counter_doc = _ensure_counter_document()
    except Exception as exc:  # pragma: no cover - safeguard logging
        logging.exception("Failed to fetch counter.")
        return func.HttpResponse(
            json.dumps({"error": "Failed to read counter", "details": str(exc)}),
            status_code=500,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept"
            }
        )

    return func.HttpResponse(
        json.dumps({"count": counter_doc["count"]}),
        mimetype="application/json",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept"
        }
    )


@app.route(route="counter/increment", methods=["POST", "OPTIONS"], auth_level=func.AuthLevel.ANONYMOUS)
def increment_counter(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /api/counter/increment
    Increments the visitor count stored in Cosmos DB and returns the new value.
    """
    logging.info("increment_counter triggered")
    
    # Handle CORS preflight request
    if req.method == "OPTIONS":
        return func.HttpResponse(
            "",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept"
            }
        )
    
    try:
        container_client = _get_container_client()
        counter_doc = _ensure_counter_document()
        counter_doc["count"] += 1
        container_client.replace_item(item=COUNTER_ID, body=counter_doc)
    except Exception as exc:  # pragma: no cover - safeguard logging
        logging.exception("Failed to increment counter.")
        return func.HttpResponse(
            json.dumps({"error": "Failed to increment counter", "details": str(exc)}),
            status_code=500,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Accept"
            }
        )

    return func.HttpResponse(
        json.dumps({"count": counter_doc["count"]}),
        mimetype="application/json",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept"
        }
    )