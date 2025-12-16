# Code Review Best Practices and Bug Patterns

## Code Quality Dimensions

When reviewing code, evaluate across these key dimensions:

### 1. Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled properly?
- Are there off-by-one errors?
- Are null/undefined values handled?
- Are async operations properly awaited?

### 2. Security
- Input validation and sanitization
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication and authorization checks
- Sensitive data exposure
- Dependency vulnerabilities
- CSRF protection
- Rate limiting

### 3. Performance
- Unnecessary loops or nested loops
- N+1 query problems
- Missing database indexes
- Inefficient algorithms (O(n²) where O(n) possible)
- Memory leaks
- Blocking operations on event loop
- Missing caching opportunities
- Large payload transfers

### 4. Maintainability
- Code clarity and readability
- Appropriate naming conventions
- DRY (Don't Repeat Yourself) principle
- Single Responsibility Principle
- Appropriate abstraction levels
- Comments explaining "why" not "what"
- Consistent code style

### 5. Testing
- Are tests included?
- Do tests cover happy paths and edge cases?
- Are error conditions tested?
- Mock/stub usage appropriate?
- Integration vs unit test balance

### 6. Error Handling
- Proper try-catch blocks
- Meaningful error messages
- Graceful degradation
- Logging of errors
- No silent failures

## Common Bug Patterns

### Concurrency Issues
```python
# BAD: Race condition
if key not in cache:
    cache[key] = compute_value()

# GOOD: Atomic operation
cache.setdefault(key, compute_value())
```

### Resource Leaks
```python
# BAD: File not closed on exception
f = open('file.txt')
data = process(f.read())
f.close()

# GOOD: Context manager ensures cleanup
with open('file.txt') as f:
    data = process(f.read())
```

### Off-by-One Errors
```javascript
// BAD: Missing last element
for (let i = 0; i < array.length - 1; i++) {
    process(array[i]);
}

// GOOD: Process all elements
for (let i = 0; i < array.length; i++) {
    process(array[i]);
}
```

### Type Coercion Issues
```javascript
// BAD: Loose equality
if (value == null) { }  // Catches both null and undefined

// GOOD: Explicit checks when needed
if (value === null || value === undefined) { }
```

### Async/Await Pitfalls
```javascript
// BAD: Not awaiting promises in loop
for (const item of items) {
    processAsync(item);  // All fire simultaneously
}

// GOOD: Sequential processing
for (const item of items) {
    await processAsync(item);
}

// BETTER: Parallel when appropriate
await Promise.all(items.map(item => processAsync(item)));
```

### SQL Injection
```python
# BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### Missing Error Handling
```python
# BAD: Uncaught exceptions
data = json.loads(response.text)

# GOOD: Handle parse errors
try:
    data = json.loads(response.text)
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse JSON: {e}")
    return None
```

### State Management Issues
```javascript
// BAD: Mutating state directly
this.state.items.push(newItem);

// GOOD: Creating new state
this.setState({ items: [...this.state.items, newItem] });
```

## Code Smells to Watch For

1. **Long Methods**: Functions > 50 lines often do too much
2. **Too Many Parameters**: > 4 parameters suggests refactoring needed
3. **Deep Nesting**: > 3 levels makes code hard to follow
4. **Commented-Out Code**: Should be removed or explained
5. **Magic Numbers**: Use named constants instead
6. **God Objects**: Classes doing too many things
7. **Duplicate Code**: Extract into shared functions
8. **Premature Optimization**: Optimize only after profiling
9. **Missing Documentation**: Complex logic needs explanation
10. **Inconsistent Naming**: Follow project conventions

## Language-Specific Considerations

### Python
- List comprehensions vs loops
- Generator expressions for memory efficiency
- Context managers for resource handling
- Type hints for clarity
- Virtual environment dependencies

### JavaScript/TypeScript
- Proper use of const/let (no var)
- Arrow functions vs regular functions
- Promise chains vs async/await
- TypeScript strict mode benefits
- Module import/export patterns

### Java
- Proper exception hierarchy usage
- Stream API for collections
- Try-with-resources for AutoCloseable
- Immutability where possible
- Generics for type safety

### Go
- Error handling patterns
- Goroutine and channel safety
- Defer for cleanup
- Interface satisfaction
- Context propagation

## Review Process Tips

1. **Start with the big picture**: Understand the overall change before diving into details
2. **Read the tests first**: They explain what the code should do
3. **Check for missing tests**: What scenarios aren't covered?
4. **Look for simplification opportunities**: Can complexity be reduced?
5. **Consider alternatives**: Is there a better approach?
6. **Think about future maintenance**: Will this be easy to modify later?
7. **Verify documentation**: Are comments and docs updated?
8. **Check dependencies**: Are new libraries necessary and secure?
