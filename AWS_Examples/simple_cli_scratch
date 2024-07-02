
## AWS EC2, Load Balancer, and MongoDB Setup Guide

Instructions to create AWS resources dynamically including VPC, Subnet, Security Groups, EC2 instance, configuring a load balancer, and using MongoDB, following best practices for handling keys and user passwords.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Creating AWS Resources](#creating-aws-resources)
- [Setting Up Nginx](#setting-up-nginx)
- [Configuring a Load Balancer](#configuring-a-load-balancer)
- [Using MongoDB from the Command Line](#using-mongodb)
- [Best Practices for Keys and Passwords](#best-practices-for-keys-and-passwords)

## Prerequisites
- AWS Account
- AWS CLI installed and configured
- MongoDB installed on your local machine
- SSH client

## Creating AWS Resources

1. **Create a VPC:**
   ```bash
   VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
   ```

2. **Create a Subnet:**
   ```bash
   SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --query 'Subnet.SubnetId' --output text)
   ```

3. **Create an Internet Gateway and attach it to the VPC:**
   ```bash
   IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
   aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
   ```

4. **Create a Route Table and a public route:**
   ```bash
   ROUTE_TABLE_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
   aws ec2 create-route --route-table-id $ROUTE_TABLE_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
   aws ec2 associate-route-table --subnet-id $SUBNET_ID --route-table-id $ROUTE_TABLE_ID
   ```

5. **Create a Security Group:**
   ```bash
   SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name my-sg --description "My security group" --vpc-id $VPC_ID --query 'GroupId' --output text)
   aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
   aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
   ```

6. **Launch an EC2 instance:**
   ```bash
   INSTANCE_ID=$(aws ec2 run-instances \
     --image-id ami-0abcdef1234567890 \
     --instance-type t2.micro \
     --key-name MyKeyPair \
     --security-group-ids $SECURITY_GROUP_ID \
     --subnet-id $SUBNET_ID \
     --associate-public-ip-address \
     --query 'Instances[0].InstanceId' --output text)
   ```

7. **Retrieve the public IP:**
   ```bash
   PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
     --query "Reservations[*].Instances[*].PublicIpAddress" --output text)
   ```

8. **SSH into the instance:**
   ```bash
   ssh -i path/to/MyKeyPair.pem ec2-user@$PUBLIC_IP
   ```

## Setting Up Nginx

1. **Update and install necessary packages:**
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   sudo apt-get install -y nginx
   ```

2. **Configure Nginx:**
   - Edit `/etc/nginx/sites-available/default`:
     ```nginx
     server {
         listen 80;
         server_name $PUBLIC_IP;

         location / {
             proxy_pass http://localhost:3000;
             proxy_http_version 1.1;
             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection 'upgrade';
             proxy_set_header Host $host;
             proxy_cache_bypass $http_upgrade;
         }
     }
     ```

4. **Restart Nginx:**
   ```bash
   sudo systemctl restart nginx
   ```

## Configuring a Load Balancer

1. **Create a load balancer:**
   ```bash
   LOAD_BALANCER_ARN=$(aws elbv2 create-load-balancer \
     --name my-load-balancer \
     --subnets $SUBNET_ID \
     --security-groups $SECURITY_GROUP_ID \
     --query 'LoadBalancers[0].LoadBalancerArn' --output text)
   ```

2. **Create target groups:**
   ```bash
   TARGET_GROUP_ARN=$(aws elbv2 create-target-group \
     --name my-targets \
     --protocol HTTP \
     --port 80 \
     --vpc-id $VPC_ID \
     --query 'TargetGroups[0].TargetGroupArn' --output text)
   ```

3. **Register targets:**
   ```bash
   aws elbv2 register-targets \
     --target-group-arn $TARGET_GROUP_ARN \
     --targets Id=$INSTANCE_ID
   ```

4. **Create a listener:**
   ```bash
   aws elbv2 create-listener \
     --load-balancer-arn $LOAD_BALANCER_ARN \
     --protocol HTTP \
     --port 80 \
     --default-actions Type=forward,TargetGroupArn=$TARGET_GROUP_ARN
   ```

## Using MongoDB from the Command Line

1. **Install MongoDB:**
   ```bash
   sudo apt-get install -y mongodb
   ```

2. **Start MongoDB service:**
   ```bash
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   ```

3. **Access MongoDB shell:**
   ```bash
   mongo
   ```

4. **Basic MongoDB commands:**
   ```javascript
   use mydatabase
   db.createCollection("mycollection")
   db.mycollection.insert({ name: "John Doe", age: 30, status: "active" })
   db.mycollection.find()
   ```

## Best Practices for Keys and Passwords

1. **Store keys and passwords in files:**
   - Create a directory for sensitive files:
     ```bash
     mkdir -p ~/secrets
     ```

   - Save your keys and passwords in files within this directory.

2. **Set permissions for the directory and files:**
   ```bash
   chmod 700 ~/secrets
   chmod 600 ~/secrets/*
   ```

3. **Access keys and passwords in scripts:**
   ```bash
   KEY=$(cat ~/secrets/mykey.pem)
   PASSWORD=$(cat ~/secrets/mypassword.txt)
   ```

4. **Use environment variables:**
   ```bash
   export MY_KEY=$(cat ~/secrets/mykey.pem)
   export MY_PASSWORD=$(cat ~/secrets/mypassword.txt)
   ```

5. **Example usage in a script:**
   ```bash
   #!/bin/bash
   export KEY=$(cat ~/secrets/mykey.pem)
   export PASSWORD=$(cat ~/secrets/mypassword.txt)

   # Use the key and password
   ssh -i "$KEY" user@host
   ```

## Conclusion

By following this guide, you will have a secure and functional AWS EC2 instance with a VPS, load balancer, and MongoDB set up. Always follow best practices for managing keys and passwords to ensure your setup is secure.
```
