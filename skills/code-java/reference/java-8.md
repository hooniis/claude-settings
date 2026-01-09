# Java 8

**Release:** March 2014 | **Status:** EOL (migrate to 11+)

---

## Key Features

| Feature | Description |
|---------|-------------|
| Lambda Expressions | `(x) -> x * 2` |
| Stream API | `list.stream().filter().map().collect()` |
| Optional | Null-safe container |
| Method References | `String::length`, `User::new` |
| Functional Interfaces | `Function`, `Predicate`, `Consumer`, `Supplier` |
| Date/Time API | `LocalDate`, `LocalDateTime`, `ZonedDateTime` |
| Default Methods | Interface methods with implementation |

---

## Guidelines

### Streams

- Use for transformations, not as loop replacement
- Prefer method references: `User::getName` over `u -> u.getName()`
- Avoid parallel streams for small collections
- Streams are single-use - create new stream for each operation

```java
// Good
List<String> names = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .toList();

// Bad - stream reuse
Stream<String> stream = list.stream();
long count = stream.count();
stream.filter(...);  // IllegalStateException!
```

### Optional

| Do | Don't |
|----|-------|
| Return `Optional` from methods | Use as method parameter |
| Use `orElse`, `orElseThrow`, `map` | Call `get()` without check |
| Use for return values | Use as class field |

```java
// Good
Optional<User> findUser(Long id);
user.map(User::getName).orElse("Unknown");
user.orElseThrow(() -> new NotFoundException());

// Bad
void process(Optional<User> user);  // Don't use as parameter
user.get();  // May throw NoSuchElementException
```

### Functional Interfaces

| Interface | Method | Use Case |
|-----------|--------|----------|
| `Function<T,R>` | `R apply(T)` | Transform |
| `Predicate<T>` | `boolean test(T)` | Filter |
| `Consumer<T>` | `void accept(T)` | Side effect |
| `Supplier<T>` | `T get()` | Factory |

### Date/Time API

| Old (Avoid) | New (Use) |
|-------------|-----------|
| `Date` | `LocalDate`, `Instant` |
| `Calendar` | `LocalDateTime` |
| `SimpleDateFormat` | `DateTimeFormatter` |

---

## Common Pitfalls

- **Stream reuse** - Streams can only be consumed once
- **Optional.get()** - Always use `orElse` or `orElseThrow`
- **Modifying external state in lambdas** - Variables must be effectively final
- **Parallel stream overhead** - Not faster for small collections

---

## Migration

Replace anonymous classes with lambdas:
```java
// Before
Runnable r = new Runnable() { public void run() { ... } };

// After
Runnable r = () -> { ... };
```
