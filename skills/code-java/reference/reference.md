# Java Reference

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

---

## Additional References

| Reference | Description |
|-----------|-------------|
| [Core Topics](core-topics.md) | Naming, code organization, formatting, clean code, modern features, immutability, error handling, anti-patterns |
| [Testing](testing.md) | Test quality guidelines, what to test, mocking guidelines, anti-patterns |
| [Java 8](java-8.md) | Lambdas, Streams, Optional, Date/Time API |
| [Java 11](java-11.md) | var, String methods, HTTP Client |
| [Java 17](java-17.md) | Records, Sealed classes, Pattern matching, Text blocks |
| [Java 21](java-21.md) | Pattern matching for switch, Virtual threads, Sequenced collections |
| [Java 25](java-25.md) | Module imports, Scoped values, Structured concurrency |

---

## Essential Rules

| Rule | Example |
|------|---------|
| Use `Optional` for absence | `Optional<User> findUser(Long id)` |
| Prefer immutability | `private final List<User> users` |
| Use records for DTOs | `record UserDto(Long id, String name)` |
| Early returns over nesting | `if (invalid) return;` |
| Self-documenting names | `calculateTotalWithTax()` not `calc()` |

---

## Modern Java Checklist

- [ ] Records for simple data carriers
- [ ] Sealed classes for closed type hierarchies
- [ ] Pattern matching for instanceof/switch
- [ ] Text blocks for multiline strings
- [ ] Optional instead of null returns
- [ ] Streams for collection transformations
- [ ] var for obvious types
- [ ] Immutable collections (List.of, Set.of, Map.of)

---

## Version Selection

| Version | Status | Recommendation |
|---------|--------|----------------|
| Java 8 | EOL | Migrate to 11+ |
| Java 11 | LTS (2026) | Conservative migration |
| Java 17 | LTS (2029) | Stable, mature |
| Java 21 | LTS (2031) | **Recommended for new projects** |
| Java 25 | LTS (2033) | Cutting-edge projects |

### Key Features by Version

| Feature | 8 | 11 | 17 | 21 | 25 |
|---------|---|----|----|----|----|
| Lambdas, Streams, Optional | ✅ | ✅ | ✅ | ✅ | ✅ |
| var | - | ✅ | ✅ | ✅ | ✅ |
| Records, Sealed Classes | - | - | ✅ | ✅ | ✅ |
| Pattern Matching (switch) | - | - | - | ✅ | ✅ |
| Virtual Threads | - | - | - | ✅ | ✅ |
| Scoped Values, Structured Concurrency | - | - | - | - | ✅ |

---

## Do's and Don'ts

### Do ✅

- Write readable, self-documenting code
- Use modern Java features appropriately
- Keep classes and methods focused (SRP)
- Prefer immutability
- Use Optional for absence

### Don't ❌

- Over-engineer simple solutions
- Return null (use Optional)
- Create god classes
- Use magic numbers
- Ignore compiler warnings

---

## External Resources

- [Effective Java (Book)](https://www.oreilly.com/library/view/effective-java/9780134686097/)
