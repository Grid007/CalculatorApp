pipeline {
  agent any
  environment {
    // AWS Credentials stored in Jenkins
    PIPELINE_USER_CREDENTIAL_ID = 'aws-access'
    SAM_TEMPLATE = 'template.yaml'
    
    // Branch and Stack Names
    MAIN_BRANCH = 'main'
    TESTING_STACK_NAME = 'sam-pipe-dev'
    PROD_STACK_NAME = 'sam-pipe-prod'

    // IAM Roles for Testing and Production
    TESTING_PIPELINE_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/testing-pipeline-execution-role'
    TESTING_CLOUDFORMATION_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/testing-cloudformation-execution-role'
    PROD_PIPELINE_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/prod-pipeline-execution-role'
    PROD_CLOUDFORMATION_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/prod-cloudformation-execution-role'
    
    // S3 Buckets for Storing Artifacts
    TESTING_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-dev-pipeline'
    PROD_ARTIFACTS_BUCKET = 'aws-sam-cli-managed-prod-pipeline'
    
    // AWS Regions
    TESTING_REGION = 'ap-south-1'
    PROD_REGION = 'ap-south-1'
  }
  stages {
    
    // Stage: Unit Testing
    stage('unit-test') {
      steps {
        script {
          echo "Running unit tests with unittest discover"
          // Using unittest's discovery to run all tests in the tests/ directory
          sh '''
            python3 -m unittest discover -s tests
          '''
        }
      }
    }

    // Stage: Build and Package (For all branches)
    stage('build-and-package') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
          args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        echo "Building and packaging with SAM"

        // Build and package for Testing environment
        sh 'sam build --template ${SAM_TEMPLATE} --use-container'
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.TESTING_REGION, role: env.TESTING_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam package --s3-bucket ${TESTING_ARTIFACTS_BUCKET} --region ${TESTING_REGION} --output-template-file packaged-testing.yaml
          '''
        }

        // Build and package for Production environment
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.PROD_REGION, role: env.PROD_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam package --s3-bucket ${PROD_ARTIFACTS_BUCKET} --region ${PROD_REGION} --output-template-file packaged-prod.yaml
          '''
        }

        // Archive the packaged artifacts
        archiveArtifacts artifacts: 'packaged-testing.yaml'
        archiveArtifacts artifacts: 'packaged-prod.yaml'
      }
    }

    // Stage: Deploy to Testing Environment (Always Runs)
    stage('deploy-testing') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
        }
      }
      steps {
        echo "Deploying to Testing Environment"
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.TESTING_REGION, role: env.TESTING_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam deploy --stack-name ${TESTING_STACK_NAME} \
              --template-file packaged-testing.yaml \
              --capabilities CAPABILITY_IAM \
              --region ${TESTING_REGION} \
              --s3-bucket ${TESTING_ARTIFACTS_BUCKET} \
              --no-fail-on-empty-changeset \
              --role-arn ${TESTING_CLOUDFORMATION_EXECUTION_ROLE}
          '''
        }
      }
    }

    // Stage: Integration Testing
    stage('integration-test') {
      steps {
        script {
          echo "Running integration tests"
          // Run your integration tests here
          sh '''
            # Example: integration tests, replace with your specific tests
            ./run-integration-tests.sh
          '''
        }
      }
    }

    // Stage: Deploy to Production (Runs for all branches)
    stage('deploy-prod') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
        }
      }
      steps {
        echo "Deploying to Production Environment"
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.PROD_REGION, role: env.PROD_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam deploy --stack-name ${PROD_STACK_NAME} \
              --template-file packaged-prod.yaml \
              --capabilities CAPABILITY_IAM \
              --region ${PROD_REGION} \
              --s3-bucket ${PROD_ARTIFACTS_BUCKET} \
              --no-fail-on-empty-changeset \
              --role-arn ${PROD_CLOUDFORMATION_EXECUTION_ROLE}
          '''
        }
      }
    }
  }
}
