pipeline {
    agent {
        docker {
            image 'lambci/lambda:build-python3.8'
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'  // Specify your AWS region
        S3_BUCKET = 'my-calc-store'  // Replace with your actual S3 bucket
        STACK_NAME = 'simple-calculator'     // Replace with your CloudFormation stack name
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Create and activate a virtual environment
                    sh '''
                    python3 -m venv /tmp/venv
                    . /tmp/venv/bin/activate
                    pip install --upgrade pip
                    pip install wheel
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    // Activate virtual environment and build the SAM project
                    sh '''
                    . /tmp/venv/bin/activate
                    sam build
                    '''
                }
            }
        }

        stage('Package') {
            steps {
                script {
                    // Activate virtual environment and package the Lambda function
                    sh '''
                    . /tmp/venv/bin/activate
                    sam package \
                      --output-template-file packaged.yaml \
                      --s3-bucket ${S3_BUCKET}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Activate virtual environment and deploy the CloudFormation stack
                    sh '''
                    . /tmp/venv/bin/activate
                    sam deploy \
                      --template-file packaged.yaml \
                      --stack-name ${STACK_NAME} \
                      --capabilities CAPABILITY_IAM \
                      --region ${AWS_DEFAULT_REGION}
                    '''
                }
            }
        }
    }

    post {
        always {
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
