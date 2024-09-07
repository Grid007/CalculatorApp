pipeline {
    agent {
        docker {
            // Use the official AWS Lambda Python 3.8 build image
            image 'lambci/lambda:build-python3.8'
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'  // AWS region, can be customized
        S3_BUCKET = 'my-calc-app'  // Replace with your actual S3 bucket
        STACK_NAME = 'simple-calculator'  // Replace with your CloudFormation stack name
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Upgrade pip and install wheel before running SAM build
                    sh '''
                        python3 -m pip install --upgrade pip
                        python3 -m pip install wheel
                    '''
                }
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
            // Clean up the workspace after the build process
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
