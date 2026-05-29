# 🌩️ SERVERLESS SRE: AWS LAMBDA MASTER STUDY GUIDE

Serverless shifts the focus from managing servers to **Event-Driven Architectures**. For an SRE, the challenges are **Cold Starts, Timeouts, and Async Monitoring**.

---

## 1. What is Serverless (Lambda)?
Compute without managing instances. You provide code; AWS handles scaling and availability.

## 2. Core Concepts
- **Events**: Triggers (S3 upload, API Gateway request, SNS message).
- **Runtime**: Python, Node.js, Go, etc.
- **Concurrency**: How many instances of your function run at once.
- **Cold Start**: The delay when a function is triggered after being idle.

## 3. SRE Cost & Performance Tuning
- **Memory vs CPU**: Lambda scales CPU proportionally to Memory. Sometimes increasing memory makes the code run faster and **saves money**.
- **Provisioned Concurrency**: Keeps functions "warm" to eliminate cold starts.
- **Reserved Concurrency**: Guarantees capacity and acts as a "Throttle" to prevent one function from consuming all account resources.

## 4. Monitoring & Observability
- **CloudWatch Metrics**: Duration, Errors, Throttles, ConcurrentExecutions.
- **CloudWatch Logs**: Centralized logging for every execution.
- **AWS X-Ray**: Distributed tracing to see where Lambda is spending time.

## 5. Deployment with IaC
Never use the Console. Use **Serverless Framework, SAM, or Terraform**.
```hcl
resource "aws_lambda_function" "my_func" {
  filename      = "function.zip"
  function_name = "sre_automation"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.handler"
  runtime       = "python3.9"
}
```

---

## 🏠 How to test Serverless on Localhost?
Use **LocalStack** to run Lambda functions locally.

1.  **Start LocalStack**:
    ```bash
    localstack start
    ```
2.  **Create Function**:
    ```bash
    awslocal lambda create-function --function-name test --runtime python3.9 ...
    ```
3.  **Invoke**:
    ```bash
    awslocal lambda invoke --function-name test output.txt
    ```
