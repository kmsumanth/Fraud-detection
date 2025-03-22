Sentinel - AI-Powered Fraud Detection in Financial Transactions
Overview
Sentinel is an AI-driven fraud detection system designed to process real-time financial transactions and identify fraudulent activities. It leverages Kafka for streaming, Databricks (Spark Streaming) for machine learning-based fraud detection, and integrates MongoDB, Snowflake, and Azure Data Factory for data storage and orchestration. The project also includes CI/CD automation using GitHub Actions for seamless deployment and monitoring.

Key Components
Kafka – Handles real-time transaction streaming.

Databricks (Spark Streaming) – Processes transactions and applies machine learning models for fraud detection.

MongoDB – Stores real-time transaction logs for immediate analysis.

Snowflake – Maintains historical transaction data for advanced analytics.

Azure Data Factory – Orchestrates batch processing and data pipelines.

FastAPI – Facilitates API communication and alerting.

GitHub Actions – Implements CI/CD for automated deployment, testing, and monitoring.

Workflow
Kafka continuously streams real-time transaction data from various financial systems.

Databricks processes incoming transactions, applying fraud detection models to identify suspicious activity.

Flagged transactions trigger alerts for further investigation.

MongoDB stores real-time logs for immediate analysis, while Snowflake retains historical transaction data for deeper insights.

Azure Data Factory orchestrates batch jobs for retraining fraud detection models and performing long-term trend analysis.

GitHub Actions automates testing, deployment, and monitoring of the entire pipeline.

CI/CD Implementation
The project integrates GitHub Actions to ensure automated deployment, continuous testing, and efficient monitoring. The pipeline includes:

Automated testing for fraud detection models and APIs.

Docker-based containerization for efficient deployment.

Seamless integration with cloud infrastructure.

