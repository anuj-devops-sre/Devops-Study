# 🐍 PYTHON FOR SRE: AUTOMATION TOOLBOX

Bash is for scripts; Python is for **Automation Systems**. For a Mid-level SRE, you must know how to use **Boto3** for AWS automation.

---

## 1. Why Python for SRE?
- **Readability**: Easier to maintain complex logic than Bash.
- **Library Support**: Huge ecosystem for Cloud (Boto3), K8s (Kubernetes Python Client), and APIs.
- **Error Handling**: Proper try-except blocks for production scripts.

## 2. Boto3 (The AWS Power Tool)
The official SDK for AWS.
```python
import boto3

# Example: List all unencrypted S3 buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}")
```

## 3. Common SRE Automation Tasks
- **Snapshot Cleanup**: Delete EBS snapshots older than 30 days.
- **Instance Scheduler**: Stop Dev instances at 6 PM and start at 9 AM to save cost.
- **Unused EBS Finder**: Identify and delete volumes that are not attached to any EC2.
- **K8s Health Monitor**: Script that checks for `CrashLoopBackOff` pods and sends a Slack alert.

## 4. Building CLI Tools
Use **Click** or **Argparse** to build professional CLI tools for your team.
```python
import click

@click.command()
@click.option('--region', default='us-east-1', help='AWS Region')
def list_instances(region):
    ec2 = boto3.resource('ec2', region_name=region)
    for instance in ec2.instances.all():
        print(f"{instance.id} is {instance.state['Name']}")

if __name__ == '__main__':
    list_instances()
```

## 5. SRE Best Practices
- **Use Virtualenvs**: Always isolate your script dependencies.
- **Logging**: Use the `logging` module, never just `print()`.
- **Unit Testing**: Test your automation logic with **Moto** (mocking Boto3).

---

## 🏠 Local Practice
```bash
# Install Boto3 and Moto
pip install boto3 moto

# Run a script against LocalStack
export AWS_ENDPOINT_URL=http://localhost:4566
python my_script.py
```
