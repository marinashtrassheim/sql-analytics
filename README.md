# ClickHouse Query Optimization Demo

A hands-on project demonstrating query optimization in ClickHouse using:
- Materialized Views
- Window functions vs correlated subqueries
- Performance benchmarking with `EXPLAIN` and execution time

## Overview

This project simulates an e-commerce sales database with **2 million records**. It compares the performance of four SQL queries in two pairs:

| Pair | Query | Method | Optimized Approach |
|------|-------|--------|---------------------|
| 1 | Daily revenue by category | Plain aggregation | Materialized View (`SummingMergeTree`) |
| 2 | Top-3 categories per region | Correlated subquery | Window function (`RANK()`) |

The results are visualized in a Streamlit dashboard showing:
- Median execution time per query
- Number of rows read (if available)
- Execution plans (`EXPLAIN`)

## Stack

- **ClickHouse** – columnar OLAP database
- **Docker** – containerized environment
- **Python** – data generation, benchmarking, and dashboard
- **Streamlit** – interactive visualization

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git (optional)

### Run the Project

1. Clone the repository:
   ```bash
   git clone git@github.com:marinashtrassheim/sql-analytics.git
   cd sql-analytics

2. Build and start all services:
   ```bash
   docker-compose up --build

This will:

Start ClickHouse
Generate 2 million sales records (spanning 3 years)
Run the benchmark (executes each query 5 times)
Launch the Streamlit dashboard

3. Open the dashboard in your browser:
   ```bash
   http://localhost:8501

### Results
After the benchmark completes, you'll see a summary in the terminal:

| Query               | Median Time (s) |
|---------------------|-----------------|
| query1_mv           | 0.0035          |
| query1_plain        | 0.0093          |
| query2_window       | 0.0103          |
| query2_correlated   | 0.0220          |

Key observations:

- **The materialized view is 2.6× faster than plain aggregation.**
- **Window function is 2.1× faster than the correlated subquery.**

The dashboard also displays:
- Bar charts of execution times and read rows.
- Full `EXPLAIN` plans for each query (expandable).

### Clean up
```bash
docker-compose down -v
