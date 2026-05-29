# 📊 ClickHouse: Big Data for SREs

## 🌟 Introduction
ClickHouse is a fast open-source column-oriented database management system for online analytical processing (OLAP). Perfect for log analysis and monitoring at scale.

## 🟢 Level 0: What is OLAP?
In Row-oriented (MySQL/Postgres), data is stored row-by-row. In Column-oriented (ClickHouse), data is stored column-by-column, allowing massive compression and lightning-fast queries on specific fields.

## 🟡 Level 1: Performance Concepts
- **MergeTree Engine:** The most powerful engine for high-load tasks.
- **Data Compression:** Can compress data up to 10x vs Postgres.

## 🟠 Level 2: SRE Use Cases
- **Log Aggregation:** Storing billions of logs with sub-second query times.
- **Real-time Metrics:** Analyzing traffic patterns across millions of requests.
- **Distributed Queries:** Querying data across multiple nodes.

## 💡 Why ClickHouse?
When Elasticsearch becomes too expensive or slow for your logs, ClickHouse is the answer.
