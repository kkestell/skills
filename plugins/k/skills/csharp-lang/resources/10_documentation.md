# Documentation

## XML Documentation

Public APIs in reusable libraries and packages should have XML documentation. In application code, document non-obvious public surfaces and externally consumed contracts; do not add filler comments just to satisfy a rule. Use `<summary>`, `<param>`, `<returns>`, `<exception>`, and `<remarks>` as appropriate. Enable documentation file generation for libraries: `<GenerateDocumentationFile>true</GenerateDocumentationFile>`.

## Summary Style

Start summaries with a verb: "Gets...", "Calculates...", "Determines...". Avoid "This method..." or "This class...". Keep summaries concise—one sentence for simple members.

## Parameter Documentation

Document all parameters, including their purpose and any constraints. Document `cancellationToken` parameters: "The cancellation token to cancel the operation."

## Return Documentation

Document what is returned, including possible `null` values. Use `<returns>` for non-void methods.

## Exception Documentation

Document all exceptions that can be thrown, with conditions. Use `<exception cref="...">` with the exception type.

## Nullable Documentation

When returning nullable types (`T?`), document when `null` is returned. Use `<value>` for property documentation.

## README Files

Every project should have a README with:
- Brief description of what the project does
- Installation or usage instructions
- Quick start example
- Link to full documentation

## Example Code in Docs

Use `<example>` tags with code samples. Keep examples minimal but complete enough to understand usage. Avoid hypothetical code—use realistic scenarios.

## Avoid Redundant Documentation

Don't document what is obvious from the signature. The property `public int Count { get; }` needs no documentation unless there's something non-obvious about the count.

## Inherit Documentation

Use `<inheritdoc />` to inherit documentation from base classes or interfaces. Don't copy-paste documentation.
