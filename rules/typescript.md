# TypeScript Style & Best Practices

A pragmatic guide for writing clean, readable, and maintainable TypeScript code.

> **Core Philosophy**: Simple is best. Write code that humans can understand. Don't over-engineer.

Based on [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html).

---

## Table of Contents

1. [Naming Conventions](#naming-conventions)
2. [Source Organization](#source-organization)
3. [Formatting](#formatting)
4. [Type System](#type-system)
5. [Clean Code Principles](#clean-code-principles)
6. [OOP & SOLID (Pragmatically)](#oop--solid-pragmatically)
7. [Functional Programming (Balanced)](#functional-programming-balanced)
8. [Functions](#functions)
9. [Classes](#classes)
10. [Error Handling](#error-handling)
11. [Testing](#testing)
12. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Naming Conventions

### Casing Rules

| Type | Style | Example |
|------|-------|---------|
| Classes, Interfaces, Types, Enums | `UpperCamelCase` | `UserService`, `HttpClient` |
| Variables, Functions, Methods | `lowerCamelCase` | `userName`, `calculateTotal()` |
| Constants (global immutable) | `CONSTANT_CASE` | `MAX_RETRY_COUNT` |
| Enum members | `CONSTANT_CASE` | `Status.ACTIVE` |

### Examples

```typescript
// Classes & Interfaces
class UserRepository { }
interface PaymentGateway { }
type UserId = string;

// Functions & Variables
function processOrder() { }
const userName = 'John';
let orderCount = 0;

// Constants
const MAX_RETRY_COUNT = 3;
const DEFAULT_TIMEOUT_MS = 5000;

// Enums
enum OrderStatus {
  PENDING,
  PROCESSING,
  COMPLETED,
}
```

### Acronyms
```typescript
// Treat acronyms as words
function loadHttpUrl() { }  // Not loadHTTPURL
class XmlParser { }         // Not XMLParser
const htmlContent = '';     // Not HTMLContent
```

### Avoid
```typescript
// Don't use underscores or prefixes
let _privateVar;        // Bad
let opt_value;          // Bad
interface IUserService  // Bad: no 'I' prefix

// Good
private privateVar;
let value;
interface UserService
```

---

## Source Organization

### File Structure Order
```typescript
// 1. Imports
import { Injectable } from '@angular/core';
import type { User } from './types';

// 2. Constants
const DEFAULT_PAGE_SIZE = 20;

// 3. Types/Interfaces (if not in separate file)
interface UserFilter {
  name?: string;
  active?: boolean;
}

// 4. Implementation
export class UserService { }
```

### Import Guidelines
```typescript
// Use named exports (avoid default exports)
export { UserService };           // Good
export default UserService;       // Avoid

// Use 'import type' for type-only imports
import type { User, Order } from './types';
import { UserService } from './services';

// Prefer destructured imports for frequently used items
import { map, filter, reduce } from 'lodash';

// Use namespace imports for large APIs
import * as fs from 'fs';
```

### File Naming
```typescript
// kebab-case for files
user-service.ts
order.types.ts
payment-gateway.interface.ts
```

---

## Formatting

### Braces & Spacing
```typescript
// Always use braces, even for single statements
if (isValid) {
  return result;
}

// Space after keywords
if (condition) { }
for (const item of items) { }
while (running) { }
```

### Strings
```typescript
// Use single quotes for simple strings
const name = 'John';

// Use template literals for interpolation or multi-line
const greeting = `Hello, ${name}!`;
const query = `
  SELECT *
  FROM users
  WHERE active = true
`;
```

### Semicolons
```typescript
// Always use explicit semicolons
const value = 42;
function process() { }
```

### Object & Array Formatting
```typescript
// Trailing commas for multi-line
const user = {
  name: 'John',
  email: 'john@example.com',
  age: 30,
};

const items = [
  'apple',
  'banana',
  'orange',
];
```

---

## Type System

### Type Inference
```typescript
// Let TypeScript infer obvious types
const name = 'John';              // string inferred
const count = 42;                 // number inferred
const items = ['a', 'b', 'c'];    // string[] inferred

// Annotate when not obvious or for clarity
function processUser(user: User): ProcessedUser { }
const config: AppConfig = loadConfig();
```

### Prefer `unknown` over `any`
```typescript
// Bad: loses type safety
function parse(input: any): any { }

// Good: forces type checking
function parse(input: unknown): Result {
  if (typeof input === 'string') {
    return parseString(input);
  }
  throw new Error('Invalid input');
}
```

### Interfaces vs Type Aliases
```typescript
// Use interfaces for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type aliases for unions, intersections, primitives
type UserId = string;
type Status = 'active' | 'inactive' | 'pending';
type UserWithOrders = User & { orders: Order[] };
```

### Array Types
```typescript
// Use T[] for simple types
const names: string[] = [];
const users: User[] = [];

// Use Array<T> for complex types (readability)
const handlers: Array<(event: Event) => void> = [];
```

### Nullability
```typescript
// Use optional properties
interface User {
  name: string;
  nickname?: string;  // Good: optional
}

// Avoid union with undefined
interface User {
  nickname: string | undefined;  // Avoid
}

// Handle null/undefined early
function processUser(user: User | null) {
  if (!user) {
    return null;
  }
  // user is now User
  return transform(user);
}
```

### Readonly
```typescript
// Mark non-reassigned properties as readonly
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

class UserService {
  private readonly repository: UserRepository;

  constructor(repository: UserRepository) {
    this.repository = repository;
  }
}
```

---

## Clean Code Principles

### Write Self-Documenting Code
```typescript
// Bad
function calc(a: number, b: number) {
  return a * b * 1.1;
}

// Good
function calculateTotalWithTax(price: number, quantity: number): number {
  const subtotal = price * quantity;
  const tax = subtotal * TAX_RATE;
  return subtotal + tax;
}
```

### Keep Functions Small & Focused
```typescript
// Bad: doing too much
async function processOrder(order: Order) {
  // validate (20 lines)
  // calculate (15 lines)
  // save (10 lines)
  // notify (15 lines)
}

// Good: single responsibility
async function processOrder(order: Order): Promise<ProcessedOrder> {
  const validated = validateOrder(order);
  const priced = calculateTotals(validated);
  const saved = await orderRepository.save(priced);
  await notificationService.sendConfirmation(saved);
  return saved;
}
```

### Avoid Deep Nesting
```typescript
// Bad
function processUser(user: User | null) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission('admin')) {
        // logic here
      }
    }
  }
}

// Good: early returns
function processUser(user: User | null) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission('admin')) return;

  // logic here
}
```

### Comments: Explain Why, Not What
```typescript
// Bad: explains what (obvious)
// Increment counter
counter++;

// Good: explains why (not obvious)
// Reset after successful connection to prevent accumulated retries
retryCount = 0;
```

---

## OOP & SOLID (Pragmatically)

> Apply when they add value. Don't create abstractions for hypothetical future needs.

### Single Responsibility
```typescript
// Good: focused class
class OrderPriceCalculator {
  calculate(order: Order): Money { }
}

// Simple case: function is fine
function calculateOrderPrice(order: Order): number {
  return order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

### Dependency Injection
```typescript
// Good: injectable dependencies
class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService,
  ) { }
}

// Simple case: default values are fine
class SimpleService {
  constructor(
    private readonly client: HttpClient = new HttpClient(),
  ) { }
}
```

### When NOT to Over-Engineer
```typescript
// Bad: interface for single implementation
interface UserRepository { }
class UserRepositoryImpl implements UserRepository { }

// Good: just use the class
class UserRepository { }

// Rule: Wait for 2-3 real use cases before abstracting
```

---

## Functional Programming (Balanced)

### Prefer Immutability
```typescript
// Use const by default
const users = ['John', 'Jane'];

// Use readonly for arrays that shouldn't change
function processUsers(users: readonly User[]): void { }

// Use spread for immutable updates
const updated = { ...user, name: 'New Name' };
const newItems = [...items, newItem];
```

### Array Methods
```typescript
// Good: readable chain
const activeAdminEmails = users
  .filter(user => user.isActive)
  .filter(user => user.role === 'admin')
  .map(user => user.email);

// Don't over-chain: break into steps if complex
const activeUsers = users.filter(user => user.isActive);
const adminUsers = activeUsers.filter(user => user.role === 'admin');
const emails = adminUsers.map(user => user.email);
```

### Avoid Over-Functional Code
```typescript
// Bad: too clever
const result = items
  .reduce((acc, item) => {
    const key = item.category;
    return { ...acc, [key]: [...(acc[key] || []), item] };
  }, {} as Record<string, Item[]>);

// Good: clear and readable
const grouped = new Map<string, Item[]>();
for (const item of items) {
  const existing = grouped.get(item.category) || [];
  grouped.set(item.category, [...existing, item]);
}
```

### Pure Functions When Possible
```typescript
// Good: pure function, easy to test
function calculateDiscount(price: number, percentage: number): number {
  return price * (1 - percentage / 100);
}

// Avoid: side effects hidden in function
function calculateDiscount(price: number, percentage: number): number {
  logger.log('Calculating discount');  // Side effect
  analytics.track('discount');          // Side effect
  return price * (1 - percentage / 100);
}
```

---

## Functions

### Function Declarations vs Arrow Functions
```typescript
// Use function declarations for top-level named functions
function processOrder(order: Order): ProcessedOrder { }

// Use arrow functions for callbacks and inline functions
const activeUsers = users.filter(user => user.isActive);

// Use arrow functions to preserve 'this'
class UserService {
  private handleClick = () => {
    this.process();
  };
}
```

### Parameters
```typescript
// Use default parameters
function createUser(name: string, role: Role = Role.USER): User { }

// Use rest parameters instead of arguments
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}

// Use object parameters for many options
function createRequest(options: {
  url: string;
  method?: string;
  headers?: Record<string, string>;
  timeout?: number;
}): Request { }
```

### Return Types
```typescript
// Annotate complex return types for clarity
function parseConfig(input: string): AppConfig { }

// Let TypeScript infer simple returns
const double = (n: number) => n * 2;
```

---

## Classes

### Structure
```typescript
class UserService {
  // 1. Static properties
  private static readonly instance: UserService;

  // 2. Instance properties
  private readonly repository: UserRepository;
  private cache: Map<string, User>;

  // 3. Constructor
  constructor(repository: UserRepository) {
    this.repository = repository;
    this.cache = new Map();
  }

  // 4. Public methods
  async findUser(id: string): Promise<User | null> { }

  // 5. Private methods
  private validateId(id: string): void { }
}
```

### Parameter Properties
```typescript
// Use parameter properties to reduce boilerplate
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly emailService: EmailService,
  ) { }
}

// Instead of
class UserService {
  private readonly repository: UserRepository;
  private readonly emailService: EmailService;

  constructor(repository: UserRepository, emailService: EmailService) {
    this.repository = repository;
    this.emailService = emailService;
  }
}
```

### Visibility
```typescript
// Use TypeScript's private, not #private
class Service {
  private secret: string;  // Good
  #secret: string;         // Avoid
}

// Default to private, expose only what's needed
class UserService {
  private cache: Map<string, User>;

  public findUser(id: string): User | null { }
}
```

---

## Error Handling

### Throw Only Error Objects
```typescript
// Bad: throwing primitives
throw 'Something went wrong';
throw 404;

// Good: throw Error instances
throw new Error('Something went wrong');
throw new NotFoundError(`User ${id} not found`);
```

### Custom Errors
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}
```

### Result Pattern for Expected Failures
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function parseJson(input: string): Result<unknown> {
  try {
    return { success: true, data: JSON.parse(input) };
  } catch (e) {
    return { success: false, error: e as Error };
  }
}

// Usage
const result = parseJson(input);
if (result.success) {
  console.log(result.data);
} else {
  console.error(result.error.message);
}
```

### Null Checks
```typescript
// Use == null to check both null and undefined
if (value == null) {
  return defaultValue;
}

// Use strict equality for other comparisons
if (status === 'active') { }
```

---

## Testing

### Descriptive Names
```typescript
describe('UserService', () => {
  describe('findUser', () => {
    it('should return null when user does not exist', () => { });
    it('should throw error when id is invalid', () => { });
  });
});
```

### Arrange-Act-Assert
```typescript
it('should calculate correct total with discount', () => {
  // Arrange
  const order: Order = {
    items: [{ price: 100, quantity: 2 }],
    discountPercent: 10,
  };

  // Act
  const total = calculator.calculateTotal(order);

  // Assert
  expect(total).toBe(180);
});
```

### Test One Thing
```typescript
// Bad: testing multiple behaviors
it('should validate and save user', () => { });

// Good: separate tests
it('should reject user with invalid email', () => { });
it('should save valid user to repository', () => { });
```

---

## Anti-Patterns to Avoid

### Over-Engineering
```typescript
// Bad
interface StringProcessor { process(s: string): string; }
class UpperCaseProcessor implements StringProcessor { }
class ProcessorFactory { create(): StringProcessor { } }

// Good
function toUpperCase(s: string): string {
  return s.toUpperCase();
}
```

### Using `any`
```typescript
// Bad
function process(data: any): any { }

// Good
function process<T>(data: T): ProcessedData<T> { }
function process(data: unknown): Result { }
```

### God Classes
```typescript
// Bad
class UserManager {
  createUser() { }
  sendEmail() { }
  generateReport() { }
  // ... 50 more methods
}

// Good: split by responsibility
class UserService { }
class EmailService { }
class ReportGenerator { }
```

### Copy-Paste Code
```typescript
// Bad: duplicated validation
function validateUser(user: User) { /* same logic */ }
function validateAdmin(admin: Admin) { /* same logic */ }

// Good: reusable
interface HasContactInfo {
  name: string;
  email: string;
}

function validateContactInfo<T extends HasContactInfo>(entity: T): void {
  if (!entity.name) throw new Error('Name required');
  if (!entity.email) throw new Error('Email required');
}
```

### Disallowed Patterns
```typescript
// Never use
var x = 1;                    // Use const/let
new String('foo');            // Use primitives
eval('code');                 // Security risk
with (obj) { }                // Deprecated
```

---

## Summary

| Do | Don't |
|----|-------|
| Use `const`/`let` | Use `var` |
| Use `unknown` | Use `any` |
| Use named exports | Use default exports |
| Throw `Error` objects | Throw primitives |
| Use strict equality `===` | Use loose equality `==` |
| Write readable code | Write clever code |
| Keep it simple | Over-engineer |
| Abstract when needed | Abstract preemptively |

> **Remember**: Code is read more often than written. Optimize for readability.
