# MCP Server Evaluation Guide

Comprehensive guide for evaluating and testing MCP servers to ensure quality and effectiveness.

---

## Table of Contents

1. [Evaluation Overview](#1-evaluation-overview)
2. [Test Scenarios](#2-test-scenarios)
3. [Performance Testing](#3-performance-testing)
4. [Error Handling Tests](#4-error-handling-tests)
5. [Integration Testing](#5-integration-testing)
6. [Evaluation Metrics](#6-evaluation-metrics)
7. [Test Harness Setup](#7-test-harness-setup)

---

## 1. Evaluation Overview

### Why Evaluation Matters

MCP server quality is measured by how well it enables LLMs to accomplish real-world tasks. Evaluation helps ensure:

- **Functionality**: Tools work as expected
- **Reliability**: Consistent behavior under various conditions
- **Performance**: Acceptable response times
- **Usability**: Clear error messages and guidance

### Evaluation Approach

Use **Evaluation-Driven Development**:
1. Create realistic evaluation scenarios early
2. Let agent feedback drive tool improvements
3. Prototype quickly and iterate based on actual performance

---

## 2. Test Scenarios

### Basic Functionality Tests

```python
# Test 1: Get single resource
result = await server.execute_tool('get_user', {'user_id': '123'})
assert result['success'] is True
assert result['id'] == '123'

# Test 2: Search with filters
result = await server.execute_tool('search_users', {
    'query': 'john',
    'limit': 10
})
assert 'results' in result
assert len(result['results']) <= 10

# Test 3: Create resource
result = await server.execute_tool('create_user', {
    'name': 'John Doe',
    'email': 'john@example.com'
})
assert result['success'] is True
assert 'id' in result
```

### Edge Case Tests

```python
# Empty results
result = await server.execute_tool('search_users', {'query': 'nonexistent'})
assert result['results'] == []

# Maximum limits
result = await server.execute_tool('search_users', {'limit': 100})
assert len(result['results']) <= 100

# Special characters in input
result = await server.execute_tool('search_users', {'query': "O'Brien"})
assert result['success'] is True
```

### Workflow Tests

Test complete user workflows:

```python
async def test_user_creation_workflow(server):
    """Test complete user creation and retrieval workflow."""
    
    # 1. Create user
    create_result = await server.execute_tool('create_user', {
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert create_result['success'] is True
    user_id = create_result['id']
    
    # 2. Get user
    get_result = await server.execute_tool('get_user', {
        'user_id': user_id
    })
    assert get_result['name'] == 'Test User'
    
    # 3. Update user
    update_result = await server.execute_tool('update_user', {
        'user_id': user_id,
        'name': 'Updated Name'
    })
    assert update_result['success'] is True
    
    # 4. Verify update
    get_result = await server.execute_tool('get_user', {
        'user_id': user_id
    })
    assert get_result['name'] == 'Updated Name'
```

---

## 3. Performance Testing

### Response Time Tests

```python
import time
import statistics

async def test_response_times(server, db_connection):
    """Test response times for various operations."""
    
    test_cases = [
        ('get_user', {'user_id': 'test-1'}),
        ('search_users', {'query': 'test', 'limit': 10}),
        ('list_users', {'page': 1, 'per_page': 50})
    ]
    
    results = []
    for tool_name, params in test_cases:
        times = []
        for _ in range(10):
            start = time.time()
            await server.execute_tool(tool_name, params)
            times.append(time.time() - start)
        
        results.append({
            'tool': tool_name,
            'avg': statistics.mean(times),
            'min': min(times),
            'max': max(times),
            'p95': sorted(times)[int(len(times) * 0.95)]
        })
    
    # Assert performance targets
    for r in results:
        assert r['avg'] < 1.0, f"{r['tool']} avg {r['avg']:.3f}s > 1.0s"
        assert r['p95'] < 2.0, f"{r['tool']} p95 {r['p95']:.3f}s > 2.0s"
```

### Concurrency Tests

```python
import asyncio
import statistics

async def test_concurrent_execution(server):
    """Test performance under concurrent load."""
    
    async def execute_tool():
        start = time.time()
        await server.execute_tool('get_user', {'user_id': 'test-1'})
        return time.time() - start
    
    # Test with various concurrency levels
    for concurrency in [1, 5, 10, 20]:
        tasks = [execute_tool() for _ in range(concurrency)]
        
        start = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start
        
        avg_time = statistics.mean(results)
        
        print(f"Concurrency {concurrency}: {total_time:.2f}s total, {avg_time:.3f}s avg")
        
        # Assert reasonable performance
        assert total_time < 10.0, f"Total time {total_time:.2f}s too high for {concurrency} requests"
```

### Scalability Tests

```python
async def test_scalability(server, db_connection):
    """Test how performance scales with data size."""
    
    data_sizes = [100, 500, 1000, 2000]
    response_times = []
    
    for size in data_sizes:
        # Setup: Create test data
        await setup_test_data(db_connection, size)
        
        # Measure query time
        start = time.time()
        result = await server.execute_tool('search_users', {'query': 'test'})
        response_time = time.time() - start
        
        response_times.append(response_time)
        print(f"Data size {size}: {response_time:.3f}s")
    
    # Assert reasonable scaling (not exponential)
    for i in range(1, len(response_times)):
        ratio = response_times[i] / response_times[i-1]
        assert ratio < 3.0, f"Scaling ratio {ratio:.2f} too high between {data_sizes[i-1]} and {data_sizes[i]}"
```

---

## 4. Error Handling Tests

### Authentication Errors

```python
async def test_authentication_errors(server):
    """Test handling of authentication failures."""
    
    # Test with invalid credentials
    result = await server.execute_tool('get_user', {
        'user_id': '123',
        'api_key': 'invalid'
    })
    
    assert result['success'] is False
    assert 'auth' in result['error'].lower() or 'credential' in result['error'].lower()
    assert 'suggestion' in result  # Helpful guidance

# Test with expired token
async def test_expired_token(server):
    result = await server.execute_tool('get_user', {
        'user_id': '123',
        'api_key': 'expired_token'
    })
    
    assert result['success'] is False
    assert 'expired' in result['error'].lower()
    assert 'refresh' in result.get('suggestion', '').lower()
```

### Rate Limiting Tests

```python
async def test_rate_limiting(server):
    """Test rate limit handling."""
    
    # Make many rapid requests
    results = []
    for i in range(100):
        result = await server.execute_tool('search_users', {'query': f'test{i}'})
        results.append(result)
    
    # Find rate-limited request
    rate_limited = [r for r in results if not r.get('success') and 'rate' in r.get('error', '').lower()]
    
    if rate_limited:
        # Verify proper rate limit response
        rl = rate_limited[0]
        assert 'retry' in rl.get('suggestion', '').lower() or 'retry_after' in rl
```

### Validation Error Tests

```python
async def test_validation_errors(server):
    """Test input validation error handling."""
    
    test_cases = [
        ('get_user', {'user_id': ''}, 'required'),
        ('search_users', {'limit': -1}, 'greater than 0'),
        ('search_users', {'query': 'x' * 500}, 'shorter')
    ]
    
    for tool, params, expected_hint in test_cases:
        result = await server.execute_tool(tool, params)
        
        assert result['success'] is False
        assert 'error' in result
        assert expected_hint.lower() in result.get('suggestion', '').lower()
```

---

## 5. Integration Testing

### LLM Integration Tests

```python
async def test_llm_can_use_tools(server, llm_client):
    """Test that an LLM can successfully use the tools."""
    
    # Provide tools to LLM
    tools = await server.list_tools()
    
    # Simulate LLM decision-making
    prompt = f"Find user with email 'test@example.com'"
    
    # LLM should decide to use search_users
    tool_call = await llm_client.decide_tool(prompt, tools)
    
    # Execute tool
    result = await server.execute_tool(tool_call.name, tool_call.arguments)
    
    # Verify LLM can interpret results
    assert result['success'] is True

### Multi-Tool Workflow

async def test_multi_tool_workflow(server, llm_client):
    """Test complex workflows requiring multiple tools."""
    
    workflow = """
    1. Search for users named 'John'
    2. Get details of the first user
    3. Update the user's profile
    4. Verify the update
    """
    
    # This would involve multiple tool calls and LLM reasoning
    results = await execute_workflow(server, llm_client, workflow)
    
    assert all(r['success'] for r in results)
```

---

## 6. Evaluation Metrics

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Success Rate** | % of calls that succeed | > 95% |
| **Avg Response Time** | Mean response time | < 1s |
| **P95 Response Time** | 95th percentile | < 2s |
| **Error Recovery** | Can recover from errors | 100% |
| **LLM Pass-through** | LLM can use results | > 90% |

### Quality Score Calculation

```python
def calculate_quality_score(test_results: dict) -> float:
    """Calculate overall quality score."""
    
    scores = {
        'functionality': test_results['success_rate'] * 100,
        'performance': max(0, 100 - (test_results['avg_time'] * 100)),
        'error_handling': test_results['error_recovery_rate'] * 100,
        'usability': test_results['llm_success_rate'] * 100
    }
    
    # Weighted average
    weights = {'functionality': 0.4, 'performance': 0.2, 'error_handling': 0.2, 'usability': 0.2}
    
    return sum(scores[k] * weights[k] for k in weights)
```

---

## 7. Test Harness Setup

### Basic Test Fixture

```python
import pytest
import asyncio
from mcp.server.stdio import StdioServerTransport

@pytest.fixture
async def mcp_server():
    """Create an MCP server instance for testing."""
    from my_server import create_server
    
    server = create_server()
    transport = StdioServerTransport()
    
    return TestMCPserver(server, transport)


class TestMCPserver:
    def __init__(self, server, transport):
        self.server = server
        self.transport = transport
    
    async def execute_tool(self, name: str, arguments: dict):
        """Execute a tool and return results."""
        # Implementation depends on server type
        pass
```

### Running Evaluations

```bash
# Run all evaluations
pytest tests/evaluation.py -v

# Run specific test category
pytest tests/evaluation.py -k "performance" -v

# Run with coverage
pytest tests/evaluation.py --cov=my_server --cov-report=html
```

---

## Example: Complete Evaluation Suite

```python
"""
MCP Server Evaluation Suite
"""

import pytest
import asyncio
import time
from typing import Any


class TestBasicFunctionality:
    """Basic functionality tests."""
    
    @pytest.mark.asyncio
    async def test_get_user(self, server):
        result = await server.execute_tool('get_user', {'user_id': '123'})
        assert result['success'] is True
        assert 'id' in result
    
    @pytest.mark.asyncio
    async def test_search_users(self, server):
        result = await server.execute_tool('search_users', {
            'query': 'test',
            'limit': 10
        })
        assert 'results' in result
        assert len(result['results']) <= 10
    
    @pytest.mark.asyncio
    async def test_create_user(self, server):
        result = await server.execute_tool('create_user', {
            'name': 'Test User',
            'email': 'test@example.com'
        })
        assert result['success'] is True


class TestPerformance:
    """Performance tests."""
    
    @pytest.mark.asyncio
    async def test_response_time(self, server):
        times = []
        for _ in range(10):
            start = time.time()
            await server.execute_tool('get_user', {'user_id': '123'})
            times.append(time.time() - start)
        
        avg = sum(times) / len(times)
        assert avg < 1.0, f"Average response time {avg:.3f}s exceeds 1s"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, server):
        tasks = [
            server.execute_tool('get_user', {'user_id': f'{i}'})
            for i in range(10)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # All should succeed or fail gracefully
        assert len(results) == 10


class TestErrorHandling:
    """Error handling tests."""
    
    @pytest.mark.asyncio
    async def test_not_found_error(self, server):
        result = await server.execute_tool('get_user', {'user_id': 'nonexistent'})
        
        assert result['success'] is False
        assert 'suggestion' in result
    
    @pytest.mark.asyncio
    async def test_validation_error(self, server):
        result = await server.execute_tool('get_user', {'user_id': ''})
        
        assert result['success'] is False
        assert 'required' in result.get('error', '').lower()


# Run with: pytest tests/ -v
```

---

## Quality Checklist

- [ ] Basic functionality tests pass
- [ ] Edge cases handled gracefully
- [ ] Response times meet targets (< 1s average, < 2s p95)
- [ ] Concurrency handled properly
- [ ] Authentication errors handled
- [ ] Rate limiting handled
- [ ] Validation errors are informative
- [ ] Error messages include suggestions
- [ ] Integration with LLM tested
- [ ] Multi-tool workflows work end-to-end
- [ ] Performance scales with data size

---

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Microsoft MCP for Beginners - Testing](https://github.com/microsoft/mcp-for-beginners)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
