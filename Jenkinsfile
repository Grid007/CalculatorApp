pipeline {
  agent any
  environment {
    PIPELINE_USER_CREDENTIAL_ID = 'aws-access'
    SAM_TEMPLATE = 'template.yaml'
    MAIN_BRANCH = 'main'
    TESTING_STACK_NAME = 'sam-pipe-dev'
    PROD_STACK_NAME = 'sam-pipe-prod'
    TESTING_PIPELINE_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/testing-pipeline-execution-role'
    TESTING_CLOUDFORMATION_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/testing-cloudformation-execution-role'
    PROD_PIPELINE_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/prod-pipeline-execution-role'
    PROD_CLOUDFORMATION_EXECUTION_ROLE = 'arn:aws:iam::592789829210:role/prod-cloudformation-execution-role'
    
    // Updated S3 Buckets
    TESTING_ARTIFACTS_BUCKET = 'my-calc-store'
    PROD_ARTIFACTS_BUCKET = 'my-calc-store'
    
    TESTING_REGION = 'ap-south-1'
    PROD_REGION = 'ap-south-1'
  }
  stages {
    stage('unit-test') {
      steps {
        script {
          echo "Running unit tests with unittest discover"
          sh 'python3 -m unittest discover -s tests'
        }
      }
    }

    stage('build-and-package') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
          args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        echo "Building and packaging with SAM"
        sh 'sed -i \'s/resolve_s3 = true/# resolve_s3 = true/\' samconfig.toml'

        // Build and package for Testing environment
        sh 'sam build --template ${SAM_TEMPLATE} --use-container'
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.TESTING_REGION, role: env.TESTING_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam package --s3-bucket ${TESTING_ARTIFACTS_BUCKET} --region ${TESTING_REGION} --output-template-file packaged-testing.yaml
          '''
        }

        // Archive the packaged artifacts
        archiveArtifacts artifacts: 'packaged-testing.yaml'
      }
    }

    stage('deploy-testing') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
          args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      environment {
        SAM_CLI_CONFIG_DIR = '$WORKSPACE/sam-config' // Specify a writable directory for SAM CLI
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

    stage('integration-test') {
      steps {
        echo "Running integration tests"
        // Add your integration tests here
      }
    }

    stage('build-and-package-prod') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
          args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      steps {
        echo "Building and packaging for Production"
        sh 'sam build --template ${SAM_TEMPLATE} --use-container'
        withAWS(credentials: env.PIPELINE_USER_CREDENTIAL_ID, region: env.PROD_REGION, role: env.PROD_PIPELINE_EXECUTION_ROLE) {
          sh '''
            sam package --s3-bucket ${PROD_ARTIFACTS_BUCKET} --region ${PROD_REGION} --output-template-file packaged-prod.yaml
          '''
        }

        // Archive the packaged artifacts
        archiveArtifacts artifacts: 'packaged-prod.yaml'
      }
    }

    stage('deploy-production') {
      agent {
        docker {
          image 'public.ecr.aws/sam/build-provided'
          args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
      }
      environment {
        SAM_CLI_CONFIG_DIR = '$WORKSPACE/sam-config' // Specify a writable directory for SAM CLI
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

    stage('cleanup') {
      steps {
        echo "Cleaning up"
        // Add cleanup steps if needed
      }
    }
  }
}
