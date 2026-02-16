# MCP Best Practices

Core guidelines for building high-quality MCP servers that enable LLMs to effectively interact with external services.

---

## Table of Contents

1. [Agent-Centric Design Principles](#1-agent-centric-design-principles)
2. [Tool Design Guidelines](#2-tool-design-guidelines)
3. [Input/Output Design](#3-inputoutput-design)
4. [Error Handling](#4-error-handling)
5. [Response Formatting](#5-response-formatting)
6. [Performance Considerations](#6-performance-considerations)
7. [Security Best Practices](#7-security-best-practices)

---

## 1. Agent-Centric Design Principles

### Build for Workflows, Not Just API Endpoints

Don't simply wrap existing API endpoints — build thoughtful, high-impact workflow tools:

- **Consolidate related operations**: Create tools that do multiple things in sequence (e.g., `schedule_event` that both checks availability AND creates the event)
- **Focus on complete tasks**: Tools should enable complete workflows, not just individual API calls
- **Consider agent workflows**: Think about what tasks agents actually need to accomplish

### Optimize for Limited Context

Agents have constrained context windows — make every token count:

- **Return high-signal information**: Not exhaustive data dumps
- **Provide response format options**: Offer "concise" vs "detailed" response formats
- **Use human-readable identifiers**: Names over IDs where possible
- **Respect context budget**: Treat tokens as a scarce resource

### Design Actionable Error Messages

Error messages should guide agents toward correct usage:

- **Suggest specific next steps**: "Try using filter='active_only' to reduce results"
- **Make errors educational**: Not just diagnostic, but informative
- **Help agents learn**: Clear feedback helps proper tool usage

### Follow Natural Task Subdivisions

- **Use natural naming**: Tool names should reflect how humans think about tasks
- **Group with prefixes**: Related tools should have consistent prefixes for discoverability
- **Design around workflows**: Structure tools around natural task flows, not API structure

---

## 2. Tool Design Guidelines

### Tool Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| Verb_Noun | `get_user`, `create_file` | Single action tools |
| Verb_Noun_Noun | `send_email_notification` | Specific actions |
| Search_Filter | `search_products` | Query tools |

### Tool Definition Structure

Each tool should have:

```typescript
{
  name: "tool_name",
  description: "Clear description of what the tool does and when to use it",
  inputSchema: {
    // JSON Schema definition
  }
}
```

### Tool Annotations

Use annotations to provide hints to the LLM:

| Annotation | Use Case |
|------------|-----------|
| `readOnlyHint: true` | For read-only operations |
| `destructiveHint: false` | For non-destructive operations |
| `idempotentHint: true` | If repeated calls have same effect |
| `openWorldHint: true` | If interacting with external systems |

---

## 3. Input/Output Design

### Input Schema Best Practices

**Use Strong Typing:**
- Pydantic models (Python) or Zod schemas (TypeScript)
- Include proper constraints (min/max length, regex patterns, ranges)
- Provide clear, descriptive field descriptions
- Include diverse examples in field descriptions

**Example (Python/Pydantic):**
```python
class SearchParams(BaseModel):
    query: str = Field(min_length=1, max_length=200, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    filter_active: bool = Field(default=True, description="Filter to active items only")
```

**Example (TypeScript/Zod):**
```typescript
const SearchParams = z.object({
  query: z.string().min(1).max(200).describe("Search query"),
  limit: z.number().min(1).max(100).default(10).describe("Max results"),
  filter_active: z.boolean().default(true).describe("Filter to active items only")
});
```

### Output Schema Best Practices

- **Provide structured output** when possible
- **Include relevant metadata** (timestamps, IDs, counts)
- **Be consistent** across similar operations
- **Support both JSON and text** formats when appropriate

---

## 4. Error Handling

### Error Message Guidelines

**Do:**
- Use clear, natural language
- Explain what went wrong
- Suggest corrective actions
- Include relevant context

**Don't:**
- Use technical jargon
- Expose internal error details
- Leave agents guessing

### Error Response Format

```python
# Good error response
{
    "success": False,
    "error": "No results found for query 'invalid'",
    "suggestion": "Try a more general search term or check spelling"
}

# Good error with specific guidance
{
    "success": False,
    "error": "Rate limit exceeded",
    "retry_after": 60,
    "suggestion": "Wait 60 seconds or use batch operations"
}
```

### Common Error Scenarios

| Scenario | Handling |
|----------|----------|
| Authentication failure | Clear message about re-authenticating |
| Rate limiting | Include retry-after time |
| Invalid input | Show valid input formats |
| Resource not found | Suggest alternative searches |
| Network errors | Provide retry guidance |

---

## 5. Response Formatting

### Concise vs Detailed Modes

Provide options for response verbosity:

```python
class ResponseFormat:
    CONCISE = "concise"  # Summary of results
    DETAILED = "detailed"  # Full result with metadata
    VERBOSE = "verbose"  # Everything including debug info
```

### Character Limits and Truncation

- **Implement limits**: Default to 25,000 tokens
- **Truncate gracefully**: Show first N results with count of remaining
- **Provide pagination**: Allow fetching more results

### Response Consistency

Similar operations should return similar formats:

| Operation | Return Format |
|-----------|--------------|
| List/Get | Array of objects |
| Search | Array with total count |
| Create | Created object with ID |
| Update | Updated object |
| Delete | Confirmation with ID |

---

## 6. Performance Considerations

### Lazy Loading

- **Fetch only what's needed**: Don't pre-load all data
- **Use pagination**: Always for large datasets
- **Implement caching**: Where appropriate

### Async Operations

- **Use async/await**: For all I/O operations
- **Handle timeouts**: Set appropriate timeouts
- **Implement retries**: With exponential backoff

### Resource Management

- **Clean up connections**: Ensure proper cleanup
- **Handle concurrent requests**: Thread-safe implementations
- **Monitor memory usage**: Avoid memory leaks

---

## 7. Security Best Practices

### Input Validation

- **Validate all inputs**: Never trust client data
- **Sanitize data**: Prevent injection attacks
- **Use parameterized queries**: For database operations

### Authentication

- **Secure credential storage**: Never hardcode secrets
- **Use environment variables**: For sensitive config
- **Implement token refresh**: Handle expired tokens

### Rate Limiting

- **Implement client-side limits**: Prevent abuse
- **Respect server limits**: Handle 429 responses gracefully
- **Queue requests**: When appropriate

---

## Quality Checklist

- [ ] Tools follow natural task subdivisions
- [ ] Input schemas use strong typing with examples
- [ ] Error messages are actionable and educational
- [ ] Response formats are consistent across tools
- [ ] Character limits and truncation are implemented
- [ ] Async operations use proper patterns
- [ ] Authentication is handled securely
- [ ] Rate limiting is respected
- [ ] Documentation is comprehensive

---

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK Documentation](https://github.com/modelcontextprotocol/typescript-sdk)
