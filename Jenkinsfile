pipeline {
    agent {
        docker {
            image 'lambci/lambda:build-python3.8'
        }
    }

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'  // Specify your AWS region
        S3_BUCKET = 'my-calc-store'  // Replace with your actual S3 bucket
        STACK_NAME = 'simple-calculator'  // Replace with your CloudFormation stack name
        TESTING_STACK_NAME = 'sam-app-dev'
        PROD_STACK_NAME = 'sam-app-prod'
        TESTING_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-dev-pipeline-r-artifactsbucket-5xu5ikopmgzs'
        PROD_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-prod-pipeline--artifactsbucket-xtw0s9zf73um'
        PIPELINE_USER_CREDENTIAL_ID = 'aws-access'
        TESTING_REGION = 'ap-south-1'
        PROD_REGION = 'ap-south-1'
        SAM_TEMPLATE = 'template.yaml'
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
                    sam build --template ${SAM_TEMPLATE} 
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
                      --output-template-file packaged-testing.yaml \
                      --s3-bucket ${TESTING_ARTIFACTS_BUCKET} \
                      --region ${TESTING_REGION}
                    sam package \
                      --output-template-file packaged-prod.yaml \
                      --s3-bucket ${PROD_ARTIFACTS_BUCKET} \
                      --region ${PROD_REGION}
                    '''
                }
            }
        }

        stage('Deploy to Testing') {
            steps {
                script {
                    // Activate virtual environment and deploy to testing environment
                    withAWS(
                        credentials: env.PIPELINE_USER_CREDENTIAL_ID,
                        region: env.TESTING_REGION,
                        role: 'arn:aws:iam::592789829210:role/aws-sam-cli-managed-dev-pipel-PipelineExecutionRole-87kZ0YKd50ZD'
                    ) {
                        sh '''
                        . /tmp/venv/bin/activate
                        sam deploy --stack-name ${TESTING_STACK_NAME} \
                          --template-file packaged-testing.yaml \
                          --capabilities CAPABILITY_IAM \
                          --region ${TESTING_REGION} \
                          --no-fail-on-empty-changeset
                        '''
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Activate virtual environment and deploy to production environment
                    withAWS(
                        credentials: env.PIPELINE_USER_CREDENTIAL_ID,
                        region: env.PROD_REGION,
                        role: 'arn:aws:iam::592789829210:role/aws-sam-cli-managed-prod-pipe-PipelineExecutionRole-kQLSS8Ph06qW'
                    ) {
                        sh '''
                        . /tmp/venv/bin/activate
                        sam deploy --stack-name ${PROD_STACK_NAME} \
                          --template-file packaged-prod.yaml \
                          --capabilities CAPABILITY_IAM \
                          --region ${PROD_REGION} \
                          --no-fail-on-empty-changeset
                        '''
                    }
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
