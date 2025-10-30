"""
MCP Server with Toy Dataset - Products Database
A simple MCP server that exposes a toy product dataset with search and query capabilities.
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    INVALID_PARAMS,
    INTERNAL_ERROR
)

# Toy dataset - simple product catalog
TOY_DATASET = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 15},
    {"id": 2, "name": "Wireless Mouse", "category": "Electronics", "price": 29.99, "stock": 50},
    {"id": 3, "name": "Desk Chair", "category": "Furniture", "price": 199.99, "stock": 8},
    {"id": 4, "name": "Monitor", "category": "Electronics", "price": 299.99, "stock": 12},
    {"id": 5, "name": "Keyboard", "category": "Electronics", "price": 79.99, "stock": 30},
    {"id": 6, "name": "Desk Lamp", "category": "Furniture", "price": 39.99, "stock": 25},
    {"id": 7, "name": "Notebook", "category": "Stationery", "price": 4.99, "stock": 100},
    {"id": 8, "name": "Pen Set", "category": "Stationery", "price": 12.99, "stock": 75},
]

# Create server instance
server = Server("toy-dataset-server")

# List available tools
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_products",
            description="Search products by name or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term for product name or category"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_product_by_id",
            description="Get a specific product by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "integer",
                        "description": "The product ID to retrieve"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="filter_by_price",
            description="Filter products by price range",
            inputSchema={
                "type": "object",
                "properties": {
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price"
                    }
                },
                "required": ["min_price", "max_price"]
            }
        ),
        Tool(
            name="get_all_products",
            description="Get all products in the dataset",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

# Handle tool calls
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "search_products":
            query = arguments.get("query", "").lower()
            results = [
                p for p in TOY_DATASET 
                if query in p["name"].lower() or query in p["category"].lower()
            ]
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "get_product_by_id":
            product_id = arguments.get("product_id")
            product = next((p for p in TOY_DATASET if p["id"] == product_id), None)
            if product:
                return [TextContent(
                    type="text",
                    text=json.dumps(product, indent=2)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"Product with ID {product_id} not found"
                )]
        
        elif name == "filter_by_price":
            min_price = arguments.get("min_price", 0)
            max_price = arguments.get("max_price", float('inf'))
            results = [
                p for p in TOY_DATASET 
                if min_price <= p["price"] <= max_price
            ]
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )]
        
        elif name == "get_all_products":
            return [TextContent(
                type="text",
                text=json.dumps(TOY_DATASET, indent=2)
            )]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

# List available resources
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="dataset://products/all",
            name="All Products",
            mimeType="application/json",
            description="Complete product catalog dataset"
        ),
        Resource(
            uri="dataset://products/stats",
            name="Dataset Statistics",
            mimeType="application/json",
            description="Statistics about the product dataset"
        )
    ]

# Handle resource requests
@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "dataset://products/all":
        return json.dumps(TOY_DATASET, indent=2)
    
    elif uri == "dataset://products/stats":
        stats = {
            "total_products": len(TOY_DATASET),
            "categories": list(set(p["category"] for p in TOY_DATASET)),
            "total_stock": sum(p["stock"] for p in TOY_DATASET),
            "avg_price": sum(p["price"] for p in TOY_DATASET) / len(TOY_DATASET),
            "price_range": {
                "min": min(p["price"] for p in TOY_DATASET),
                "max": max(p["price"] for p in TOY_DATASET)
            }
        }
        return json.dumps(stats, indent=2)
    
    else:
        raise ValueError(f"Unknown resource: {uri}")

# Main entry point
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())