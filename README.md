Purpose & Usage Context:  

This API server provides functionality for storing and retrieving data from the front end.  
Designed as a microservice, it can be scaled and deployed independently, minimizing any impact on the front end.  
By developing with Docker and pushing the image to Docker Hub, any team member can verify the application in the same environment.

Environment:
- Host OS: Windows 11 Home 25H2  
- Visual Studio Code 1.108.2  
- Python 3.13.7  
- Django 5.2.5, Django REST Framework 3.16.1, Django-filter 25.1  
- json-log-formatter 1.1.1, coverage 7.10.6  
**Django REST Framework** was chosen based on existing experience with **Django**, enabling quicker development and easier long-term maintenance compared to adopting a new framework like **FastAPI**.
- Web Server: WSGI + Gunicorn  
今回は
- Database: PostgreSQL(deploy), SQLite(tests)  
- Utilities: sqlparse 0.5.3  
**PostgreSQL** were considered
- OIDC  
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
  
動作確認  
  
  
>aws ecs execute-command --cluster < cluster name> --task <task name> --container <container name> --interactive --command "python manage.py migrate"  

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


