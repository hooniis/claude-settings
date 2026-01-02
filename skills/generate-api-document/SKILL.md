---
name: generating-api-document
description: Generates API specification documents in AsciiDoc format from controller code. Analyzes endpoints to extract paths, parameters (path, query, form, body), and response structures. Use when the user asks to generate API documentation, create API specs, or document REST endpoints.
---

# API Document Generator

$ARGUMENTS

## Instructions

Generate API specification documents in AsciiDoc format by analyzing controller code.

### Workflow

1. **Analyze the controller/code** provided by the user
2. **Extract API information**:
   - HTTP method (GET, POST, PUT, DELETE, PATCH)
   - API path with path variables
   - Path parameters
   - Query parameters
   - Form parameters (if multipart/form-data)
   - Request body fields
   - Response object structure
3. **Generate AsciiDoc** using the template structure
4. **Save file** with name matching the API name (kebab-case)

---

## Code Analysis Checklist

### 1. Endpoint Identification

Look for annotations/decorators:

**Spring (Java/Kotlin)**:
- `@RestController`, `@Controller`
- `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`
- Base path from class-level `@RequestMapping`

**NestJS (TypeScript)**:
- `@Controller()`, `@Get()`, `@Post()`, `@Put()`, `@Delete()`, `@Patch()`

**Express/Fastify**:
- `app.get()`, `app.post()`, `router.get()`, etc.

### 2. Parameter Extraction

**Path Parameters**:
- Spring: `@PathVariable`
- NestJS: `@Param()`
- Express: `req.params`

**Query Parameters**:
- Spring: `@RequestParam`
- NestJS: `@Query()`
- Express: `req.query`

**Form Parameters**:
- Spring: `@RequestParam` with `multipart/form-data`, `@RequestPart`
- NestJS: `@Body()` with `FileInterceptor`

**Request Body**:
- Spring: `@RequestBody`
- NestJS: `@Body()`
- Express: `req.body`

### 3. Request/Response Object Analysis

- Trace DTO/Model classes to extract all fields
- Note field types, required/optional status
- Check validation annotations (`@NotNull`, `@NotBlank`, `@Size`, etc.)
- Look for format hints (`@DateTimeFormat`, `@JsonFormat`)
- Identify nested objects and arrays

### 4. Response Structure

- Check return type of the method
- Analyze wrapper classes (e.g., `ApiResponse<T>`, `ResponseEntity<T>`)
- Extract `data` field structure
- Document nested objects separately

---

## Output Template Structure

Reference: [TEMPLATE.adoc](TEMPLATE.adoc)

### Document Header

```asciidoc
= {API Feature Title} API
API Specification Document;
:doctype: book
:icons: font
:source-highlighter: highlightjs
:toc: left
:toclevels: 2
:table-stripes: hover
:sectanchors:
:sectnums:
:sectnumlevels: 2
```

### Overview Section

```asciidoc
= Overview
.본 문서는 {feature} API 연동하기 위한 문서입니다.
[NOTE]
--
- {API에 대한 전반적인 설명}
--
```

### Server List (Use standard template)

```asciidoc
[[server-list]]
== API Server List

.API Server List
|===
| Phase | Host | Description | IP

| `DEVELOP (TEST)`
| 별도 제공
| 테스트 서버
| 별도 제공

| `PRODUCTION (REAL)`
| 별도 제공
| 운영 서버 (상용)
| 별도 제공
|===
```

### HTTP Verbs (Use standard template)

Include the standard HTTP status code table from TEMPLATE.adoc.

### API Format (Use standard template)

Include the standard API format notes from TEMPLATE.adoc.

### API Endpoints Section

For each API endpoint:

```asciidoc
= APIs

[[{api-anchor}]]
== {API Title}

./{api-path}
[NOTE]
--
- {API 설명}
--

=== Http Request

.request sample
[source,httprequest]
----
{METHOD} {path} HTTP/1.1
Host: api.example.com
Content-Type: application/json

{request body JSON if applicable}
----
```

#### Path Parameters (if any)

```asciidoc
.Path Parameters
|===
|Path|Description

|`{paramName}`
|{파라미터 설명}
|===
```

#### Query Parameters (if any)

```asciidoc
.Query Parameters
|===
|Parameter|Required|Description

|`{paramName}`
|{true/false}
|{파라미터 설명}
|===
```

#### Form Parameters (if any)

```asciidoc
.Form Parameters
|===
|Parameter|Format|Description

|`{paramName}`
|{String/File/etc}
|{파라미터 설명}
|===
```

#### Request Body (if any)

```asciidoc
.Request Fields
|===
|Path|Type|Required|Format|Description

|`{fieldName}`
|{String/Number/Boolean/Array/Object}
|{true/false}
|{format if applicable}
|{필드 설명}
|===
```

### Response Section

```asciidoc
=== Http Response

.response sample
[source,httpresponse]
----
HTTP/1.1 200 OK
Content-Type: application/json
{
  "code": "200",
  "message": "Success",
  "data": {
    // actual response data structure
  }
}
----

.Response Fields `data`
|===
|Path|Type|Format|Description

|`{fieldName}`|{Type}|{format}|{필드 설명}
|===
```

For nested objects, create separate tables:

```asciidoc
.Response Fields `data.{nestedObject}`
|===
|Path|Type|Format|Description

|`{fieldName}`|{Type}|{format}|{필드 설명}
|===
```

### Codes Section (if applicable)

```asciidoc
= Codes

[[{code-anchor}]]
== {Code Category}

.{Code List Title}
[cols="2,3"]
|===
| Code | Description
| `{CODE_VALUE}` | {코드 설명}
|===
```

---

## Field Type Mapping

| Source Type | AsciiDoc Type |
|-------------|---------------|
| String, CharSequence | String |
| int, Integer, long, Long, BigInteger | Number |
| double, Double, float, Float, BigDecimal | Number |
| boolean, Boolean | Boolean |
| List, Set, Collection, Array | Array |
| Object, Custom Class, Map | Object |
| LocalDate | String (format: `yyyy-MM-dd`) |
| LocalDateTime | String (format: `yyyy-MM-dd'T'HH:mm:ss`) |
| Instant, ZonedDateTime | String (format: `yyyy-MM-dd'T'HH:mm:ssZ`) |
| Enum | String (list enum values in description) |

---

## Output File Naming

Generate filename from API name in kebab-case:

| API Name | Output File |
|----------|-------------|
| 사용자 조회 API | `user-inquiry-api.adoc` |
| Create Order | `create-order.adoc` |
| GET /api/v1/users/{id} | `get-user-by-id.adoc` |

---

## Example

**Input**: Spring Controller

```kotlin
@RestController
@RequestMapping("/api/v1/orders")
class OrderController(
    private val orderService: OrderService
) {
    @PostMapping
    fun createOrder(
        @RequestBody request: CreateOrderRequest
    ): ApiResponse<OrderResponse> {
        return ApiResponse.success(orderService.create(request))
    }
}

data class CreateOrderRequest(
    @field:NotBlank
    val productId: String,
    @field:Min(1)
    val quantity: Int,
    val memo: String? = null
)

data class OrderResponse(
    val orderId: String,
    val productId: String,
    val quantity: Int,
    val totalPrice: BigDecimal,
    val status: OrderStatus,
    val createdAt: LocalDateTime
)

enum class OrderStatus { PENDING, CONFIRMED, SHIPPED, DELIVERED }
```

**Output**: `create-order.adoc`

```asciidoc
= 주문 생성 API
API Specification Document;
:doctype: book
:icons: font
:source-highlighter: highlightjs
:toc: left
:toclevels: 2
:table-stripes: hover
:sectanchors:
:sectnums:
:sectnumlevels: 2

= Overview
.본 문서는 주문 생성 API 연동하기 위한 문서입니다.
[NOTE]
--
- 새로운 주문을 생성합니다.
--

// ... Server List, HTTP Verbs, API Format sections ...

= APIs

[[create-order]]
== 주문 생성

./api/v1/orders
[NOTE]
--
- 새로운 주문을 생성합니다.
--

=== Http Request

.request sample
[source,httprequest]
----
POST /api/v1/orders HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "productId": "PROD001",
  "quantity": 2,
  "memo": "배송 메모"
}
----

.Request Fields
|===
|Path|Type|Required|Format|Description

|`productId`
|String
|true
|
|상품 ID

|`quantity`
|Number
|true
|최소값: 1
|주문 수량

|`memo`
|String
|false
|
|주문 메모
|===

=== Http Response

.response sample
[source,httpresponse]
----
HTTP/1.1 200 OK
Content-Type: application/json
{
  "code": "200",
  "message": "Success",
  "data": {
    "orderId": "ORD20240101001",
    "productId": "PROD001",
    "quantity": 2,
    "totalPrice": 50000,
    "status": "PENDING",
    "createdAt": "2024-01-01T10:30:00"
  }
}
----

.Response Fields `data`
|===
|Path|Type|Format|Description

|`orderId`|String| |주문 ID
|`productId`|String| |상품 ID
|`quantity`|Number| |주문 수량
|`totalPrice`|Number| |총 주문 금액
|`status`|String|`PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`|주문 상태
|`createdAt`|String|`yyyy-MM-dd'T'HH:mm:ss`|주문 생성 일시
|===

= Codes

[[order-status]]
== 주문 상태 코드

.Order Status Code
[cols="2,3"]
|===
| Code | Description
| `PENDING` | 주문 대기
| `CONFIRMED` | 주문 확정
| `SHIPPED` | 배송 중
| `DELIVERED` | 배송 완료
|===
```
