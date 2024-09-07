pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        S3_BUCKET = 'my-calc-store'
        STACK_NAME = 'simple-calculator'
        TESTING_STACK_NAME = 'sam-app-dev'
        PROD_STACK_NAME = 'sam-app-prod'
        TESTING_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-dev-pipeline-r-artifactsbucket-5xu5ikopmgzs'
        PROD_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-prod-pipeline--artifactsbucket-xtw0s9zf73um'
        PIPELINE_USER_CREDENTIAL_ID = 'aws-access'
        SAM_TEMPLATE = 'template.yaml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Deploy') {
            steps {
                sh '''
                pip install aws-sam-cli
                sam build --template ${SAM_TEMPLATE}
                sam deploy --stack-name ${TESTING_STACK_NAME} --capabilities CAPABILITY_IAM --region ${AWS_DEFAULT_REGION} --no-fail-on-empty-changeset
                '''
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                sam deploy --stack-name ${PROD_STACK_NAME} --capabilities CAPABILITY_IAM --region ${AWS_DEFAULT_REGION} --no-fail-on-empty-changeset
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