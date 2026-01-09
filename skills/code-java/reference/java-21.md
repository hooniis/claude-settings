# Java 21

**Release:** September 2023 | **Status:** LTS (until 2031) - **Recommended**

---

## Key Features

| Feature | Description |
|---------|-------------|
| Pattern Matching (switch) | Guards with `when`, record patterns |
| Record Patterns | Deconstruct records in patterns |
| Virtual Threads | Lightweight threads for I/O |
| Sequenced Collections | `getFirst()`, `getLast()`, `reversed()` |
| String Templates | `STR."Hello \{name}"` (Preview) |
| Unnamed Patterns | `case Point(int x, _)` |

---

## Guidelines

### Virtual Threads

**Use for:**
- I/O-bound tasks (HTTP, DB, file)
- High-concurrency servers
- Thousands of concurrent tasks

**Don't use for:**
- CPU-bound computation
- Tasks requiring thread affinity

```java
// I/O tasks - use virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    users.forEach(user -> executor.submit(() -> sendEmail(user)));
}

// CPU tasks - use platform threads
ExecutorService cpu = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);
```

### Pattern Matching (switch)

```java
String describe(Object obj) {
    return switch (obj) {
        case String s when s.isEmpty() -> "empty string";
        case String s -> "string: " + s;
        case Integer i when i > 0 -> "positive";
        case Integer i -> "non-positive";
        case null -> "null";
        default -> "unknown";
    };
}
```

### Record Patterns

```java
// Deconstruct in instanceof
if (obj instanceof Point(int x, int y)) {
    process(x, y);
}

// Nested deconstruction
if (obj instanceof Rectangle(Point(int x1, int y1), Point(int x2, int y2))) {
    int area = (x2 - x1) * (y2 - y1);
}
```

### Sequenced Collections

```java
List<String> list = List.of("a", "b", "c");

String first = list.getFirst();      // "a"
String last = list.getLast();        // "c"
List<String> rev = list.reversed();  // ["c", "b", "a"]
```

---

## Common Pitfalls

### Virtual Threads

- **ThreadLocal with virtual threads** - Use Scoped Values instead (or pass context explicitly)
- **Blocking operations** - OK with virtual threads, but avoid `synchronized` blocks on virtual threads

### Pattern Matching

- **Exhaustiveness** - Must handle all cases including `null` and `default`
- **Guard ordering** - More specific guards first

### Sequenced Collections

- **Empty collection** - `getFirst()`/`getLast()` throw on empty collections

---

## Migration from Java 17

| Java 17 | Java 21 |
|---------|---------|
| `Executors.newFixedThreadPool()` | `Executors.newVirtualThreadPerTaskExecutor()` (for I/O) |
| instanceof chain | Pattern matching switch |
| `list.get(0)` | `list.getFirst()` |
| `list.get(size-1)` | `list.getLast()` |
