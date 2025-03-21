from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, MinMaxScaler
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator

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

# Stop Spark Session
spark.stop()

