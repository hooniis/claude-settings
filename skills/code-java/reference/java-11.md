# Java 11

**Release:** September 2018 | **Status:** LTS (until 2026)

---

## Key Features

| Feature | Description |
|---------|-------------|
| `var` in lambdas | `(var x) -> x.process()` |
| String methods | `isBlank()`, `lines()`, `strip()`, `repeat()` |
| Collection to Array | `list.toArray(String[]::new)` |
| File methods | `Files.readString()`, `Files.writeString()` |
| HTTP Client | Standard `HttpClient` API |
| `Optional.isEmpty()` | Opposite of `isPresent()` |
| `Predicate.not()` | `filter(Predicate.not(String::isEmpty))` |

---

## Guidelines

### var Usage

| Use `var` | Use explicit type |
|-----------|-------------------|
| Type is obvious from RHS | Type unclear from context |
| `var user = new User()` | `UserDto result = process()` |
| `var list = List.of(...)` | `var data = getData()` ❌ |

```java
// Good - type is obvious
var user = new User("John");
var users = userRepository.findAll();

// Bad - type unclear
var result = process();  // What type?
```

### String Methods

| Method | Use Case |
|--------|----------|
| `isBlank()` | Check empty or whitespace (prefer over `trim().isEmpty()`) |
| `strip()` | Remove whitespace (prefer over `trim()` - handles Unicode) |
| `lines()` | Split into lines as Stream |
| `repeat(n)` | Repeat string n times |

### HTTP Client

- Reuse `HttpClient` instance (thread-safe)
- Use async methods for non-blocking I/O
- Handle response status codes explicitly

```java
private static final HttpClient CLIENT = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(10))
    .build();
```

---

## Common Pitfalls

- **var with null** - `var x = null;` won't compile
- **strip() vs trim()** - `strip()` handles Unicode whitespace
- **HTTP error handling** - Check status code, don't assume success

---

## Migration from Java 8

| Java 8 | Java 11 |
|--------|---------|
| `new Integer(42)` | `Integer.valueOf(42)` |
| `"".trim().isEmpty()` | `"".isBlank()` |
| `list.toArray(new String[0])` | `list.toArray(String[]::new)` |
