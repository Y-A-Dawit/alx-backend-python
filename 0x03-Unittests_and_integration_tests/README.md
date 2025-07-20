# 0. Parameterize a Unit Test

This task demonstrates how to write unit tests using Python's `unittest` framework and `parameterized` library to test the `access_nested_map` function from `utils.py`.

## Goal

Write a parameterized unit test that validates the correct behavior of the `access_nested_map` function when accessing values from nested dictionaries.

## Tools & Libraries Used

- Python 3.7
- `unittest` (Python built-in testing framework)
- `parameterized` (3rd party package for test parameterization)

## Task Summary

- Create a class `TestAccessNestedMap` that inherits from `unittest.TestCase`.
- Write a test method decorated with `@parameterized.expand` to test multiple input cases.
- Use `assertEqual` to check that the returned values match expected results.

## Example Test Cases

```python
nested_map = {"a": 1}, path = ("a",)
nested_map = {"a": {"b": 2}}, path = ("a",)
nested_map = {"a": {"b": 2}}, path = ("a", "b")
