pipeline {
    agent {
        docker {
            // Use the official AWS Lambda Docker image for Python 3.8
            image 'lambci/lambda:build-python3.8'
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'  // Specify your AWS region
        S3_BUCKET = 'my-calc-store'  // Replace with your actual S3 bucket
        STACK_NAME = 'simple-calculator'  // Replace with your CloudFormation stack name
        PIP_TARGET = '/tmp/pip'  // Directory to install pip packages
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
                    // Upgrade pip and install wheel using --target to avoid permission issues
                    sh '''
                        python3 -m pip install --upgrade pip --target ${PIP_TARGET}
                        python3 -m pip install wheel --target ${PIP_TARGET}
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                // Build the SAM project
                sh '''
                export PYTHONPATH=$PYTHONPATH:${PIP_TARGET}
                sam build
                '''
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
