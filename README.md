# MCP Toy Dataset Server

A simple Model Context Protocol (MCP) server with a toy product dataset for experimentation and learning. This server exposes product data through tools and resources that can be queried by Claude Desktop.

## Features

- **Search Products**: Search by name or category
- **Filter by Price**: Find products within a price range
- **Get Product by ID**: Retrieve specific product details
- **Dataset Statistics**: View aggregate statistics about the dataset
- **Resource Access**: Direct access to the complete dataset

## Dataset

The toy dataset includes 8 sample products across three categories:
- Electronics (Laptop, Mouse, Monitor, Keyboard)
- Furniture (Desk Chair, Desk Lamp)
- Stationery (Notebook, Pen Set)

Each product has: ID, name, category, price, and stock quantity.

## Prerequisites

- Python 3.8 or higher
- Claude Desktop application
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-directory>
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

### 3. Install MCP Python SDK

```bash
pip install mcp
```

### 4. Verify Installation

```bash
python -c "import mcp; print('MCP installed successfully!')"
```

## Configuration

### Configure Claude Desktop

1. **Locate your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Create or edit the config file** with the following content:

```json
{
  "mcpServers": {
    "toy-products": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/toy_mcp_server.py"]
    }
  }
}
```

3. **Replace the paths:**
   - Replace `/absolute/path/to/venv/bin/python` with your virtual environment's Python path
   - Replace `/absolute/path/to/toy_mcp_server.py` with the full path to the server script

**Finding your virtual environment's Python path:**

```bash
# Activate your venv first, then run:
which python  # macOS/Linux
where python  # Windows
```

**Example configurations:**

macOS:
```json
{
  "mcpServers": {
    "toy-products": {
      "command": "/Users/yourname/projects/mcp-toy-server/venv/bin/python",
      "args": ["/Users/yourname/projects/mcp-toy-server/toy_mcp_server.py"]
    }
  }
}
```

Windows:
```json
{
  "mcpServers": {
    "toy-products": {
      "command": "C:\\Users\\YourName\\projects\\mcp-toy-server\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\projects\\mcp-toy-server\\toy_mcp_server.py"]
    }
  }
}
```

4. **Save the file and restart Claude Desktop**

## Usage

Once configured, Claude Desktop will automatically start the MCP server. You don't need to run it manually.

### Verify Connection

Open Claude Desktop and look for an MCP connection indicator showing "toy-products" is connected.

### Example Queries

Try these queries in Claude Desktop to interact with the toy dataset:

#### Search Products
```
Search for electronics in the toy dataset
```

#### Filter by Price
```
Show me all products under $50
```
```
Find products between $100 and $300
```

#### Get Specific Product
```
Get details for product ID 3
```

#### View All Products
```
Show me all products in the dataset
```

#### Dataset Statistics
```
What are the statistics for the toy dataset?
```

#### Category Search
```
Show me all furniture items
```

#### Complex Queries
```
What's the most expensive item in stock?
```
```
List all electronics sorted by price
```

## Available Tools

The server provides these tools:

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `search_products` | Search by name or category | `query` (string) |
| `get_product_by_id` | Get specific product | `product_id` (integer) |
| `filter_by_price` | Filter by price range | `min_price`, `max_price` (numbers) |
| `get_all_products` | Get entire dataset | None |

## Available Resources

| Resource URI | Description |
|--------------|-------------|
| `dataset://products/all` | Complete product catalog |
| `dataset://products/stats` | Dataset statistics |

## Troubleshooting

### Server Not Starting

**Check logs:**
- macOS: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\logs\mcp*.log`

**Common issues:**

1. **ModuleNotFoundError: No module named 'mcp'**
   - Make sure you're pointing to the virtual environment's Python in the config
   - Verify MCP is installed: `pip list | grep mcp`

2. **File not found errors**
   - Use absolute paths, not relative paths
   - Verify the file path is correct

3. **Permission denied (macOS/Linux)**
   ```bash
   chmod +x toy_mcp_server.py
   ```

4. **JSON syntax error in config**
   - Validate your JSON at jsonlint.com
   - Check for missing commas or brackets

### Manual Testing

Test the server directly:

```bash
python toy_mcp_server.py
```

The server should start without errors and wait for input (it won't print anything initially).

## Customization

### Adding More Products

Edit the `TOY_DATASET` list in `toy_mcp_server.py`:

```python
TOY_DATASET = [
    {"id": 9, "name": "New Product", "category": "Category", "price": 99.99, "stock": 20},
    # Add more products...
]
```

### Adding New Tools

Add new tool definitions in the `@server.list_tools()` function and implement the logic in `@server.call_tool()`.

### Adding New Resources

Add new resources in `@server.list_resources()` and implement the logic in `@server.read_resource()`.

## Project Structure

```
.
├── toy_mcp_server.py          # Main MCP server implementation
├── README.md                   # This file
└── venv/                       # Virtual environment (not committed)
```

## Learning Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop MCP Guide](https://docs.claude.com)

## License

MIT License - Feel free to use and modify for your own projects.

## Contributing

This is a simple educational project. Feel free to fork and experiment!

## Acknowledgments

Built with the Model Context Protocol (MCP) by Anthropic.
