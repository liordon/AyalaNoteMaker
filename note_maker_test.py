import unittest

from note_maker import *

example_headers = "timestamp, name, religion, sham, ba, lu, lu, isCute, isTall, isPlayingD&D".split(", ")
name_column_in_csv = 1
first_flag_column = 7
row_with_no_categories = "0, Mr. Bean, jewish, bam, ba, shu, shu, False, false, FALSE".split(", ")
row_with_two_categories = "0, Vin Diesel, jewish, bam, ba, shu, shu, False, true, TRUE".split(", ")

inspected_row_converter = RowConverter(example_headers, name_column_in_csv, first_flag_column)


def parse_flags_of_example_row(example_row):
    return inspected_row_converter.parse_relevant_categories_from_line(example_row)[1]


class MyTestCase(unittest.TestCase):
    def test_applicantNameIsAlwaysReturnedAsFirstElementOfPair(self):
        self.assertEqual(
            inspected_row_converter.parse_relevant_categories_from_line(row_with_no_categories)[0],
            row_with_no_categories[name_column_in_csv])
        self.assertEqual(
            inspected_row_converter.parse_relevant_categories_from_line(row_with_two_categories)[0],
            row_with_two_categories[name_column_in_csv])

    def test_whenApplicantHasNoRelevantCategoriesInLine_thenEmptyListIsReturned(self):
        self.assertEqual(
            parse_flags_of_example_row(row_with_no_categories), [])

    def test_whenApplicantHasTwoCategories_thenBothAreReturned(self):
        self.assertEqual(
            len(parse_flags_of_example_row(row_with_two_categories)), 2)


if __name__ == '__main__':
    unittest.main()
