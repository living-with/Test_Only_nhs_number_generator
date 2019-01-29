"""Test cases for the generate_nhs_numbers module."""

from __future__ import unicode_literals
import unittest
from generate_nhs_numbers import (deterministic_nhs_number_generator, add_separators, calculate_check_digit,
                                  random_nhs_number_generator, is_valid_nhs_number, remove_separators)


class TestNHSNumbers(unittest.TestCase):

    def setUp(self):
        self.deterministic_nhs_generator = deterministic_nhs_number_generator()
        self.random_nhs_generator = random_nhs_number_generator()

    def test_is_valid(self):
        """Test that we can tell a valid number from an invalid one."""
        self.assertTrue(is_valid_nhs_number('0000000000'))
        self.assertFalse(is_valid_nhs_number('0000000001'))   # invalid check digit
        self.assertFalse(is_valid_nhs_number('000000r000'))   # not a number
        self.assertFalse(is_valid_nhs_number('000000000'))    # too short
        self.assertFalse(is_valid_nhs_number('00000000000'))  # too long

    def test_no_duplicates(self):
        """Test that the deterministic generator doesn't repeat itself over a small range."""
        nhs_number_list = [next(self.deterministic_nhs_generator) for i in range(100)]
        the_set = set(nhs_number_list)
        self.assertEqual(len(nhs_number_list), len(set(nhs_number_list)))

    def test_all_deterministic_nums_are_valid(self):
        """Test that all numbers generated by the deterministic generator are valid."""
        for i in range(100):
            self.assertTrue(is_valid_nhs_number(next(self.deterministic_nhs_generator)))

    def test_deterministic_nhs_numbers_arguments(self):
        """Test that we can specify the range of random NHS numbers."""

        # There is no valid NHS number of the form '000000006#' so it will skip to the next valid one
        gen1 = deterministic_nhs_number_generator([(7, 100)])
        self.assertEqual('0000000078', next(gen1))

        # Once it exhausts all of the possibilities, it should end
        gen2 = deterministic_nhs_number_generator([(600000000, 600000001)])
        list2 = list(gen2)
        self.assertListEqual(['6000000006', '6000000014'], list2)

        # It should be able to handle two ranges
        gen3 = deterministic_nhs_number_generator([(600000000, 600000001), (6, 7)])
        list3 = list(gen3)
        self.assertListEqual(['6000000006', '6000000014', '0000000078'], list3)

    def test_random_range_exceptions(self):
        """Test that exceptions are raised by invalid ranges."""
        def call_low_high():
            next(random_nhs_number_generator([(8, 4)]))

        def call_fine_then_bad():
            next(random_nhs_number_generator([(4, 8), (10, 2)]))

        def call_one_possible_value():
            next(random_nhs_number_generator([(6, 6)]))

        self.assertRaises(ValueError, call_low_high)
        self.assertRaises(ValueError, call_fine_then_bad)
        self.assertRaises(ValueError, call_one_possible_value)

    def test_add_separators(self):
        """Test that we can add different kinds of separator."""
        no_dashes = '0000000027'
        self.assertEqual('000 000 0027', add_separators(no_dashes))
        self.assertEqual('000-000-0027', add_separators(no_dashes, separator='-'))
        self.assertEqual('000 000 0027', add_separators(no_dashes, separator=' '))

    def test_random_nhs_numbers_are_valid(self):
        """Test that all of the random NHS numbers are valid."""
        for i in range(100):
            self.assertTrue(is_valid_nhs_number(next(self.random_nhs_generator)))

    def test_random_nhs_numbers_arguments(self):
        """Test that we can specify the range of random NHS numbers."""
        gen = random_nhs_number_generator([(489000000, 489999999)])
        for i in range(100):
            nhs_number = next(gen)
            self.assertTrue(nhs_number.startswith('489') and is_valid_nhs_number(nhs_number))

    def test_deterministic_range_exceptions(self):
        """Test that exceptions are raised by invalid ranges."""
        def call_low_high():
            next(deterministic_nhs_number_generator([(8, 4)]))

        def call_fine_then_bad():
            next(deterministic_nhs_number_generator([(4, 8), (10, 2)]))

        def call_one_possible_value():
            next(deterministic_nhs_number_generator([(6, 6)]))

        self.assertRaises(ValueError, call_low_high)
        self.assertRaises(ValueError, call_fine_then_bad)
        self.assertRaises(ValueError, call_one_possible_value)

    def test_deterministic_default_ranges(self):
        """Test that the first number is as we would expect."""
        self.assertEqual('400000000', next(self.deterministic_nhs_generator)[0:-1])

    def test_random_default_ranges(self):
        """Test that a sample of generated numbers all fall in the ranges we would expect"""
        for _ in range(100):
            nhs_number = int(next(self.random_nhs_generator)[0:-1])
            in_lower_range = 400000000 <= nhs_number <= 499999999
            in_higher_range = 600000000 <= nhs_number <= 708800001
            self.assertTrue(in_lower_range or in_higher_range, "Number was {}.".format(nhs_number))
            [(400000000, 499999999), (600000000, 708800001)]

    def test_remove_separators(self):
        """Test that we can remove different kinds of separators."""
        self.assertEqual("7645529342", remove_separators("764-552-9342"))
        self.assertEqual("7645529342", remove_separators("764 552 9342"))
        self.assertEqual("7645529342", remove_separators("7645529342"))


if __name__ == "__main__":
    unittest.main()
