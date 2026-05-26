# Mystery Delivery System – FastBox
Overview

This assignment simulates a one-day delivery operation for FastBox. Packages are assigned to the nearest delivery agent based on Euclidean distance, deliveries are simulated using direct paths, and performance metrics are calculated.

Approach

Parsed and normalized JSON input data

Assigned packages to the nearest agent

Simulated delivery routes and distances

Calculated per-agent efficiency and identified the best agent

Generated output reports in JSON and CSV formats

Features

Handles inconsistent input keys (warehouse / warehouse_id)

Supports multiple input files via file upload

Includes random delivery delays and ASCII route visualization

Output

<input>_report.json – detailed agent performance

<input>_top_agent.csv – best agent summary

Requirements

Python 3.x (standard libraries only)
