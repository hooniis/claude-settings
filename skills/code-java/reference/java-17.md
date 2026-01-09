# Java 17

**Release:** September 2021 | **Status:** LTS (until 2029)

---

## Key Features

| Feature | Description |
|---------|-------------|
| Records | Immutable data carriers |
| Sealed Classes | Restricted class hierarchies |
| Pattern Matching (instanceof) | `if (obj instanceof String s)` |
| Text Blocks | Multi-line strings `"""..."""` |
| Switch Expressions | `switch` as expression with `->` |
| Helpful NPE | Detailed null pointer messages |

---

## Guidelines

### Records

**Use for:**
- DTOs, API responses
- Value objects
- Immutable data carriers

**Don't use for:**
- Entities with mutable state
- Classes needing inheritance

```java
// Good - DTO
public record UserDto(Long id, String name, String email) {}

// With validation
public record User(String email, String name) {
    public User {
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
    }
}
```

### Sealed Classes

**Use for:**
- Closed type hierarchies
- Domain modeling with exhaustive cases
- API stability

```java
public sealed interface Result<T> permits Success, Error {}
public record Success<T>(T data) implements Result<T> {}
public record Error(String message) implements Result<Object> {}

// Exhaustive switch - no default needed
<T> void handle(Result<T> result) {
    switch (result) {
        case Success<T> s -> process(s.data());
        case Error e -> log.error(e.message());
    }
}
```

### Pattern Matching

```java
// Before
if (obj instanceof String) {
    String s = (String) obj;
    process(s);
}

// After
if (obj instanceof String s) {
    process(s);
}

// With condition
if (obj instanceof String s && s.length() > 5) {
    process(s);
}
```

### Text Blocks

```java
String json = """
    {
        "name": "%s",
        "age": %d
    }
    """.formatted(name, age);
```

### Switch Expressions

```java
String result = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
    case SATURDAY, SUNDAY -> "Weekend";
};
```

---

## Common Pitfalls

- **Records are immutable** - Can't have setters, use `withX()` pattern
- **Sealed classes** - Permitted classes must be in same package/module
- **Pattern variable scope** - Only valid in true branch: `&&` OK, `||` not OK

---

## Migration from Java 11

| Java 11 | Java 17 |
|---------|---------|
| POJO data class | `record` |
| instanceof + cast | Pattern matching |
| String concatenation | Text blocks for multi-line |
| switch statement | Switch expression |
