# Python MCP Server Implementation Guide

Complete guide for building MCP servers using Python and the MCP Python SDK.

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Server Initialization](#2-server-initialization)
3. [Tool Registration](#3-tool-registration)
4. [Input Validation with Pydantic](#4-input-validation-with-pydantic)
5. [Structured Output](#5-structured-output)
6. [Resources and Prompts](#6-resources-and-prompts)
7. [Error Handling](#7-error-handling)
8. [Testing and Running](#8-testing-and-running)
9. [Quality Checklist](#9-quality-checklist)

---

## 1. Project Setup

### Installation

```bash
pip install mcp[fastmcp] pydantic
```

### Basic Project Structure

```
my-mcp-server/
├── server.py              # Main server file
├── models.py              # Pydantic models
├── tools/                 # Tool implementations
│   ├── __init__.py
│   └── user_tools.py
├── utils/                 # Shared utilities
│   ├── __init__.py
│   └── api_client.py
├── pyproject.toml
└── README.md
```

### Simple Single-File Structure

For simpler integrations, use a single file:

```python
# server.py
"""
My MCP Server - Short description
"""
import asyncio
from typing import Any

import mcp.server.stdio
from mcp.types import Tool, TextContent
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# ... implementation
```

---

## 2. Server Initialization

### Using MCPServer (High-Level API)

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("my-server")

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### Using Low-Level Server

```python
import asyncio
from typing import Any
import mcp.server.stdio
from mcp import types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

server = Server("my-server")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="my-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Tool Registration

### Using @mcp.tool() Decorator

```python
from mcp.server.mcpserver import MCPServer
from pydantic import BaseModel, Field

mcp = MCPServer("my-server")


@mcp.tool()
def get_user(user_id: str) -> dict:
    """Get user by ID - returns user data."""
    return {"id": user_id, "name": "John Doe"}


@mcp.tool()
def search_users(query: str, limit: int = 10) -> list[dict]:
    """Search for users by name or email."""
    # Implementation
    return []
```

### Low-Level Tool Registration

```python
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_user",
            description="Get user by ID",
            input_schema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"}
                },
                "required": ["user_id"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Any:
    """Handle tool calls."""
    if name == "get_user":
        return {"id": arguments["user_id"], "name": "John Doe"}
    raise ValueError(f"Unknown tool: {name}")
```

---

## 4. Input Validation with Pydantic

### Basic Model Definition

```python
from pydantic import BaseModel, Field


class UserSearchParams(BaseModel):
    query: str = Field(
        description="Search query for finding users",
        min_length=1,
        max_length=200
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results",
        ge=1,
        le=100
    )
    include_inactive: bool = Field(
        default=False,
        description="Include inactive users in results"
    )
```

### Using Models with Tools

```python
@mcp.tool()
def search_users(params: UserSearchParams) -> list[dict]:
    """Search for users based on query."""
    # Access validated parameters
    query = params.query
    limit = params.limit
    # Implementation
    return []
```

### Model Configuration

```python
from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"  # Reject extra fields
    )
    
    id: str
    name: str
    email: str
    active: bool = True
```

---

## 5. Structured Output

### Return Types Supported

| Return Type | Output |
|-------------|--------|
| `dict` | JSON object |
| `list` | JSON array |
| Pydantic Model | Structured JSON |
| `TypedDict` | Structured JSON |
| Primitive (str, int) | Wrapped in `{"result": ...}` |

### Pydantic Output Models

```python
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    temperature: float = Field(description="Temperature in Celsius")
    humidity: float = Field(description="Humidity percentage")
    condition: str
    wind_speed: float


@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Get weather for a city."""
    # Returns structured data with full schema
    return WeatherData(
        temperature=22.5,
        humidity=45.0,
        condition="sunny",
        wind_speed=5.2
    )
```

### TypedDict Output

```python
from typing import TypedDict


class LocationInfo(TypedDict):
    latitude: float
    longitude: float
    name: str


@mcp.tool()
def get_location(address: str) -> LocationInfo:
    """Get location coordinates."""
    return LocationInfo(
        latitude=51.5074,
        longitude=-0.1278,
        name="London, UK"
    )
```

### Output Schema in Low-Level Server

```python
types.Tool(
    name="get_weather",
    description="Get current weather for a city",
    input_schema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"}
        },
        "required": ["city"],
    },
    output_schema={  # Define structured output
        "type": "object",
        "properties": {
            "temperature": {"type": "number"},
            "condition": {"type": "string"},
            "humidity": {"type": "number"},
        },
        "required": ["temperature", "condition", "humidity"],
    },
)
```

---

## 6. Resources and Prompts

### Registering Resources

```python
@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri="config://app",
            name="App Configuration",
            description="Application settings",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if uri == "config://app":
        return '{"version": "1.0.0", "debug": false}'
    raise ValueError(f"Unknown resource: {uri}")
```

### Registering Prompts

```python
@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="user-summary",
            description="Generate a user summary",
            arguments=[
                types.PromptArgument(
                    name="user_id",
                    description="User ID to summarize",
                    required=True
                )
            ]
        )
    ]


@server.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Get a prompt template."""
    if name == "user-summary":
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        text=f"Summarize user {arguments['user_id']}"
                    )
                )
            ]
        )
    raise ValueError(f"Unknown prompt: {name}")
```

---

## 7. Error Handling

### Tool-Level Error Handling

```python
@mcp.tool()
def get_user(user_id: str) -> dict:
    """Get user by ID."""
    try:
        # Fetch user from API
        user = api.get_user(user_id)
        return {"success": True, "data": user}
    except NotFoundError:
        return {
            "success": False,
            "error": f"User '{user_id}' not found",
            "suggestion": "Check the user ID and try again"
        }
    except RateLimitError as e:
        return {
            "success": False,
            "error": "Rate limit exceeded",
            "retry_after": e.retry_after,
            "suggestion": f"Wait {e.retry_after} seconds before retrying"
        }
```

### Structured Error Responses

```python
class ToolError(Exception):
    def __init__(self, message: str, suggestion: str = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)
```

---

## 8. Testing and Running

### Important: Server Process Behavior

> **Warning:** MCP servers are long-running processes that wait for requests over stdio/stdin or SSE/HTTP. Running them directly (e.g., `python server.py`) will cause your process to hang indefinitely.

### Safe Testing Methods

**Using tmux:**
```bash
# Run server in tmux
tmux new -s mcp-server
python server.py
# Detach: Ctrl+b, then d

# Test in separate terminal
# Then kill when done
tmux kill-session -t mcp-server
```

**Using timeout:**
```bash
timeout 5s python server.py
```

### Syntax Verification

```bash
python -m py_compile server.py
```

### Import Verification

```python
# Check all imports work
import server
print("All imports successful")
```

---

## 9. Quality Checklist

- [ ] Using MCP Python SDK with proper tool registration
- [ ] Pydantic v2 models with `model_config`
- [ ] Type hints throughout the codebase
- [ ] Async/await for all I/O operations
- [ ] Proper imports organization
- [ ] Module-level constants (CHARACTER_LIMIT, API_BASE_URL)
- [ ] All tools have comprehensive docstrings
- [ ] Input validation on all tool parameters
- [ ] Structured output defined for tools
- [ ] Error handling with actionable messages
- [ ] Character limits and truncation implemented
- [ ] Both JSON and text response formats supported
- [ ] Tests verify functionality

---

## Example: Complete Server

```python
"""Example MCP Server - Weather Service"""

import asyncio
from typing import Any

from pydantic import BaseModel, Field
import mcp.server.stdio
from mcp import types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Constants
CHARACTER_LIMIT = 25000
API_BASE_URL = "https://api.weather.example.com"

server = Server("weather-server")


# Input Models
class WeatherSearchParams(BaseModel):
    city: str = Field(min_length=1, description="City name")
    units: str = Field(default="metric", description="Units: metric/imperial")


# Tools
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_weather",
            description="Get current weather for a city. Use when you need weather information.",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "units": {"type": "string", "default": "metric"}
                },
                "required": ["city"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Any:
    if name == "get_weather":
        city = arguments["city"]
        # Fetch weather (simulated)
        return {
            "city": city,
            "temperature": 22,
            "condition": "sunny",
            "humidity": 45
        }
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Additional Resources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MCP Specification](https://modelcontextprotocol.io/)
