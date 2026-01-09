# Testing Best Practices

A guide for writing meaningful, maintainable tests in Java.

---

## Critical Rules

> **NEVER MODIFY PRODUCTION CODE TO MAKE TESTS PASS**
>
> - Tests validate existing behavior, not drive code changes
> - If a test fails, fix the test logic or setup, NOT the production code
> - Production code changes require deliberate feature requests or bug fixes
> - Write tests that work with the current implementation AS-IS

> **ALWAYS RUN AND VERIFY TESTS**
>
> - Run tests immediately after writing them
> - Ensure ALL tests pass before considering the task complete
> - If tests fail, debug and fix the TEST implementation
> - Command: `./gradlew test` or specific test class

> **DO NOT CREATE BOILERPLATE TESTS FOR COVERAGE**
>
> - NEVER write tests solely to increase code coverage metrics
> - Avoid trivial tests that only verify getters, setters, or simple pass-through methods
> - Do not create tests that provide no meaningful validation of business logic
> - Coverage numbers without meaningful assertions are misleading and add maintenance burden
> - Ask yourself: "Would this test catch a real bug?" - if no, don't write it

> **GENERATE MEANINGFUL TESTS**
>
> - Focus on testing actual business logic and behavior
> - Test edge cases, boundary conditions, and error handling paths
> - Verify complex state transitions and conditional logic
> - Write tests that would catch real bugs if the implementation changes incorrectly
> - Prioritize tests for critical paths and high-risk code sections
> - Each test should answer: "What behavior am I validating, and why does it matter?"

---

## Test Quality Guidelines

### DO Write Tests That

- Validate actual business logic and behavior
- Test edge cases and boundary conditions
- Verify error handling paths
- Cover complex state transitions
- Would catch real bugs if implementation changes

### DO NOT Write Tests That

- Only increase coverage numbers
- Test trivial getters/setters
- Verify simple pass-through methods
- Provide no meaningful validation
- Test framework behavior (Spring, Hibernate, etc.)

---

## Test Design Principles

| Principle | Description |
|-----------|-------------|
| **Keep Tests Simple** | Patterns are meant to simplify, not overcomplicate. Avoid excessive mocking or overly complex setups. |
| **Focus on Behavior** | Test the "what," not the "how." Verify outcomes rather than implementation details. |
| **Avoid Over-Mocking** | Mock only what's necessary to keep tests focused and reliable. Excessive mocking leads to brittle tests. |
| **Maintain Consistency** | Adopt a pattern that works well for your team and stick to it across the codebase. |
| **One Concept Per Test** | Each test should verify a single behavior. Multiple assertions are fine if they verify the same concept. |
| **Test Independence** | Tests should not depend on each other or share mutable state. Each test must be self-contained. |

---

## Test Naming

### Naming Patterns

| Pattern | Example |
|---------|---------|
| should_When_ | `shouldReturnNull_WhenUserNotFound` |
| given_When_Then | `givenInvalidEmail_WhenCreating_ThenThrowException` |
| methodName_StateUnderTest_ExpectedBehavior | `findById_WithNegativeId_ThrowsException` |

### Guidelines

- Test names should describe the scenario and expected outcome
- Avoid vague names like `testUser()` or `test1()`
- Names should be readable as documentation

---

## Test Structure

### Arrange-Act-Assert (AAA)

The standard pattern for structuring tests:

```java
@Test
void shouldCalculateTotalWithDiscount() {
    // Arrange - set up test data and conditions
    Order order = createOrderWithDiscount(10);

    // Act - execute the behavior being tested
    Money total = calculator.calculateTotal(order);

    // Assert - verify the expected outcome
    assertEquals(Money.of(90), total);
}
```

### Given-When-Then (BDD Style)

Alternative pattern emphasizing behavior:

```java
@Test
void givenActiveUser_whenProcessing_thenShouldSendNotification() {
    // Given - preconditions
    User user = activeUser();

    // When - action
    service.process(user);

    // Then - expected outcome
    verify(notificationService).send(user);
}
```

---

## What to Test

### High Priority (Always Test)

1. **Business Logic** - Core domain rules and calculations
2. **Edge Cases** - Null inputs, empty collections, boundary values
3. **Error Handling** - Exception conditions and recovery paths
4. **State Transitions** - Workflow and status changes
5. **Integration Points** - External service interactions (with mocks)

### Low Priority (Test Selectively)

1. **Simple CRUD** - Only if custom logic exists
2. **DTOs/Value Objects** - Only validation logic
3. **Configuration** - Only complex conditional setup

### Skip (Do Not Test)

1. **Getters/Setters** - No logic to verify
2. **Framework Behavior** - Spring, Hibernate work correctly
3. **Third-party Libraries** - Trust the library tests
4. **Generated Code** - Lombok, MapStruct output

---

## Mocking Guidelines

### When to Mock

- External services (HTTP clients, message queues)
- Database repositories (in unit tests)
- Time-dependent operations
- Non-deterministic behavior (random, UUID)

### When NOT to Mock

- The class under test
- Simple value objects
- Static utility methods (usually)
- Everything "just because"

### Mocking Best Practices

```java
// Good: Mock only external dependencies
@Test
void shouldSendEmailWhenUserCreated() {
    EmailService emailService = mock(EmailService.class);
    UserService service = new UserService(realValidator, emailService);

    service.createUser("john@example.com");

    verify(emailService).sendWelcome(any());
}

// Bad: Over-mocking internal collaborators
@Test
void shouldCreateUser() {
    Validator validator = mock(Validator.class);      // Unnecessary
    Mapper mapper = mock(Mapper.class);               // Unnecessary
    Logger logger = mock(Logger.class);               // Unnecessary
    // ... test becomes brittle and hard to maintain
}
```

---

## Test Data Management

### Use Builders for Complex Objects

```java
class UserBuilder {
    private String name = "Default Name";
    private String email = "default@example.com";
    private Role role = Role.USER;

    public UserBuilder withRole(Role role) {
        this.role = role;
        return this;
    }

    public User build() {
        return new User(name, email, role);
    }
}

// Usage - only specify what matters for the test
User admin = new UserBuilder().withRole(Role.ADMIN).build();
```

### Guidelines

- Use sensible defaults for all fields
- Only override values relevant to the test
- Keep builders in test packages
- Consider factory methods for common scenarios

---

## Parameterized Tests

Use when testing the same logic with multiple inputs:

```java
@ParameterizedTest
@CsvSource({
    "100, 10, 90",   // 10% discount
    "100, 0, 100",   // no discount
    "100, 100, 0"    // full discount
})
void shouldApplyDiscount(int price, int discount, int expected) {
    assertEquals(expected, calculator.applyDiscount(price, discount));
}
```

### When to Use

- Same logic, different inputs
- Boundary value testing
- Validation rules with multiple cases

### When NOT to Use

- Different behaviors being tested
- Complex setup varies per case
- Would obscure test intent

---

## Anti-Patterns to Avoid

### Testing Implementation Details

```java
// Bad: Tests HOW it works
@Test
void shouldCallRepositoryTwice() {
    service.findUser(1L);
    verify(repository, times(2)).findById(1L);  // Why twice? Implementation detail.
}

// Good: Tests WHAT it does
@Test
void shouldReturnUserWhenExists() {
    when(repository.findById(1L)).thenReturn(Optional.of(user));

    Optional<User> result = service.findUser(1L);

    assertTrue(result.isPresent());
}
```

### Test Interdependence

```java
// Bad: Tests depend on execution order
@Test @Order(1)
void shouldCreateUser() {
    userId = service.create(user).getId();
}

@Test @Order(2)
void shouldFindUser() {
    assertNotNull(service.find(userId));  // Fails if run alone
}

// Good: Self-contained tests
@Test
void shouldFindExistingUser() {
    User created = service.create(user);
    Optional<User> found = service.find(created.getId());
    assertTrue(found.isPresent());
}
```

### Catching Exceptions Blindly

```java
// Bad: Swallows failures
@Test
void shouldProcess() {
    try {
        service.process(data);
    } catch (Exception e) {
        // Test always passes
    }
}

// Good: Explicit assertion
@Test
void shouldProcessWithoutException() {
    assertDoesNotThrow(() -> service.process(data));
}
```

### Testing for Coverage

```java
// Bad: Meaningless test for coverage
@Test
void shouldGetName() {
    User user = new User("John");
    assertEquals("John", user.getName());  // What bug would this catch?
}

// Good: Test actual behavior
@Test
void shouldNormalizeName() {
    User user = new User("  john  ");
    assertEquals("John", user.getName());  // Tests trimming and capitalization
}
```

---

## Summary

| Guideline | Description |
|-----------|-------------|
| **Test Behavior** | Focus on what, not how |
| **Meaningful Tests** | Each test should catch real bugs |
| **Simple Setup** | Avoid excessive mocking |
| **Independent** | Tests don't depend on each other |
| **Clear Names** | Names describe scenario and outcome |
| **Run Always** | Never commit failing tests |

> **Remember**: The goal is confidence in your code, not coverage numbers. A small number of meaningful tests beats a large number of trivial ones.
