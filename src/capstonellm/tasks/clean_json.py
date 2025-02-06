import boto3
import json
import pdb
import polars as pl

from capstonellm.common import catalog

# read the file from s3
s3 = boto3.client('s3')
path_to_sql_questions = "input/sql/questions.json"
path_to_sql_answers = "input/sql/answers.json"
path_to_cleaned = "test/cleaned/sql"
questions = s3.get_object(Bucket=catalog.llm_bucket, Key=path_to_sql_questions)
answers = s3.get_object(Bucket=catalog.llm_bucket, Key=path_to_sql_answers)
json_file_path = "s3://dataminded-academy-capstone-llm-data-us/input/dbt/questions.json"
json_data_questions = json.loads(questions['Body'].read().decode('utf-8'))
json_data_answers = json.loads(answers['Body'].read().decode('utf-8'))
#cleaned/<user>/{tag}


# for each question id in the json data, store it in a file
for item in json_data_questions['items']: # item is a dictionary representing the question
    question_id = item['question_id']
    question_string = json.dumps(item)
    s3.put_object(Bucket=catalog.llm_bucket, Key=f"{path_to_cleaned}/{question_id}.json", Body=question_string)

# for item in json_data_answers['items']: # item is a dictionary representing the answer
    question_id = item['question_id']
    answer_string = json.dumps(item)
    existing_file = s3.get_object(Bucket=catalog.llm_bucket, Key=f"{path_to_cleaned}/{question_id}.json")
    existing_json_data = json.loads(existing_file['Body'].read().decode('utf-8'))
    existing_json_string = json.dumps(existing_json_data)
    # Step 2: Append the new JSON data to the existing data
    updated_json_string = existing_json_string + '\n' + answer_string
    # Step 3: Upload the updated JSON content back to S3
    s3.put_object(Bucket=catalog.llm_bucket, Key=f"{path_to_cleaned}/{question_id}.json", Body=updated_json_string)
