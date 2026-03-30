# Error Handling

## Use Nullable Reference Types

Enable nullable reference types. Use `T?` to explicitly mark nullable types. Use `ArgumentNullException.ThrowIfNull()` for parameter validation. Let the compiler help you find null-related bugs.

## Exception vs Result Types

- Use exceptions for **exceptional** conditions (programming errors, system failures)
- Consider `Result<T, TError>` or `OneOf<T, TError>` for expected failures (validation, business rules)

Do not use exceptions for control flow.

## Exception Filter Clauses

Use exception filters (`catch (Exception ex) when (...)`) to catch only specific conditions. This preserves the stack trace better than re-throwing.

## Throw Helpers

Use `ArgumentNullException.ThrowIfNull()` and similar throw helpers. They are concise and inlined by the runtime.

## Custom Exceptions

Create custom exceptions only when callers need to catch and handle that specific error type. Name exceptions with `Exception` suffix. Derive from `Exception` or a more specific base. In modern .NET, do not add remoting or binary-serialization plumbing unless you are explicitly targeting a legacy interop requirement.

## ArgumentException Patterns

Use `ArgumentException` for invalid arguments. Use `ArgumentNullException` for null arguments where null is invalid. Use `ArgumentOutOfRangeException` for values outside valid range.

## Validation

Separate validation from business logic. Use validation libraries (FluentValidation, DataAnnotations) for input validation. Return validation results rather than throwing for expected validation failures.

## Never Catch and Swallow

Never catch an exception and do nothing. At minimum, log the exception. If you must swallow, document why with a comment.

## Preserve Stack Traces

When rethrowing the current exception, use `throw;` instead of `throw ex;`. The latter resets the stack trace and makes production debugging harder.

## Global Exception Handling

In ASP.NET Core, use exception handling middleware. In console apps, handle exceptions at the top level. Use `IHostApplicationLifetime` for graceful shutdown.
