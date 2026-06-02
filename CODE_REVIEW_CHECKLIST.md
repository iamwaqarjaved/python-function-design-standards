# Function-Level Code Review Checklist

Use this checklist when reviewing Python functions in marketing analytics, ETL, reporting, and dashboard-support repositories.

## 12 review questions

1. **Does the function name clearly describe the action and business object?**
   - Good: `calculate_roas`, `normalize_campaign_name`, `validate_utm_parameters`
   - Weak: `process_data`, `fix_values`, `do_calc`

2. **Does the function follow `snake_case` naming?**
   - Avoid camelCase, PascalCase, and unclear abbreviations.

3. **Does the function have one clear responsibility?**
   - It should not load data, clean data, calculate metrics, write files, and send alerts all in one place.

4. **Are required inputs positional only when they are essential to the function?**
   - Core inputs can be positional.
   - Optional behavior should usually be keyword-only.

5. **Are defaults safe, intentional, and business-approved?**
   - Defaults should not silently change business meaning.

6. **Are `*args` and `**kwargs` avoided unless there is a strong reason?**
   - They should not hide required inputs or unclear behavior.

7. **Does every public function include type hints?**
   - Return types should be explicit.
   - Use `str | None` or `Optional[str]` consistently.

8. **Does the docstring explain business behavior, not just restate the code?**
   - Include edge cases, assumptions, and return behavior.

9. **Are comprehensions readable and limited to simple transformations or filters?**
   - Replace deeply nested or side-effect-driven comprehensions with loops.

10. **Are lambdas only used for simple local expressions?**
    - Business logic should be placed in named functions.

11. **Is the function testable without hidden global state?**
    - Avoid hidden dependencies on current time, environment variables, files, or APIs unless injected.

12. **Are important edge cases handled?**
    - Examples: zero spend, missing campaign names, null UTM fields, empty lists, invalid dates, currency mismatches.
