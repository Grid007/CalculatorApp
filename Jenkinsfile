pipeline {
    agent {
        docker {
            // Use the official AWS SAM CLI Docker image
            image 'lambci/lambda:build-python3.8'
            
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'  // Specify your AWS region
        S3_BUCKET = 'my-calc-app'  // Replace with your actual S3 bucket
        STACK_NAME = 'simple-calculator'     // Replace with your CloudFormation stack name
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // Build the SAM project
                sh 'sam build'
            }
        }

        stage('Package') {
            steps {
                // Package the Lambda function and upload it to the S3 bucket
                sh '''
                sam package \
                  --output-template-file packaged.yaml \
                  --s3-bucket ${S3_BUCKET}
                '''
            }
        }

        stage('Deploy') {
            steps {
                // Deploy the CloudFormation stack
                sh '''
                sam deploy \
                  --template-file packaged.yaml \
                  --stack-name ${STACK_NAME} \
                  --capabilities CAPABILITY_IAM \
                  --region ${AWS_DEFAULT_REGION}
                '''
            }
        }
    }

    post {
        always {
            // Cleanup workspace
            cleanWs()
        }
        success {
            echo 'Deployment succeeded!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
