Purpose & Usage Context:  

This API server provides functionality for storing and retrieving data from the front end.  
Designed as a microservice, it can be scaled and deployed independently, minimizing any impact on the front end.  
The infrastructure — including ECS/Fargate, RDS, and the ALB — is provisioned first using Terraform. After that, GitHub Actions handles deploying the Django API server onto the AWS environment.  
Early on, Copilot was used to quickly launch ECS/Fargate, and the generated CloudFormation was applied experimentally. Working through the resulting issues helped build a deeper understanding of AWS resource configurations.

Environment:
- Host OS: Windows 11 Home 25H2  
- Visual Studio Code 1.108.2  
- Python 3.13.7  
- Django 5.2.5, Django REST Framework 3.16.1, Django-filter 25.1  
- json-log-formatter 1.1.1, coverage 7.10.6  
**Django REST Framework** was chosen based on existing experience with **Django**, enabling quicker development and easier long-term maintenance compared to adopting a new framework like **FastAPI**.
- Web Server: WSGI with Gunicorn  
This application provides only REST APIs and does not require WebSocket support or asynchronous processing. To keep the architecture simple and efficient, **WSGI with Gunicorn** was chosen instead of an **ASGI**-based setup.
- Database: PostgreSQL(deploy), SQLite(tests)  
- Utilities: sqlparse 0.5.3  
The project initially used **SQLite**. However, when considering horizontal scaling on ECS, it became clear that write operations from multiple containers would trigger database locks, which is a critical limitation for a scalable architecture. To avoid this issue, the database was migrated to **Amazon RDS**.
**PostgreSQL** was chosen because Django provides first class support and optimizations for it by default.
- GitHub Actions currently authenticates to AWS using IAM user access keys. Migrating to **OIDC**‑based authentication is planned as a future improvement.  
- AWS CLI 2.30.6

API server Functions:
- records and stores product names(product) and prices(price)
- No authentication
- Searchable by product name
- No pagination

Logging:
- All HTTP request and response logs are captured in myapi/middleware.py.
- Log format: JSON
- Output destination:
  - Console
  - logs/api_server.log
- LogLevel:
  - Django: INFO
  - myapi.middleware: DEBUG

<br>
Unit Test: 
https://github.com/HideTake761/CI-CD-Django-REST-API-with-Docker-on-AWS-ECS-Fargate/blob/main/myapi/tests.py
<br>
<br>
<br>
  
Starting the Django application on AWS ECS with RDS  
1. Install the Session Manager Plugin on your local machine. (AWS Systems Manager Session Manager is required to connect to the ECS container.)
2. Run the following command to execute the migration inside the ECS container.  
  
  
>aws ecs execute-command --cluster (cluster name) --task (task name) --container (container name) --interactive --command "python manage.py migrate"  

<br>  
  
AWS:  
- This architecture was built using [**Terraform**](https://github.com/HideTake761/Terraform/tree/main/AWS_ECS_RDS)
- Compute: ECS(Fargate)  
**Fargate** was selected with future scalability in mind
- Container Management: ECR
- Database: RDS PostgreSQL
- Networking: ALB(Application Load Balancer), VPC, VPC Endpoint  
**VPC Endpoints** were chosen instead of a NAT Gateway to avoid unnecessary internet traffic.
- Monitoring & Logging: CloudWatch Logs, Alarm
- IaC: Terraform
- Cost Management: AWS Budgets
- System Architecture Diagram is below  
  <img src="./AWS ECS RDS.jpg" alt="System Architecture Diagram" width="600" />

**AWS infrastructure** is managed in a separate **Terraform** repository:
[Terraform/AWS_ECS_RDS](https://github.com/HideTake761/Terraform/tree/main/AWS_ECS_RDS)
  
<br>  
  
CI/CD Pipeline (via GitHub Actions):  
  
**GitHub Actions** was selected due to deep integration with the GitHub ecosystem. It can be configured through the GitHub UI and a YAML file which makes it much simpler to implement than alternatives like **Jenkins** or **CircleCI**.
- Trigger: Push, pull request & merge to the main branch
- CI: Runs unit tests automatically
- CD: If tests pass, it builds a Docker image and then deploys it to AWS ECS (Fargate)  
- For more details, please refer to the below.<br>
https://github.com/HideTake761/CI-CD-Django-REST-API-with-Docker-on-AWS-ECS-Fargate/blob/main/.github/workflows/docker-build.yaml 








