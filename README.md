# Deploying Flight Reservation API For Local

- Prerequisites
1. Install `docker` and `docker-compose`

### Starting PostgreSQL
- `docker-compose -f docker-compose-postgres.yml up -d`

### Required Environment Variables
- **POSTGRES_USER:** Username that API may use to connect to Postgres
- **POSTGRES_DB:** Database that API migrates the changes and serve users
- **POSTGRES_PORT:** Port at which the Postgres is running
- **POSTGRES_PASSWORD:** Password that API may use to connect to Postgres
- **POSTGRES_HOST:** Host (URL) that API may use to connect to Postgres, e.g. 'localhost' or 'db.traveloair.com' or '10.20.0.0'


### Starting API
- Configurable variables should be isolated to .env
- Start with:
`docker build -t traveloair_flight_reservation_api:latest -f Dockerfile .`

`docker-compose -f docker-compose.yml up -d`
- Optional: include `-d` flag at end of docker-compose statement to run in background


# Deploying Flight Reservation API For Remote (AWS EC2-ECR-RDS)

Create Postegres Database using RDS

1. Login to your AWS account
2. Search RDS
3. Choose second option create Databases
4. On right click on create Database
5. Choose a database creation method: Standard-Create
6. Engine options: Postgres
7. Templates: Free tier
8. Settings -> give the DB instance identifier name / master username and Paasword(copy username and passwrod later you will not able to see it)
9. Connectivity -> Piblic Access -> always select Yes
PostgreSQL version lower than version 13
10. VPC security Group create New
11. Additional Configuration: give the Database name
12. Create Database
----------------------------------------------------------------
After that go to the Databases -> click on newly created db instance then check the tab Connectivity & security
Endpoint is your Your Host name something like: traveloairdb.xxxxxxxx.us-xxx-x.rds.amazonaws.com


Now Set postgres database connection's Environment variable and### Required Environment Variables in .env file

- **POSTGRES_USER:** RDS Username that API may use to connect to Postgres
- **POSTGRES_DB:** RDS Database that API migrates the changes and serve users
- **POSTGRES_PORT:** RDS Port at which the Postgres is running
- **POSTGRES_PASSWORD:** RDS Password that API may use to connect to Postgres
- **POSTGRES_HOST:** RDS Host (URL) that API may use to connect to Postgres

# steps for loading the data to the RDS posgres
- Start with:
`docker build -t traveloair_flight_reservation_api:latest -f Dockerfile .`

`docker-compose -f docker-compose.yml up -d`
- Optional: include `-d` flag at end of docker-compose statement to run in background

to check the data loaded into the db or not open pgadmin add new server and add the RDS detail into it and check for the data


# Steps for working with Elastic Container Registry(ECR) for connecting it to Docker

This is so that specified users or Amazon EC2 instances can access your container repositories and images. You can use your preferred CLI to push, pull, and manage Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts.

1. Search ECR and find it and click on it.
2. Create repository
3. Select visibility setting private
4. Give repository Name
5. Keep default setting of other thing now click on create
6. Now click on View push command to run the command on mac
7. Make sure that you have the latest version of the AWS CLI and Docker installed. For more information
8. If you don't have Download Docker and for CLI run below CLI Commands
9. curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
10. curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
11. sudo installer -pkg ./AWSCLIV2.pkg -target /
12. To verify that the shell can find and run the aws command in your $PATH, use the following commands. 
 - which aws
 - aws --version
13. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 248009137196.dkr.ecr.us-east-1.amazonaws.com

14. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:
docker build -t r_test .

15. After the build completes, tag your image so you can push the image to this repository:
docker tag r_test:latest 248009137196.dkr.ecr.us-east-1.amazonaws.com/r_test:latest

16. Run the following command to push this image to your newly created AWS repository:
docker push 248009137196.dkr.ecr.us-east-1.amazonaws.com/r_test:latest

17. Image pushed and now copy Image URI

18. Amazon ECS -> Clusters -> Create Cluster -> EC2 Linux + Networking 
19. Click on next step -> Give Cluster Name -> EC2 instance Type: T2.micro
20. Number of instaces : 1
21. Create key for selection here
22. Select VPC
23. Select Subnet
24. Select Default Security Group
25. Click on Create
26. Search ECS 
27. Click on Task Definitions -> Create new task Definition -> Select ECS
28. Give task definition name
29. Task role -> None, Network mode -> <default>
30. Task memory 100
31. Task CPU: 1 Vcpu
32. click on add container container name -> paste copied image URI -> give the host port and container port 8800:5000
33. give the postgres host, db , username, password
34. click on add and now click on Create
35. Go to the Cluster on your left panel: click on blue color cluster name link
36. Click on Task tab -> Click on Run new Task -> Select Launch type: EC2 -> keep default setting -> Run Task -> wait for running status
37. search EC2->security groups-> edit inbound rules -> add two new rules -> 
select type Custom TCP, port range: 8800, source: custom select 0.0.0.0/0 
select type Custom TCP, port range: 8800, source: custom select ::/0
38. search for EC2 instance -> click on running instance -> go for copying IPv4  which is your URL for running the project on your browser xx-xx-xx-xx.comput-1.amazonaws.com:8800/
39. Finish  
  
  
  








