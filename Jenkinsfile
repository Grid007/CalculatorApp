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
                sh '''
                python3 -m pip install --upgrade pip
                python3 -m pip install wheel
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'sam build'
            }
        }

        stage('Package') {
            steps {
                sh '''
                sam package \
                  --output-template-file packaged.yaml \
                  --s3-bucket ${S3_BUCKET}
                '''
            }
        }

        stage('Deploy') {
            steps {
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
