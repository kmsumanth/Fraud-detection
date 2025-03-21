from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.pipeline import PipelineModel

# Initialize Spark Session
spark = SparkSession.builder.appName("FraudDetectionModel").getOrCreate()

# Load Dataset
df = spark.read.csv("fraud_detection_dataset.csv", header=True, inferSchema=True)

# Handling Categorical Features
categorical_cols = ["transaction_location", "device_type", "merchant_category", "transaction_channel", "user_location"]
indexers = [StringIndexer(inputCol=col, outputCol=col + "_index") for col in categorical_cols]
encoders = [OneHotEncoder(inputCol=col + "_index", outputCol=col + "_encoded") for col in categorical_cols]

# Feature Selection
numeric_cols = ["transaction_amount", "previous_transactions", "failed_transactions", "account_age_days",
                "user_credit_score", "is_foreign_transaction", "is_high_risk_country", "is_vpn_used",
                "user_income", "is_account_compromised"]

# Vector Assembler
assembler = VectorAssembler(inputCols=numeric_cols + [col + "_encoded" for col in categorical_cols], outputCol="features_raw")

# Standardization
scaler = StandardScaler(inputCol="features_raw", outputCol="features_scaled")

# Normalization
normalizer = MinMaxScaler(inputCol="features_scaled", outputCol="features")

# Model Selection
gbt = GBTClassifier(labelCol="is_fraud", featuresCol="features", maxIter=50)

# Pipeline
pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler, normalizer, gbt])

# Train-Test Split
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

# Train Model
model = pipeline.fit(train_df)

# Predictions
predictions = model.transform(test_df)

# Evaluation
evaluator = BinaryClassificationEvaluator(labelCol="is_fraud", metricName="areaUnderROC")
roc_auc = evaluator.evaluate(predictions)
print(f"Model AUC: {roc_auc}")

# Save Model
model.save("fraud_detection_model")

# Load Model for Prediction
loaded_model = PipelineModel.load("fraud_detection_model")

# Perform Prediction on New Data
new_data = spark.createDataFrame([
    (12345, 2500.75, "NY", 150, 1430, "mobile", 20, 2, 500, 720, 0, 0, 0, "electronics", "online", 75000.00, 0, "NY")
], ["user_id", "transaction_amount", "transaction_location", "merchant_id", "transaction_time", "device_type", "previous_transactions", "failed_transactions", "account_age_days", "user_credit_score", "is_foreign_transaction", "is_high_risk_country", "is_vpn_used", "merchant_category", "transaction_channel", "user_income", "is_account_compromised", "user_location"])

prediction_result = loaded_model.transform(new_data)
prediction_result.select("user_id", "prediction").show()

# Stop Spark Session
spark.stop()

