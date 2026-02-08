Bug Classification Database
A comprehensive reference for bug detection and classification systems.

1. Security Vulnerabilities
SQL Injection
Category: Security Severity: Critical Description: Unsanitized user input directly concatenated into SQL queries, allowing attackers to execute arbitrary SQL commands. Common Patterns: String concatenation with user input in SQL queries, missing parameterized queries Solution: Use parameterized queries or prepared statements

Command Injection
Category: Security Severity: Critical Description: Unsanitized user input passed to system commands, allowing arbitrary command execution. Common Patterns: os.system(), subprocess with shell=True, eval() with user input Solution: Use safe APIs, validate/sanitize input, avoid shell=True

Cross-Site Scripting (XSS)
Category: Security Severity: High Description: Unescaped user input rendered in HTML, allowing script injection. Common Patterns: Direct HTML rendering of user input, missing output encoding Solution: Use proper HTML escaping, Content Security Policy headers

Path Traversal
Category: Security Severity: High Description: Unsanitized file paths allowing access to files outside intended directory. Common Patterns: User-controlled file paths, missing path validation, ../.. patterns Solution: Validate paths, use os.path.abspath() and check basedir

Hardcoded Credentials
Category: Security Severity: Critical Description: Passwords, API keys, or secrets stored directly in source code. Common Patterns: password = "admin123", api_key = "sk-...", connection strings with credentials Solution: Use environment variables, secret management systems

Buffer Overflow
Category: Security Severity: Critical Description: Writing beyond allocated buffer size, potentially overwriting memory. Common Patterns: strcpy(), gets(), sprintf() without bounds checking, unbounded array access Solution: Use safe string functions (strncpy, snprintf), validate array indices

2. Logic Errors
Division by Zero
Category: Logic Error Severity: High Description: Division operation without checking for zero divisor, causing runtime exception. Common Patterns: x / y without checking if y == 0, modulo operations Solution: Add zero check before division

Off-by-One Error
Category: Logic Error Severity: Medium Description: Loop or array access with incorrect boundary, often using <= instead of <. Common Patterns: for i in range(len(arr) + 1), arr[len(arr)], fence-post errors Solution: Correct loop bounds, use proper indexing

Null/None Dereference
Category: Logic Error Severity: Medium Description: Attempting to access attributes or methods on None/null pointer. Common Patterns: obj.method() without null check, dereferencing uninitialized pointers Solution: Add null checks before access

Integer Overflow
Category: Logic Error Severity: Medium Description: Arithmetic operation results in value exceeding type limits. Common Patterns: Large multiplications, additions without bounds checking Solution: Use appropriate data types, add bounds checking

Race Condition
Category: Concurrency Severity: High Description: Multiple threads accessing shared resource without proper synchronization. Common Patterns: Shared variables without locks, TOCTOU bugs, check-then-act patterns Solution: Use locks, mutexes, or atomic operations

Infinite Loop
Category: Logic Error Severity: High Description: Loop without proper exit condition, causing program to hang. Common Patterns: while True without break, incorrect loop conditions, missing increment Solution: Ensure proper exit conditions, add safeguards

Incorrect Comparison
Category: Logic Error Severity: Medium Description: Using wrong comparison operator or comparing wrong values. Common Patterns: Using = instead of ==, comparing floating points with ==, wrong operands Solution: Use correct operators, compare with tolerance for floats

3. Variable and Initialization Errors
Uninitialized Variable
Category: Initialization Error Severity: High Description: Variable declared but used before being assigned a value. Common Patterns: int count; used in loop without initialization, uninitialized pointers Solution: Always initialize variables at declaration

Wrong Variable Used
Category: Logic Error Severity: Medium Description: Using a different variable than intended due to similar names or copy-paste errors. Common Patterns: Using temp1 instead of temp2, loop variable shadowing Solution: Use meaningful variable names, code review

Incorrect Assignment
Category: Logic Error Severity: Medium Description: Assigning wrong value to a variable, often due to typos or logic errors. Common Patterns: x = y when y = x intended, wrong constant values Solution: Code review, unit testing

4. Function and Method Errors
Wrong Method Name
Category: API Misuse Severity: High Description: Calling incorrect method name, often due to typos or confusion with similar methods. Common Patterns: Using close() instead of shutdown(), begin() vs start(), case sensitivity errors Solution: Consult API documentation, use IDE autocomplete

Wrong Parameter Value
Category: API Misuse Severity: High Description: Passing incorrect value as function/method parameter. Common Patterns: Negative value where positive required, wrong units, inverted boolean Solution: Validate parameters, check documentation for expected values

Wrong Parameter Order
Category: API Misuse Severity: Medium Description: Arguments passed in incorrect order to function call. Common Patterns: func(y, x) instead of func(x, y), especially with same-type parameters Solution: Use named parameters, check function signature

Missing Function Call
Category: Logic Error Severity: Medium Description: Required function or method not called when expected. Common Patterns: Missing initialization calls, cleanup not performed Solution: Follow API contracts, ensure all required calls are made

5. Resource Management
Memory Leak
Category: Resource Management Severity: High Description: Allocated memory not properly freed, leading to gradual memory exhaustion. Common Patterns: new without delete, malloc without free, circular references Solution: Proper cleanup, use smart pointers, RAII pattern

Resource Leak
Category: Resource Management Severity: Medium Description: File handles, connections, or other resources not properly closed. Common Patterns: Missing close() calls, no try-finally, exception interrupts cleanup Solution: Use context managers (with statement), ensure cleanup in finally blocks

Double Free
Category: Resource Management Severity: Critical Description: Freeing the same memory location twice, causing undefined behavior. Common Patterns: delete called twice, free() on already freed pointer Solution: Set pointer to null after free, use smart pointers

Use After Free
Category: Resource Management Severity: Critical Description: Accessing memory after it has been freed. Common Patterns: Dereferencing freed pointer, using closed file handle Solution: Set pointer to null after free, careful lifetime management

6. Input Validation
Missing Input Validation
Category: Input Validation Severity: Medium-High Description: User input accepted without validation, leading to unexpected behavior. Common Patterns: Direct use of user input, no type checking, no range validation Solution: Validate all inputs, check types, ranges, formats

Type Confusion
Category: Type Error Severity: Medium Description: Variable used as wrong type, causing runtime errors or unexpected behavior. Common Patterns: Mixing strings and integers, wrong function arguments, implicit conversions Solution: Use type hints, validate input types, explicit casting

Invalid Range
Category: Input Validation Severity: Medium Description: Value outside expected or valid range. Common Patterns: Negative index, percentage > 100, negative quantity Solution: Add range checks, define and enforce constraints

7. Error Handling
Unhandled Exception
Category: Error Handling Severity: Medium Description: Exception not caught, causing program to crash. Common Patterns: Missing try-except blocks, unchecked exceptions Solution: Add appropriate exception handling

Silent Failure
Category: Error Handling Severity: Medium Description: Errors caught but not logged or handled, making debugging difficult. Common Patterns: Empty except blocks, pass in exception handlers, swallowing errors Solution: Log errors, provide meaningful error messages

Incorrect Error Handling
Category: Error Handling Severity: Medium Description: Exception caught but handled incorrectly, masking real issues. Common Patterns: Catching Exception instead of specific types, continuing after critical error Solution: Catch specific exceptions, handle appropriately

Missing Error Check
Category: Error Handling Severity: Medium Description: Return value or error status not checked after function call. Common Patterns: Ignoring return codes, not checking errno, assuming success Solution: Always check return values and error states

8. Code Quality Issues
Dead Code
Category: Code Quality Severity: Low Description: Code that is never executed or has no effect. Common Patterns: Unreachable code after return, unused variables, commented blocks Solution: Remove dead code

Code Duplication
Category: Code Quality Severity: Low Description: Same or similar code repeated in multiple places. Common Patterns: Copy-pasted code blocks, repeated logic Solution: Extract common code into functions

Magic Numbers
Category: Code Quality Severity: Low Description: Hardcoded numbers without explanation or constants. Common Patterns: arr[42], sleep(86400), buffer[1024] Solution: Use named constants with meaningful names

Unreachable Code
Category: Code Quality Severity: Low Description: Code that can never be executed due to control flow. Common Patterns: Code after return/break/continue, always-false conditions Solution: Remove unreachable code or fix control flow

Summary - All Bug Types
#	Bug Type	Category	Severity
1	SQL Injection	Security	Critical
2	Command Injection	Security	Critical
3	Cross-Site Scripting (XSS)	Security	High
4	Path Traversal	Security	High
5	Hardcoded Credentials	Security	Critical
6	Buffer Overflow	Security	Critical
7	Division by Zero	Logic Error	High
8	Off-by-One Error	Logic Error	Medium
9	Null/None Dereference	Logic Error	Medium
10	Integer Overflow	Logic Error	Medium
11	Race Condition	Concurrency	High
12	Infinite Loop	Logic Error	High
13	Incorrect Comparison	Logic Error	Medium
14	Uninitialized Variable	Initialization Error	High
15	Wrong Variable Used	Logic Error	Medium
16	Incorrect Assignment	Logic Error	Medium
17	Wrong Method Name	API Misuse	High
18	Wrong Parameter Value	API Misuse	High
19	Wrong Parameter Order	API Misuse	Medium
20	Missing Function Call	Logic Error	Medium
21	Memory Leak	Resource Management	High
22	Resource Leak	Resource Management	Medium
23	Double Free	Resource Management	Critical
24	Use After Free	Resource Management	Critical
25	Missing Input Validation	Input Validation	Medium-High
26	Type Confusion	Type Error	Medium
27	Invalid Range	Input Validation	Medium
28	Unhandled Exception	Error Handling	Medium
29	Silent Failure	Error Handling	Medium
30	Incorrect Error Handling	Error Handling	Medium
31	Missing Error Check	Error Handling	Medium
32	Dead Code	Code Quality	Low
33	Code Duplication	Code Quality	Low
34	Magic Numbers	Code Quality	Low
35	Unreachable Code	Code Quality	Low
