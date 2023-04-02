from django.test import TestCase

import unittest
from .data_processing.dataframe_compliance import *
from .data_processing.statistics_extractor import *
import os

class DataframeComplianceTest(unittest.TestCase):
    def test_empty_dataframe(self):
        compliance = evaluate_dataframe(os.path.join('test_files', 'empty_data.csv'))
        self.assertFalse(compliance['not_empty'])

    def test_wrong_columns(self):
        compliance = evaluate_dataframe(os.path.join('test_files', 'wrong_columns.csv'))
        self.assertFalse(compliance['columns_valid'])

class DataframeStatisticsTest(unittest.TestCase):
    def test_statistics(self):
        df = pd.read_csv(os.path.join('test_files', 'stats_test.csv'))
        statistics = generate_statistics(df, ['review_time', 'merge_time'])
        self.assertTrue(len(statistics) == 3)
        self.assertTrue(any([s['team_name'] == 'Application' for s in statistics]))
        self.assertTrue(any([s['team_name'] == 'Development' for s in statistics]))
        self.assertTrue(any([s['team_name'] == 'all_data' for s in statistics]))

        application = [s for s in statistics if s['team_name'] == 'Application' ][0]
        development = [s for s in statistics if s['team_name'] == 'Development' ][0]
        all_data = [s for s in statistics if s['team_name'] == 'all_data' ][0]

        self.assertTrue(application['review_time']['mean_val'] == 1.0)
        self.assertTrue(application['review_time']['std_val'] == 0)
        self.assertTrue(development['review_time']['mean_val'] == 3.0)
        self.assertTrue(development['review_time']['std_val'] == 0)
        self.assertTrue(application['merge_time']['mean_val'] == 2.0)
        self.assertTrue(application['merge_time']['std_val'] == 0)
        self.assertTrue(development['merge_time']['mean_val'] == 4.0)
        self.assertTrue(development['merge_time']['std_val'] == 0)

        self.assertTrue(all_data['review_time']['std_val'] != 0)
        self.assertTrue(all_data['merge_time']['std_val'] != 0)