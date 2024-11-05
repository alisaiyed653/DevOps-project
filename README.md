# DevOps-project
Project to deploy a Dockerized Flask web application on AWS using Terraform, ECS, and Jenkins. This setup showcases Infrastructure as Code (IaC) with Terraform, containerization with Docker, and CI/CD automation using AWS-native tools for a scalable cloud environment.
---

## Project Summary
- **Application**: Flask web app
- **DevOps Tools**: Docker (for containerization), Terraform (for infrastructure as code), Git (for version control), ECS (Elastic Container Service for running and managing the docker containers on AWS, CodePipeline (for Management of continuous integration and deployment (CI/CD), automating the build, test, and deployment processes.

---

## Project Steps

### 1. Setting Up the Flask Application
   - **Files**: `server.py` (Flask app), `requirements.txt`
   - **Challenge**: Initial setup lacked `requirements.txt`, so dependencies were missing for Docker.
   - **Solution**: Created a virtual environment, installed Flask, and generated `requirements.txt` using:
     ```
     pip freeze > requirements.txt
     ```
---
### 2. Dockerizing the Flask Application
   - **File**: `Dockerfile`
   - **Dockerfile Structure**:
     - **Base Image**: Used Python 3.8
     - **Working Directory**: Set as `/app`
     - **Copy Project Files**: Added `COPY . .` to include all project files
     - **Dependencies**: Installed with `RUN pip install -r requirements.txt`
     - **Run Command**: Configured `CMD ["python", "server.py"]` to launch Flask
   - **Challenge**: Initially, the container wouldn’t serve the app on the host machine.
     - **Solution**: Updated `server.py` with `app.run(host='0.0.0.0')`, allowing the app to listen on all network interfaces within the container.
   - **Build Command**:
     ```
     docker build -t flask-web-app .
     ```
---
### 3. Testing the Dockerized Application Locally
   - **Run Command**:
     ```
     docker run -p 80:5000 flask-web-app
     ```
   - **Testing**: Verified by accessing `http://localhost`.
   - **Challenge**: Initially, I mapped `-p 80:80`, but Flask defaults to port 5000.
     - **Solution**: Corrected the command to `-p 80:5000`.

---
### 4. Deploying to AWS with ECS and ECR

   - **Setting Up AWS Infrastructure with Terraform**:
     - **VPC and Subnets**: Created a VPC with a CIDR block for secure networking. Defined two public subnets across availability zones (`eu-west-2a` and `eu-west-2b`) to ensure high availability.
     - **Internet Gateway and Route Table**: Configured an Internet Gateway for external access, added a route table, and associated it with subnets for internet routing.
     - **Security Groups**: Set up security group rules to allow inbound HTTP traffic on port 80 from any IP, ensuring the Flask app is accessible from the public internet.

   - **Pushing Docker Image to ECR**:
     - **Image Tagging and Push**: Tagged the Docker image with the ECR repository URI and pushed it to ECR.
     - **Challenges**: Encountered `400 Bad Request` errors due to tag immutability and missing execution role requirements.
     - **Solution**: Rebuilt the image, updated ECR settings, and created an execution role with permissions for ECS tasks to pull images from ECR.
---

### 5. Detailed Terraform Configuration and ECS Setup

   - **Terraform Configurations**:
     - **`main.tf` Adjustments**: Added configurations for VPC, subnets, security groups, Internet Gateway, and ECS cluster setup.
     - **IAM Role for ECS**: Defined an IAM role (`AmazonECSTaskExecutionRole`) with permissions for ECS to pull images from ECR, resolving permission-related issues during deployment.
     - **ECS Task and Service**: Configured an ECS task with `awsvpc` networking, using Fargate, and linked it to the security group with port 80 open. Set up an ECS service to manage and scale tasks, and enabled load balancing.

   - **Challenges and Solutions**:
     - **Execution Role**: Defined and attached an IAM role in Terraform, granting ECS tasks access to ECR images by applying the `AmazonECSTaskExecutionRolePolicy`.
     - **Security Group Misconfiguration**: Fixed missing inbound rules to allow HTTP traffic. Adjusted Terraform code to ensure the security group was configured for HTTP access and verified the application’s availability.

---
### 6. Integrating Jenkins for CI/CD

   - **Jenkins Installation (UPDATED)**:
      - Previously I was laucnhing an instance on the AWS console and manually configuring and installing the dependencies as well as configuring it to run on port 8080. As I am using AWS as an individual I do not want to rack up bills and keep these instances active          continuously. As a result I added this to my terraform script and automated this process so now my updated main.tf file contains this procedure. 
      - Verified installation by accessing Jenkins via the public IP address.
         
   - **Configuring Jenkins**:
      - GitHub Integration:
         - Set up GitHub credentials in Jenkins under "Manage Jenkins" → "Manage Credentials."
         - Added GitHub repository URL in the Jenkins pipeline configuration.
         
      - AWS Integration**:
         - Set up Access ID and secret access key credentials to allow jenkins to connect to AWS.
         
      - Docker Plugin:
         - Installed the Docker Pipeline plugin to facilitate Docker operations within Jenkins jobs.
         
   - **Pipeline Creation**:
     
        - Created a Jenkins pipeline for the project, defining stages for:
        - Checkout: Pulling the latest code from the GitHub repository.
        - Build Docker Image: Building the Docker image using the Dockerfile located in the repository.
        - Login to ECR: Authenticating to the AWS ECR to allow image pushes.
        - Push to ECR: Pushing the built image to the ECR repository.

     **Pipeline Script**:

   ```
      groovy
      pipeline {
          agent any
          environment {
              ECR_REGISTRY = '255625225972.dkr.ecr.eu-west-2.amazonaws.com'
              ECR_REPOSITORY = 'flask-web-app'
              IMAGE_TAG = "latest"
          }
          stages {
              stage('Checkout') {
                  steps {
                      git credentialsId: 'aws_credentials', url: 'https://github.com/alisaiyed653/DevOps-project.git'
                  }
              }
              stage('Build Docker Image') {
                  steps {
                      script {
                          docker.build("${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}")
                      }
                  }
              }
              stage('Login to ECR') {
                  steps {
                      script {
                          sh "aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                      }
                  }
              }
              stage('Push to ECR') {
                  steps {
                      script {
                          docker.image("${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}").push()
                      }
                  }
              }
          }
      }
```

   - **Building and Testing**:
      - After configuring the pipeline, triggered a build in Jenkins to ensure all stages executed correctly.
      - Observed build logs to troubleshoot issues related to Docker permissions and ECR login failures, adjusting configurations as needed.

   - **Challenges Faced**:

      - Disk Space Issues: Encountered low disk space errors during pipeline execution.
      - Permission Denied Errors: Faced issues related to Docker daemon permissions, which were resolved by adding the Jenkins user to the Docker group.
      - Git Credential Issues: Initially faced challenges accessing the GitHub repository, resolved by correctly setting up credentials in Jenkins.
