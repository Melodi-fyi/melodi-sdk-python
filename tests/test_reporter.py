import unittest
from unittest.mock import patch, MagicMock
from melodi import braintrust_reporter
from io import StringIO
import os
import sys


class TestMelodiReporter(unittest.TestCase):

    @patch.dict(os.environ, {"BRAINTRUST_API_KEY": "test_api_key"})
    @patch.dict(os.environ, {"MELODI_API_KEY": "test_api_key"})
    @patch('melodi.braintrust_reporter.requests.post')
    def test_report_evaluator_result(self, mock_post):
        # Mock the responses from `requests.post` for each function call
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {'feedbackUrl': 'https://example.com/123'}),
            MagicMock(status_code=200), # for log_to_melodi_comparison_json
            MagicMock(status_code=200),  # for log_to_melodi_comparison_json
            MagicMock(status_code=200, json=lambda: {'shareableLink': 'https://example.com/share/123'})
        ]
        
        # Mock sys.stdout to capture print statements
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        
        # Call your function
        evaluator = MagicMock()
        result = MagicMock()
        result.summary.experiment_name = "Test Experiment"
        result.summary.project_name = "Test Project"
        # Mocking result.results with a list of MagicMock objects
        expected_result_1 = MagicMock(expected='Hi Foo', output='Hi Foo')
        expected_result_2 = MagicMock(expected='Hi Bar', output='Hi Bar')
        result.results = [expected_result_1, expected_result_2]


        # Call the function that is being tested
        braintrust_reporter.report_evaluator_result(evaluator, result, verbose=True, jsonl=False)
        
        # Reset sys.stdout
        sys.stdout = sys.__stdout__

        # Check if the shareable link was printed
        self.assertIn("Shareable Melodi Link", capturedOutput.getvalue())

        # Check that mock_post was called twice
        self.assertEqual(mock_post.call_count, 4)

# Run the tests
if __name__ == '__main__':
    unittest.main()
