# DevOps-project
Project to deploy a Dockerized Flask web application on AWS using Terraform, ECS, and CodePipeline. This setup showcases Infrastructure as Code (IaC) with Terraform, containerization with Docker, and CI/CD automation using AWS-native tools for a scalable cloud environment.
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

### 3. Testing the Dockerized Application Locally
   - **Run Command**:
     ```
     docker run -p 80:5000 flask-web-app
     ```
   - **Testing**: Verified by accessing `http://localhost`.
   - **Challenge**: Initially, I mapped `-p 80:80`, but Flask defaults to port 5000.
     - **Solution**: Corrected the command to `-p 80:5000`.

---


