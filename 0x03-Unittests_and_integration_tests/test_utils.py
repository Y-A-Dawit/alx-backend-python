#!/usr/bin/env python3
"""Unit tests for utils.py"""

from unittest.mock import patch, Mock
import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test case for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

    @parameterized.expand([
        ({"a": 1}, ("a", "b")),
        ({}, ("a",)),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised when path is invalid in nested map."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function in utils module."""

    @parameterized.expand([
      ("http://example.com", {"payload": True}),
      ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns the correct payload
          from a mocked HTTP response."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch(
                "utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(
                    test_url
                    )
            mock_get.assert_called_once_with(
                    test_url
                    )
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for TestMemoize"""

    def test_memoize(self):
        """Test that the memoize decorator caches the result of a_method."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(
                TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
