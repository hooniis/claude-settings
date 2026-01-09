# Java Core Topics

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

---

## Naming

### Conventions

| Type | Style | Example |
|------|-------|---------|
| Classes | Nouns, PascalCase | `OrderService`, `FlightManager` |
| Methods | Verbs, camelCase | `createOrder`, `findByAirline` |
| Booleans | Question form | `isValid`, `hasPermission`, `canProcess` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Packages | lowercase | `com.example.order` |

### Guidelines

- Use intention-revealing names
- Express domain concepts, not technical implementation
- Avoid abbreviations
- Boolean names should read as questions

```java
// Bad
int d = 7;
if (order.status == 3 && order.paidAt != null)

// Good
int maxRetryDays = 7;
if (order.isConfirmed() && order.isPaid())
```

---

## Functions

### Rules

- **Single responsibility** - do one thing well
- **Keep short** - prefer < 20 lines
- **Max 7 parameters** - use object for more
- **Avoid side effects** - be predictable
- **Return early** - reduce nesting

### Early Return Pattern

```java
// Good - early return
public Result process(Order order) {
    if (order == null) return Result.empty();
    if (order.isCancelled()) return Result.cancelled();
    return processOrder(order);
}

// Bad - deep nesting
public Result process(Order order) {
    if (order != null) {
        if (!order.isCancelled()) {
            return processOrder(order);
        }
    }
    return Result.empty();
}
```

---

## Classes

### Rules

- Single responsibility
- Small and focused
- Prefer composition over inheritance
- Keep dependencies minimal (< 5 constructor params)
- ~200-300 lines max
- **Avoid setters** - prefer immutability

### Avoid Setters

Setters break encapsulation and make objects mutable. Prefer immutable objects.

```java
// Bad - mutable with setters
public class User {
    private String name;
    private String email;

    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }
}

// Good - immutable via constructor
public class User {
    private final String name;
    private final String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
}

// Good - use record (Java 16+)
public record User(String name, String email) {}

// If mutation needed - return new instance
public User withName(String newName) {
    return new User(newName, this.email);
}
```

**When setters are acceptable:**
- Framework requirements (JPA entities, JavaBeans)
- Builder pattern internals
- Performance-critical mutable buffers

### Class Layout Order

```java
public class UserService {
    // 1. Static constants
    private static final int CACHE_SIZE = 100;

    // 2. Static variables
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    // 3. Instance variables
    private final UserRepository repository;
    private final Map<Long, User> cache;

    // 4. Constructors
    public UserService(UserRepository repository) {
        this.repository = repository;
        this.cache = new HashMap<>();
    }

    // 5. Static factory methods (public)
    public static UserService create() { }

    // 6. Public methods
    public Optional<User> findUser(Long id) { }

    // 7. Package-private methods
    void clearCache() { }

    // 8. Protected methods
    protected void validateUser(User user) { }

    // 9. Private methods
    private void updateCache(User user) { }

    // 10. Private static methods
    private static String normalize(String input) { }

    // 11. Nested classes (static first, then inner)
    private static class CacheEntry { }
}
```

| Order | Member Type |
|-------|-------------|
| 1 | Static constants (`static final`) |
| 2 | Static variables |
| 3 | Instance variables |
| 4 | Constructors |
| 5 | Static factory methods (`public static`) |
| 6 | Public methods |
| 7 | Package-private methods |
| 8 | Protected methods |
| 9 | Private methods |
| 10 | Private static methods |
| 11 | Nested classes (static → inner) |

### When to Split

Split when:
- Class has multiple unrelated responsibilities
- Class is hard to test
- Class exceeds ~200-300 lines

Keep together when:
- Operations are cohesive
- Splitting would scatter related logic

---

## Comments

### Rules

- Code should be self-documenting
- Comment **WHY**, not **WHAT**
- Delete commented-out code
- Use Javadoc for public APIs

```java
// Bad - explains what
// Increment counter by 1
counter++;

// Good - explains why
// Retry count resets after successful response per API spec
retryCount = 0;
```

---

## Error Handling

### Rules

- Use specific exceptions
- Fail fast - validate early
- Don't swallow exceptions silently
- Log with context
- Use Optional for expected absence

```java
// Good - specific exception
public Order findOrder(Long id) {
    return orderRepository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));
}

// Bad - returning null for errors
public Order findOrder(Long id) {
    try {
        return orderRepository.findById(id).orElse(null);
    } catch (Exception e) {
        return null;  // Lost error context
    }
}
```

---

## Clean Code Principles

### DRY (Don't Repeat Yourself)

- Extract common logic to methods
- Use utility classes for shared operations
- But avoid premature abstraction

### KISS (Keep It Simple)

- Simplest solution that works
- Avoid clever code
- Optimize for readability

```java
// Good - simple and clear
var activeOrders = orders.stream().filter(Order::isActive).toList();

// Bad - unnecessarily complex
var activeOrders = orders.stream()
    .reduce(new ArrayList<Order>(), (acc, order) -> {
        if (order.isActive()) acc.add(order);
        return acc;
    }, (a, b) -> a);
```

---

## Code Smells to Avoid

| Smell | Threshold |
|-------|-----------|
| Long methods | > 20 lines |
| Long parameter lists | > 7 params |
| Deep nesting | > 2 levels |
| Magic numbers/strings | Any |
| Dead code | Any |
| Duplicate code | Any |
| God classes | > 300 lines |

---

## Readable Code

### Use Explanatory Variables

```java
// Bad - hard to understand
if (flight.getDepartureTime().isAfter(now) && flight.getSeats() > 0 && !flight.isCancelled())

// Good - clear intent
boolean isUpcoming = flight.getDepartureTime().isAfter(now);
boolean hasAvailableSeats = flight.getSeats() > 0;
boolean isBookable = isUpcoming && hasAvailableSeats && !flight.isCancelled();

if (isBookable) { ... }
```

### Prefer Positive Conditions

```java
// Bad - double negative
if (!isNotValid)

// Good - positive
if (isValid)
```

### Group Related Code

```java
// Good - logical sections separated
public Result processOrder(Order order) {
    // Validation
    validateOrder(order);

    // Processing
    var result = calculateTotal(order);
    applyDiscount(result);

    // Persistence
    return saveOrder(result);
}
```

### Self-Documenting Code

```java
// Bad - needs comment
// Check if user can book (must be adult and verified)
if (user.getAge() >= 18 && user.isVerified())

// Good - code explains itself
if (user.isAdult() && user.isVerified())

// Even better
if (user.canBook())
```

---

## Testable Code

### Use Constructor Injection

```java
// Good - dependencies injected, easy to mock
public class OrderService {
    private final OrderRepository orderRepository;
    private final FareCalculator fareCalculator;

    public OrderService(OrderRepository orderRepository, FareCalculator fareCalculator) {
        this.orderRepository = orderRepository;
        this.fareCalculator = fareCalculator;
    }
}

// Bad - hard dependencies
public class OrderService {
    private final OrderRepository orderRepository = new OrderRepositoryImpl();
}
```

### Avoid Static Methods and Singletons

```java
// Good - injectable dependency
public class BookingService {
    private final TimeProvider timeProvider;

    public boolean isExpired(Booking booking) {
        return booking.getExpiresAt().isBefore(timeProvider.now());
    }
}

// Bad - static call, untestable
public class BookingService {
    public boolean isExpired(Booking booking) {
        return booking.getExpiresAt().isBefore(LocalDateTime.now());
    }
}
```

### Separate Pure Logic from Side Effects

```java
// Good - pure function, easy to test
public Money calculateDiscount(Order order, Membership membership) {
    if (membership.isVip()) return order.getTotal().multiply(0.2);
    if (membership.isPremium()) return order.getTotal().multiply(0.1);
    return Money.ZERO;
}
```

### Use Interfaces for External Dependencies

```java
// Good - interface allows test doubles
public interface FlightClient {
    List<Flight> search(SearchRequest request);
}

public class FlightService {
    private final FlightClient flightClient;

    public Optional<Flight> findCheapest(SearchRequest request) {
        return flightClient.search(request).stream()
            .min(Comparator.comparing(Flight::getPrice));
    }
}
```

### Testability Checklist

- [ ] Can I instantiate this class without a framework?
- [ ] Can I control all inputs including time and randomness?
- [ ] Can I verify outputs without checking database/files?
- [ ] Are there any hidden dependencies?
- [ ] Is the logic separated from I/O operations?

---

## OOP & SOLID

> **Apply pragmatically, don't over-engineer.**
>
> These are guidelines, not strict rules. The simplest solution that works is often the best.

### Core Principles

- **Encapsulation** - Hide internal details, expose meaningful behavior
- **Composition over Inheritance** - Prefer has-a over is-a relationships
- **Program to interfaces** - At external boundaries (API, DB), not everywhere

### Don't Over-Engineer

**Signs of over-engineering:**
- Interface with single implementation
- Abstract class with one subclass
- Factory for simple object creation
- Multiple layers for simple operations

**Rule of thumb:** Wait for 2-3 real use cases before abstracting.

---

## SOLID Principles

> Apply when they solve real problems. Skip when they add unnecessary complexity.

| Principle | When to Apply | When to Skip |
|-----------|---------------|--------------|
| **S** - Single Responsibility | Class has unrelated responsibilities | Service orchestrating multiple operations is fine |
| **O** - Open/Closed | Multiple implementations exist | Single implementation - just use class |
| **L** - Liskov Substitution | Building class hierarchies | Simple composition |
| **I** - Interface Segregation | Clients need different subsets | 5-7 method interface is fine |
| **D** - Dependency Inversion | External boundaries (API, DB) | Internal utility code |

---

## When to Abstract

**Create interfaces when:**
- Multiple implementations exist or are likely
- Testing requires mocking external dependencies
- Crossing architectural boundaries (API, DB)

**Don't abstract when:**
- Only one implementation exists
- It's internal utility code
- It adds complexity without benefit

---

## Summary

| Do | Don't |
|----|-------|
| Write readable code | Write clever code |
| Keep it simple | Over-engineer |
| Abstract when needed | Abstract preemptively |
| Apply SOLID flexibly | Follow rules blindly |
| Name things clearly | Use abbreviations |
| Return early | Nest deeply |

> **Remember**: The simplest solution that works is usually the best. Don't create abstractions for hypothetical future needs.
