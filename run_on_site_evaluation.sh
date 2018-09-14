#!/bin/sh

python evaluate_multiple_submissions.py submissions/test/ data/test_dataset/GT/ submissions/test-temp submissions/test-results

python generate_leaderboards.py submissions/test-results/table_of_results.csv submissions/test-results/
 