# Java 25

**Release:** September 2025 | **Status:** LTS (until 2033)

---

## Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| Module Imports | Final | `import module java.base;` |
| Instance Main | Final | `void main() { }` |
| Flexible Constructors | Final | Statements before `super()` |
| Scoped Values | Final | ThreadLocal replacement |
| Structured Concurrency | Preview | Coordinated concurrent tasks |
| Primitive Patterns | Preview | `case int i when i > 0` |
| Compact Object Headers | Final | 33% memory reduction |

---

## Guidelines

### Module Imports

| Use | Avoid |
|-----|-------|
| Scripts, learning | Production code |
| Quick prototypes | Libraries |

```java
// Scripts - OK
import module java.base;
void main() { println(List.of(1, 2, 3)); }

// Production - use explicit imports
import java.util.List;
```

### Instance Main Methods

**Use for:**
- Scripts, CLI tools
- Learning examples
- Quick prototypes

**Don't use for:**
- Framework-based apps (Spring, etc.)
- Production services

```java
// Script
void main(String[] args) {
    if (args.length == 0) {
        println("Usage: program <name>");
        return;
    }
    println("Hello, " + args[0]);
}
```

### Scoped Values (Replace ThreadLocal)

| Scoped Values | ThreadLocal |
|---------------|-------------|
| Immutable | Mutable |
| Explicit scope | Implicit scope |
| No memory leaks | Potential leaks |
| Virtual thread safe | Problematic with virtual threads |

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

void handleRequest(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        processRequest();  // User available in entire call stack
    });
}
```

### Structured Concurrency

**Use for:**
- Multiple parallel tasks that should succeed/fail together
- Clean cancellation handling

```java
UserData fetchUserData(Long userId) throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        var user = scope.fork(() -> userService.fetch(userId));
        var orders = scope.fork(() -> orderService.fetchByUser(userId));

        scope.join();
        scope.throwIfFailed();

        return new UserData(user.get(), orders.get());
    }
}
```

### Flexible Constructor Bodies

```java
// Now allowed: validation before super()
public User(String name) {
    if (name == null || name.isBlank()) {
        throw new IllegalArgumentException("Name required");
    }
    name = name.trim();
    super();
    this.name = name;
}
```

---

## Common Pitfalls

- **Module imports in production** - Use explicit imports for clarity
- **Scoped value mutation** - Treat as immutable, use `List.copyOf()` for collections
- **Structured concurrency** - Always call `throwIfFailed()` after `join()`
- **Primitive patterns** - Still preview, may change

---

## Migration from Java 21

| Java 21 | Java 25 |
|---------|---------|
| ThreadLocal | Scoped Values |
| CompletableFuture.allOf() | Structured Concurrency |
| Static main method | Instance main (for scripts) |
| Validation after super() | Flexible constructor bodies |

---

## Performance

- **Compact Object Headers** - Automatic 33% memory reduction for small objects
- **Generational Shenandoah** - Lower GC pause times
- **AOT Optimizations** - Faster startup with `-XX:AOTMode=on`
