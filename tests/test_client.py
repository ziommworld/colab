import os
import unittest
import gspread
import pandas as pd
import warnings
from src.shared.client import GoogleSheetsClient
from src.shared.util import get_timestamp

warnings.filterwarnings("ignore", category=ResourceWarning)

SKIP_SPREADSHEETS = False
SKIP_WORKSHEETS = False


class TestGoogleSheetsClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Construct the absolute path to the JSON keyfile
        current_dir = os.path.dirname(__file__)
        cls.json_keyfile_path = os.path.abspath(
            os.path.join(current_dir, "..", "env", "colab.json")
        )
        cls.client = GoogleSheetsClient(json_keyfile_path=cls.json_keyfile_path)

    def setUp(self):
        # Initialize the GoogleSheetsClient with the correct JSON keyfile path
        self.test_spreadsheet_name = f"Test_Spreadsheet_{get_timestamp()}"
        self.test_worksheet_name = "Test_Worksheet"

    def tearDown(self):
        # Attempt to clean up any created spreadsheet
        try:
            self.client.delete_spreadsheet(self.test_spreadsheet_name)
        except Exception as e:
            pass  # Spreadsheet already deleted or not found, ignore this error

    # ===================== SPREADSHEETS =====================

    @unittest.skipIf(SKIP_SPREADSHEETS, "skip spreadsheets tests")
    def test_create_spreadsheet(self):
        # Create a new spreadsheet
        created_spreadsheet = self.client.create_spreadsheet(self.test_spreadsheet_name)

        # Verify that the spreadsheet was created
        self.assertIsNotNone(created_spreadsheet)
        self.assertEqual(created_spreadsheet.title, self.test_spreadsheet_name)

    @unittest.skipIf(SKIP_SPREADSHEETS, "skip spreadsheets tests")
    def test_read_existing_spreadsheet(self):
        # First, ensure the spreadsheet exists
        self.client.create_spreadsheet(self.test_spreadsheet_name)

        # Now, try reading the existing spreadsheet
        spreadsheet = self.client.read_spreadsheet(self.test_spreadsheet_name)
        self.assertEqual(spreadsheet.title, self.test_spreadsheet_name)

    @unittest.skipIf(SKIP_SPREADSHEETS, "skip spreadsheets tests")
    def test_read_non_existing_spreadsheet(self):
        # Attempt to read a non-existing spreadsheet, should create it
        spreadsheet = self.client.read_spreadsheet(self.test_spreadsheet_name)

        # Verify that a new spreadsheet was created
        self.assertIsNotNone(spreadsheet)
        self.assertEqual(spreadsheet.title, self.test_spreadsheet_name)

    @unittest.skipIf(SKIP_SPREADSHEETS, "skip spreadsheets tests")
    def test_delete_spreadsheet(self):
        # First, ensure the spreadsheet exists
        self.client.create_spreadsheet(self.test_spreadsheet_name)

        # Now, delete the spreadsheet
        self.client.delete_spreadsheet(self.test_spreadsheet_name)

        # Verify that the spreadsheet no longer exists
        self.assertFalse(self.client.spreadsheet_exists(self.test_spreadsheet_name))

    # ===================== WORKSHEETS =====================

    @unittest.skipIf(SKIP_WORKSHEETS, "skip worksheets tests")
    def test_create_worksheet(self):
        # Ensure the spreadsheet exists
        self.client.read_spreadsheet(self.test_spreadsheet_name)

        # Create a new worksheet in the existing spreadsheet
        self.client.create_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )

        # Verify that the worksheet was created
        worksheets = self.client.get_all_worksheets(self.test_spreadsheet_name)
        worksheet_titles = [ws.title for ws in worksheets]
        self.assertIn(self.test_worksheet_name, worksheet_titles)

    @unittest.skipIf(SKIP_WORKSHEETS, "skip worksheets tests")
    def test_read_non_existing_worksheet_creates_new(self):
        # Ensure the spreadsheet exists
        self.client.read_spreadsheet(self.test_spreadsheet_name)

        # Attempt to read a non-existing worksheet, should create it
        worksheet = self.client.read_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )

        # Verify that a new worksheet was created
        self.assertEqual(worksheet.title, self.test_worksheet_name)

    @unittest.skipIf(SKIP_WORKSHEETS, "skip worksheets tests")
    def test_update_worksheet(self):
        # Ensure the spreadsheet exists
        self.client.read_spreadsheet(self.test_spreadsheet_name)

        # Ensure the worksheet exists
        self.client.create_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )

        # Create a sample DataFrame
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        # Update the worksheet with the DataFrame
        self.client.update_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name, df
        )

        # Read back the data to verify the update
        worksheet = self.client.read_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )
        data = worksheet.get_all_values()
        header, *rows = data

        # Convert the rows data to integers for comparison
        rows_as_integers = [[int(value) for value in row] for row in rows]

        # Verify that the header and rows match the DataFrame
        self.assertEqual(header, list(df.columns))
        self.assertEqual(rows_as_integers, df.values.tolist())

    @unittest.skipIf(SKIP_WORKSHEETS, "skip worksheets tests")
    def test_delete_worksheet(self):
        # Ensure the spreadsheet and worksheet exist
        self.client.read_spreadsheet(self.test_spreadsheet_name)
        self.client.create_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )

        # Now, delete the worksheet
        self.client.delete_worksheet(
            self.test_spreadsheet_name, self.test_worksheet_name
        )

        # Verify that the worksheet no longer exists
        worksheets = self.client.get_all_worksheets(self.test_spreadsheet_name)
        worksheet_titles = [ws.title for ws in worksheets]
        self.assertNotIn(self.test_worksheet_name, worksheet_titles)


if __name__ == "__main__":
    unittest.main()
