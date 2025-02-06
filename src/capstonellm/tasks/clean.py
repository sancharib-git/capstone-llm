import argparse
import logging
from pyspark.sql import SparkSession
from capstonellm.common.catalog import llm_bucket
from capstonellm.common.spark import ClosableSparkSession
import os
import json

logger = logging.getLogger(__name__)

def clean(spark: SparkSession, environment: str, tag: str):
    # write answer here
    output_dir = f"cleaned/{tag}/"
    # read the json file from s3
    df = spark.read.json("questions.json")
    items = df.collect()
    for index, item in enumerate(items):
        item_dict = item.asDict()  # Convert Row to dictionary
        output_file = os.path.join(output_dir, f"item_{index + 1}.json")
    
        # Write each item to a separate file
        with open(output_file, 'x') as f:
            json.dump(item_dict, f)

def main():
    parser = argparse.ArgumentParser(description="capstone_llm")
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=False, default="local"
    )
    parser.add_argument(
        "-t", "--tag", dest="tag", help="the tag to process",
        default="python-polars", required=False
    )
    logger.info("starting the cleaning job")

    args = parser.parse_args()
    common_spark_config = {
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    }
    if args.env == "local":
        print("This is a local execution of the capestonellm project")
        session = (
            SparkSession.builder.appName("Spark S3 Integration")
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4")
            .getOrCreate()
        )
        clean(session, args.env, args.tag)
    else:
        with ClosableSparkSession("capstone_llm", spark_config=common_spark_config) as session:
            clean(session, args.env, args.tag)


if __name__ == "__main__":
    main()
