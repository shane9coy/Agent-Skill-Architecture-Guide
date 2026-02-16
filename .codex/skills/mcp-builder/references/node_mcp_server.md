# Node.js/TypeScript MCP Server Implementation Guide

Complete guide for building MCP servers using TypeScript and the MCP TypeScript SDK.

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Server Initialization](#2-server-initialization)
3. [Tool Registration](#3-tool-registration)
4. [Input Validation with Zod](#4-input-validation-with-zod)
5. [Structured Output](#5-structured-output)
6. [Resources and Prompts](#6-resources-and-prompts)
7. [Error Handling](#7-error-handling)
8. [Testing and Running](#8-testing-and-running)
9. [Quality Checklist](#9-quality-checklist)

---

## 1. Project Setup

### Installation

```bash
npm install @modelcontextprotocol/server @modelcontextprotocol/sdk zod
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Basic Project Structure

```
my-mcp-server/
├── src/
│   ├── index.ts          # Main entry point
│   ├── tools/            # Tool implementations
│   │   └── userTools.ts
│   ├── schemas/          # Zod schemas
│   │   └── userSchemas.ts
│   └── utils/            # Shared utilities
│       └── apiClient.ts
├── package.json
├── tsconfig.json
└── README.md
```

---

## 2. Server Initialization

### Using McpServer (High-Level API)

```typescript
import { McpServer } from '@modelcontextprotocol/server';

const server = new McpServer({
  name: 'my-server',
  version: '1.0.0'
});

// Run with stdio
import { StdioServerTransport } from '@modelcontextprotocol/server';

const transport = new StdioServerTransport();
await server.run(transport);
```

### With Capabilities

```typescript
import { McpServer, StdioServerTransport } from '@modelcontextprotocol/server';

const server = new McpServer(
  { name: 'my-server', version: '1.0.0' },
  {
    capabilities: {
      resources: {},
      tools: {},
      prompts: {}
    }
  }
);

const transport = new StdioServerTransport();
await server.run(transport);
```

### Low-Level Server Setup

```typescript
import { Server } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server';
import { CallToolResult } from '@modelcontextprotocol/server';

const server = new Server(
  { name: 'my-server', version: '1.0.0' },
  {
    capabilities: {
      tools: {}
    }
  }
);

const transport = new StdioServerTransport();
await server.run(transport);
```

---

## 3. Tool Registration

### Using server.registerTool()

```typescript
import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';

const server = new McpServer({ name: 'my-server', version: '1.0.0' });

server.registerTool(
  'get-user',
  {
    title: 'Get User',
    description: 'Get user by ID. Use when you need user information.',
    inputSchema: z.object({
      userId: z.string().describe('User ID')
    })
  },
  async ({ userId }): Promise<CallToolResult> => {
    // Implementation
    return {
      content: [{ type: 'text', text: JSON.stringify({ id: userId, name: 'John' }) }]
    };
  }
);
```

### Using High-Level API (server.tool())

```typescript
// Simplified high-level API
server.tool('get-user', { userId: z.string() }, async ({ userId }) => {
  return { content: [{ type: 'text', text: 'result' }] };
});
```

### Low-Level Tool Registration

```typescript
import { Server } from '@modelcontextprotocol/server';
import { z } from 'zod';

const server = new Server({ name: 'my-server', version: '1.0.0' }, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'get-user',
        description: 'Get user by ID',
        inputSchema: {
          type: 'object',
          properties: {
            userId: { type: 'string', description: 'User ID' }
          },
          required: ['userId']
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'get-user') {
    return {
      content: [{ type: 'text', text: JSON.stringify({ id: args.userId }) }]
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});
```

---

## 4. Input Validation with Zod

### Basic Schema Definition

```typescript
import { z } from 'zod';

const UserSearchParams = z.object({
  query: z.string()
    .min(1, "Query must be at least 1 character")
    .max(200, "Query must be at most 200 characters")
    .describe("Search query for finding users"),
  limit: z.number()
    .min(1, "Limit must be at least 1")
    .max(100, "Limit must be at most 100")
    .default(10)
    .describe("Maximum number of results"),
  includeInactive: z.boolean()
    .default(false)
    .describe("Include inactive users in results")
});

type UserSearchParams = z.infer<typeof UserSearchParams>;
```

### Schema with Descriptions

```typescript
const CreateUserParams = z.object({
  name: z.string()
    .min(1)
    .describe("User's full name"),
  email: z.string()
    .email()
    .describe("User's email address"),
  role: z.enum(['admin', 'user', 'guest'])
    .default('user')
    .describe("User's role")
});
```

### Strict Schema Validation

```typescript
const StrictUserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email()
}).strict();  // Rejects extra fields
```

### Using with Tool Registration

```typescript
server.registerTool(
  'search-users',
  {
    title: 'Search Users',
    description: 'Search for users by name or email',
    inputSchema: UserSearchParams
  },
  async (params: UserSearchParams) => {
    const { query, limit, includeInactive } = params;
    // Implementation
    return { content: [{ type: 'text', text: 'results' }] };
  }
);
```

---

## 5. Structured Output

### Basic Text Output

```typescript
server.registerTool(
  'get-weather',
  { inputSchema: z.object({ city: z.string() }) },
  async ({ city }) => {
    const weather = { temp: 22, condition: 'sunny' };
    return {
      content: [{ type: 'text', text: `Weather in ${city}: ${weather.temp}°C, ${weather.condition}` }]
    };
  }
);
```

### Structured Content Output

```typescript
import { CallToolResult } from '@modelcontextprotocol/server';

server.registerTool(
  'get-weather',
  {
    title: 'Get Weather',
    description: 'Get weather for a city',
    inputSchema: z.object({
      city: z.string().describe('City name')
    }),
    outputSchema: z.object({
      temperature: z.number(),
      condition: z.string(),
      humidity: z.number()
    })
  },
  async ({ city }): Promise<CallToolResult> => {
    const weather = { temperature: 22, condition: 'sunny', humidity: 45 };

    return {
      content: [{ type: 'text', text: JSON.stringify(weather) }],
      structuredContent: weather
    };
  }
);
```

### Output Schema Types

```typescript
// Object output
outputSchema: z.object({
  id: z.string(),
  name: z.string(),
  items: z.array(z.string())
})

// Array output
outputSchema: z.array(z.object({
  id: z.string(),
  name: z.string()
}))

// Primitive output
outputSchema: z.string()
// or
outputSchema: z.number()
```

---

## 6. Resources and Prompts

### Registering Resources

```typescript
server.registerResource(
  'config',
  'config://app',
  {
    title: 'App Configuration',
    description: 'Application settings',
    mimeType: 'application/json'
  },
  async () => {
    return JSON.stringify({ version: '1.0.0', debug: false });
  }
);
```

### Resource Templates

```typescript
server.registerResourceTemplate(
  'user-data',
  'users://{userId}',
  {
    title: 'User Data',
    description: 'Get user data by ID'
  },
  async ({ userId }) => {
    const user = await getUser(userId);
    return JSON.stringify(user);
  }
);
```

### Registering Prompts

```typescript
server.registerPrompt(
  'user-summary',
  {
    title: 'User Summary',
    description: 'Generate a user summary',
    arguments: [
      {
        name: 'userId',
        description: 'User ID to summarize',
        required: true
      }
    ]
  },
  async ({ userId }) => {
    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Summarize user ${userId}`
          }
        }
      ]
    };
  }
);
```

---

## 7. Error Handling

### Tool Error Responses

```typescript
server.registerTool(
  'get-user',
  {
    inputSchema: z.object({ userId: z.string() })
  },
  async ({ userId }): Promise<CallToolResult> => {
    try {
      const user = await fetchUser(userId);
      return {
        content: [{ type: 'text', text: JSON.stringify(user) }],
        structuredContent: user
      };
    } catch (error) {
      if (error.code === 'NOT_FOUND') {
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: `User '${userId}' not found`,
              suggestion: 'Check the user ID and try again'
            })
          }]
        };
      }

      if (error.code === 'RATE_LIMIT') {
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: 'Rate limit exceeded',
              retryAfter: error.retryAfter,
              suggestion: `Wait ${error.retryAfter} seconds before retrying`
            })
          }]
        };
      }

      throw error;
    }
  }
);
```

### Error Response Format

```typescript
interface ErrorResponse {
  success: false;
  error: string;
  suggestion?: string;
  retryAfter?: number;
}
```

---

## 8. Testing and Running

### Important: Server Process Behavior

> **Warning:** MCP servers are long-running processes that wait for requests over stdio/stdin or SSE/HTTP. Running them directly (e.g., `node dist/index.js`) will cause your process to hang indefinitely.

### Safe Testing Methods

**Using tmux:**
```bash
# Run server in tmux
tmux new -s mcp-server
npm run build && node dist/index.js
# Detach: Ctrl+b, then d

# Test in separate terminal
# Then kill when done
tmux kill-session -t mcp-server
```

**Using timeout:**
```bash
timeout 5s node dist/index.js
```

### Build Process

```json
// package.json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc && node dist/index.js"
  }
}
```

### Syntax Verification

```bash
# Type check without emitting
npx tsc --noEmit

# Build
npm run build
```

---

## 9. Quality Checklist

- [ ] Using MCP TypeScript SDK with proper tool registration
- [ ] Zod schemas with `.strict()` where appropriate
- [ ] TypeScript strict mode enabled
- [ ] No `any` types - use proper types
- [ ] Explicit `Promise<T>` return types
- [ ] Build process configured (`npm run build`)
- [ ] All tools have comprehensive descriptions
- [ ] Input validation on all tool parameters
- [ ] Structured output defined for tools
- [ ] Error handling with actionable messages
- [ ] Both structuredContent and text content returned
- [ ] Tests verify functionality

---

## Example: Complete Server

```typescript
/**
 * Example MCP Server - Weather Service
 */

import { McpServer, StdioServerTransport } from '@modelcontextprotocol/server';
import { z } from 'zod';
import { CallToolResult } from '@modelcontextprotocol/server';

// Constants
const CHARACTER_LIMIT = 25000;
const API_BASE_URL = 'https://api.weather.example.com';

// Input Schemas
const WeatherSearchParams = z.object({
  city: z.string().min(1).describe('City name'),
  units: z.enum(['metric', 'imperial']).default('metric').describe('Units')
});

type WeatherSearchParams = z.infer<typeof WeatherSearchParams>;

// Server Initialization
const server = new McpServer({
  name: 'weather-server',
  version: '1.0.0'
}, {
  capabilities: {
    tools: {}
  }
});

// Register Tools
server.registerTool(
  'get-weather',
  {
    title: 'Get Weather',
    description: 'Get current weather for a city. Use when you need weather information.',
    inputSchema: WeatherSearchParams,
    outputSchema: z.object({
      city: z.string(),
      temperature: z.number(),
      condition: z.string(),
      humidity: z.number()
    })
  },
  async ({ city, units }): Promise<CallToolResult> => {
    // Fetch weather (simulated)
    const weather = {
      city,
      temperature: units === 'metric' ? 22 : 72,
      condition: 'sunny',
      humidity: 45
    };

    return {
      content: [{ type: 'text', text: JSON.stringify(weather) }],
      structuredContent: weather
    };
  }
);

// Run Server
async function main() {
  const transport = new StdioServerTransport();
  await server.run(transport);
}

main().catch(console.error);
```

---

## Additional Resources

- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Zod Documentation](https://zod.dev/)
- [MCP Specification](https://modelcontextprotocol.io/)
