Purpose & Usage Context:  

This API server provides functionality for storing and retrieving data from the front end.  
Designed as a microservice, it can be scaled and deployed independently, minimizing any impact on the front end.  
By developing with Docker and pushing the image to Docker Hub, any team member can verify the application in the same environment.

Environment:
- Host OS: Windows 11 Home 24H2  
- Visual Studio Code  
- Docker Desktop for Windows  
- Docker Image: Python:3.13-slim linux/amd64  
- Docker: version 28.3.2  
- Python 3.9.16  
- Django 5.2.5, Django REST Framework 3.16.1, Django-filter 25.1  
- json-log-formatter 1.1.1, coverage 7.10.6  
**Django REST Framework** was chosen based on existing experience with **Django**, enabling quicker development and easier long-term maintenance compared to adopting a new framework like **FastAPI**.
- SQLite, sqlparse 0.5.3  
**SQLite** was selected because it is Django’s default RDBMS and easy to set up. More advanced RDBMSs such as **MySQL** or **PostgreSQL** were considered unnecessary due to the limited scale of the data handled in this project.
- AWS Copilot CLI v1.34.1

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
  
AWS:  
- This architecture was built using **AWS Copilot CLI**
- Compute: ECS(Fargate)  
**Fargate** was selected with future scalability in mind
- Container Management: ECR
- Networking: ALB(Application Load Balancer), VPC  
**ALB** was adopted for load balancing. Due to constraints of the **Copilot CLI**, detailed **VPC** configurations rely on the default settings
- Monitoring & Logging: CloudWatch Logs, Alarm
- IaC: CloudFormation  
Revise **CloudFormation Templates** created by **Copilot** and re-deploy them. Manage **infrastructure as code** 
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
