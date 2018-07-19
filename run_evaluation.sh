#!/bin/sh

python evaluate_multiple_submissions.py submissions/validation/ data/REFUGE-Validation400/GT/ submissions/validation-temp submissions/validation-results

python generate_leaderboards.py submissions/validation-results/table_of_results.csv submissions/validation-results/
 