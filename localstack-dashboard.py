#!/usr/bin/env python3
"""
Simple LocalStack Web Dashboard
Access at: http://localhost:5000
"""

from flask import Flask, render_template_string
import boto3
import os

app = Flask(__name__)

# Configure AWS credentials and endpoint
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

LOCALSTACK_URL = 'http://localhost:4566'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LocalStack Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { margin-bottom: 30px; border-bottom: 1px solid #30363d; padding-bottom: 20px; }
        h1 { color: #58a6ff; }
        .service { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        .service h2 { color: #79c0ff; margin-bottom: 15px; font-size: 18px; }
        .items { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .item { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 15px; }
        .item-name { color: #79c0ff; font-weight: bold; margin-bottom: 5px; word-break: break-all; }
        .item-meta { color: #8b949e; font-size: 12px; }
        .empty { color: #6e7681; font-style: italic; padding: 20px; text-align: center; }
        .error { color: #f85149; }
        .status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; background: #238636; color: white; }
        button { background: #238636; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
        button:hover { background: #2ea043; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 LocalStack Dashboard</h1>
            <p>Endpoint: {{ endpoint }} | Region: {{ region }}</p>
        </header>

        <div class="service">
            <h2>📦 S3 Buckets</h2>
            {% if s3_buckets %}
                <div class="items">
                    {% for bucket in s3_buckets %}
                        <div class="item">
                            <div class="item-name">🪣 {{ bucket['Name'] }}</div>
                            <div class="item-meta">Created: {{ bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S') }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty">No S3 buckets found</div>
            {% endif %}
        </div>

        <div class="service">
            <h2>⚡ DynamoDB Tables</h2>
            {% if dynamodb_tables %}
                <div class="items">
                    {% for table in dynamodb_tables %}
                        <div class="item">
                            <div class="item-name">📊 {{ table['TableName'] }}</div>
                            <div class="item-meta">Status: <span class="status">{{ table['TableStatus'] }}</span></div>
                            <div class="item-meta">Items: {{ table.get('ItemCount', 0) }} | Size: {{ table.get('TableSizeBytes', 0) }} bytes</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty">No DynamoDB tables found</div>
            {% endif %}
        </div>

        <div class="service">
            <h2>📬 SQS Queues</h2>
            {% if sqs_queues %}
                <div class="items">
                    {% for queue in sqs_queues %}
                        <div class="item">
                            <div class="item-name">📨 {{ queue.split('/')[-1] }}</div>
                            <div class="item-meta">{{ queue }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty">No SQS queues found</div>
            {% endif %}
        </div>

        <div class="service">
            <h2>📢 SNS Topics</h2>
            {% if sns_topics %}
                <div class="items">
                    {% for topic in sns_topics %}
                        <div class="item">
                            <div class="item-name">🔔 {{ topic['TopicArn'].split(':')[-1] }}</div>
                            <div class="item-meta">{{ topic['TopicArn'] }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty">No SNS topics found</div>
            {% endif %}
        </div>

        <div class="service">
            <h2>🐍 Lambda Functions</h2>
            {% if lambda_functions %}
                <div class="items">
                    {% for func in lambda_functions %}
                        <div class="item">
                            <div class="item-name">⚙️ {{ func['FunctionName'] }}</div>
                            <div class="item-meta">Runtime: {{ func.get('Runtime', 'N/A') }}</div>
                            <div class="item-meta">Modified: {{ func.get('LastModified', 'N/A') }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty">No Lambda functions found</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    try:
        # S3
        s3 = boto3.client('s3', endpoint_url=LOCALSTACK_URL)
        s3_buckets = s3.list_buckets().get('Buckets', [])
    except Exception as e:
        s3_buckets = []
        print(f"S3 Error: {e}")

    try:
        # DynamoDB
        dynamodb = boto3.client('dynamodb', endpoint_url=LOCALSTACK_URL)
        tables = dynamodb.list_tables().get('TableNames', [])
        dynamodb_tables = []
        for table in tables:
            table_info = dynamodb.describe_table(TableName=table)['Table']
            dynamodb_tables.append(table_info)
    except Exception as e:
        dynamodb_tables = []
        print(f"DynamoDB Error: {e}")

    try:
        # SQS
        sqs = boto3.client('sqs', endpoint_url=LOCALSTACK_URL)
        sqs_queues = sqs.list_queues().get('QueueUrls', [])
    except Exception as e:
        sqs_queues = []
        print(f"SQS Error: {e}")

    try:
        # SNS
        sns = boto3.client('sns', endpoint_url=LOCALSTACK_URL)
        sns_topics = sns.list_topics().get('Topics', [])
    except Exception as e:
        sns_topics = []
        print(f"SNS Error: {e}")

    try:
        # Lambda
        lam = boto3.client('lambda', endpoint_url=LOCALSTACK_URL)
        lambda_functions = lam.list_functions().get('Functions', [])
    except Exception as e:
        lambda_functions = []
        print(f"Lambda Error: {e}")

    return render_template_string(
        HTML_TEMPLATE,
        endpoint=LOCALSTACK_URL,
        region='us-east-1',
        ec2_instances=ec2_instances,
        s3_buckets=s3_buckets,
        dynamodb_tables=dynamodb_tables,
        sqs_queues=sqs_queues,
        sns_topics=sns_topics,
        lambda_functions=lambda_functions
    )

if __name__ == '__main__':
    print("🚀 Starting LocalStack Dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
bles().get('TableNames', [])
        dynamodb_tables = []
        for table in tables:
            table_info = dynamodb.describe_table(TableName=table)['Table']
            dynamodb_tables.append(table_info)
    except Exception as e:
        dynamodb_tables = []
        print(f"DynamoDB Error: {e}")

    try:
        # SQS
        sqs = boto3.client('sqs', endpoint_url=LOCALSTACK_URL)
        sqs_queues = sqs.list_queues().get('QueueUrls', [])
    except Exception as e:
        sqs_queues = []
        print(f"SQS Error: {e}")

    try:
        # SNS
        sns = boto3.client('sns', endpoint_url=LOCALSTACK_URL)
        sns_topics = sns.list_topics().get('Topics', [])
    except Exception as e:
        sns_topics = []
        print(f"SNS Error: {e}")

    try:
        # Lambda
        lam = boto3.client('lambda', endpoint_url=LOCALSTACK_URL)
        lambda_functions = lam.list_functions().get('Functions', [])
    except Exception as e:
        lambda_functions = []
        print(f"Lambda Error: {e}")

    return render_template_string(
        HTML_TEMPLATE,
        endpoint=LOCALSTACK_URL,
        region='us-east-1',
        s3_buckets=s3_buckets,
        dynamodb_tables=dynamodb_tables,
        sqs_queues=sqs_queues,
        sns_topics=sns_topics,
        lambda_functions=lambda_functions
    )

if __name__ == '__main__':
    print("🚀 Starting LocalStack Dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
