# 🏗️ Terraform Mastery: The SRE's Blueprint

Infrastructure as Code (IaC) is the only way to scale cloud infrastructure reliably. Terraform is the industry standard for cloud-agnostic IaC.

## 1. Core Workflow
- **Write**: Define resources in `.tf` files (HCL syntax).
- **Plan**: `terraform plan` - See what will change before it happens.
- **Apply**: `terraform apply` - Create/Update the infrastructure.

## 2. The State File (`terraform.tfstate`)
This is the single source of truth. It maps your code to real-world resources.
- **SRE Warning**: Never delete or edit this file manually.
- **Remote State**: Always store this in **S3 with DynamoDB Locking** for team collaboration.

## 3. Modules (The Dry Principle)
Don't repeat yourself. Use Modules to package common infrastructure (e.g., a "Standard VPC" or "Production EKS").
```hcl
module "my_vpc" {
  source = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}
```

## 4. Variables & Locals
- **Variables**: Inputs for your modules (Environment name, region).
- **Outputs**: Data you want to see or pass to other modules (VPC ID, LB DNS).
- **Locals**: Internal temporary values to simplify logic.

## 5. SRE Best Practices
1.  **State Locking**: Use DynamoDB to prevent two people from applying changes at the same time.
2.  **Version Pinning**: Always pin your provider and module versions to avoid breaking changes.
3.  **Workspaces vs. Folders**: Use different folders for `dev/stage/prod` to keep environments isolated.

---

## 🏠 How to test Terraform on Localhost?
Use **LocalStack** to apply Terraform code without an AWS account.

1.  **Provider Override**:
    ```hcl
    provider "aws" {
      access_key = "test"
      secret_key = "test"
      region     = "us-east-1"
      endpoints {
        ec2 = "http://localhost:4566"
        s3  = "http://localhost:4566"
      }
    }
    ```
2.  **Simulation**: Run `terraform apply` against LocalStack and verify the resources with `awslocal`.
