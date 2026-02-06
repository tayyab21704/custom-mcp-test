# Bug Classification Database

## Security Vulnerabilities

### SQL Injection
**Category**: Security
**Severity**: Critical
**Description**: Unsanitized user input directly concatenated into SQL queries, allowing attackers to execute arbitrary SQL commands.
**Common Patterns**: String concatenation with user input in SQL queries, missing parameterized queries
**Solution**: Use parameterized queries or prepared statements

### Command Injection
**Category**: Security
**Severity**: Critical
**Description**: Unsanitized user input passed to system commands, allowing arbitrary command execution.
**Common Patterns**: os.system(), subprocess with shell=True, eval() with user input
**Solution**: Use safe APIs, validate/sanitize input, avoid shell=True

### Cross-Site Scripting (XSS)
**Category**: Security
**Severity**: High
**Description**: Unescaped user input rendered in HTML, allowing script injection.
**Common Patterns**: Direct HTML rendering of user input, missing output encoding
**Solution**: Use proper HTML escaping, Content Security Policy headers

### Path Traversal
**Category**: Security
**Severity**: High
**Description**: Unsanitized file paths allowing access to files outside intended directory.
**Common Patterns**: User-controlled file paths, missing path validation
**Solution**: Validate paths, use os.path.abspath() and check basedir

### Hardcoded Credentials
**Category**: Security
**Severity**: Critical
**Description**: Passwords, API keys, or secrets stored directly in source code.
**Common Patterns**: password = "admin123", api_key = "sk-..."
**Solution**: Use environment variables, secret management systems

## Logic Errors

### Division by Zero
**Category**: Logic Error
**Severity**: High
**Description**: Division operation without checking for zero divisor, causing runtime exception.
**Common Patterns**: x / y without checking if y == 0
**Solution**: Add zero check before division

### Off-by-One Error
**Category**: Logic Error
**Severity**: Medium
**Description**: Loop or array access with incorrect boundary, often using <= instead of <.
**Common Patterns**: for i in range(len(arr) + 1), arr[len(arr)]
**Solution**: Correct loop bounds, use proper indexing

### Null/None Dereference
**Category**: Logic Error
**Severity**: Medium
**Description**: Attempting to access attributes or methods on None/null value.
**Common Patterns**: obj.method() without checking if obj is None
**Solution**: Add null checks before access

### Integer Overflow
**Category**: Logic Error
**Severity**: Medium
**Description**: Arithmetic operation results in value exceeding type limits.
**Common Patterns**: Large multiplications, additions without bounds checking
**Solution**: Use appropriate data types, add bounds checking

### Race Condition
**Category**: Concurrency
**Severity**: High
**Description**: Multiple threads accessing shared resource without proper synchronization.
**Common Patterns**: Shared variables without locks, TOCTOU bugs
**Solution**: Use locks, mutexes, or atomic operations

## Resource Management

### Memory Leak
**Category**: Resource Management
**Severity**: High
**Description**: Allocated memory not properly freed, leading to gradual memory exhaustion.
**Common Patterns**: Circular references, unclosed resources, growing caches
**Solution**: Proper cleanup, use context managers, weak references

### Resource Leak
**Category**: Resource Management
**Severity**: Medium
**Description**: File handles, connections, or other resources not properly closed.
**Common Patterns**: Missing close() calls, no try-finally or with statements
**Solution**: Use context managers (with statement), ensure cleanup in finally blocks

### Infinite Loop
**Category**: Logic Error
**Severity**: High
**Description**: Loop without proper exit condition, causing program to hang.
**Common Patterns**: while True without break, incorrect loop conditions
**Solution**: Ensure proper exit conditions, add safeguards

## Input Validation

### Missing Input Validation
**Category**: Input Validation
**Severity**: Medium-High
**Description**: User input accepted without validation, leading to unexpected behavior.
**Common Patterns**: Direct use of user input, no type checking
**Solution**: Validate all inputs, check types, ranges, formats

### Type Confusion
**Category**: Type Error
**Severity**: Medium
**Description**: Variable used as wrong type, causing runtime errors or unexpected behavior.
**Common Patterns**: Mixing strings and integers, wrong function arguments
**Solution**: Use type hints, validate input types

### Buffer Overflow
**Category**: Security
**Severity**: Critical
**Description**: Writing beyond allocated buffer size, potentially overwriting memory.
**Common Patterns**: Unbounded string operations, array access without bounds checking
**Solution**: Use safe string functions, validate array indices

## Error Handling

### Unhandled Exception
**Category**: Error Handling
**Severity**: Medium
**Description**: Exception not caught, causing program to crash.
**Common Patterns**: Missing try-except blocks, empty except clauses
**Solution**: Add appropriate exception handling

### Silent Failure
**Category**: Error Handling
**Severity**: Medium
**Description**: Errors caught but not logged or handled, making debugging difficult.
**Common Patterns**: Empty except blocks, pass in exception handlers
**Solution**: Log errors, provide meaningful error messages

### Incorrect Error Handling
**Category**: Error Handling
**Severity**: Medium
**Description**: Exception caught but handled incorrectly, masking real issues.
**Common Patterns**: Catching Exception instead of specific types, continuing after error
**Solution**: Catch specific exceptions, handle appropriately

## Code Quality Issues

### Dead Code
**Category**: Code Quality
**Severity**: Low
**Description**: Code that is never executed or has no effect.
**Common Patterns**: Unreachable code after return, unused variables
**Solution**: Remove dead code

### Code Duplication
**Category**: Code Quality
**Severity**: Low
**Description**: Same or similar code repeated in multiple places.
**Common Patterns**: Copy-pasted code blocks
**Solution**: Extract common code into functions

### Magic Numbers
**Category**: Code Quality
**Severity**: Low
**Description**: Hardcoded numbers without explanation or constants.
**Common Patterns**: arr[42], sleep(86400)
**Solution**: Use named constants with meaningful names