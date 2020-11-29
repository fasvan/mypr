def sendEmailOnFailure() {
    emailext(attachLog: true, body: "$BUILD_URL", subject: "Failure: $JOB_NAME #${env.BUILD_NUMBER}",
        recipientProviders: [[$class: 'RequesterRecipientProvider'], [$class: 'DevelopersRecipientProvider']])
}

pipeline {
    agent any

    environment {
        TESTS_CONTAINER = 'integ-tests'
    }

    parameters {
        booleanParam(defaultValue: false, description: 'Deploy', name: 'PUSH_AND_DEPLOY')
    }

    options{
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }

    stages {
        stage('Build image') {
            steps{
                sh('cd app/ && docker build . -t web-app')
            }
        }

        stage('Start service') {
            steps{
                sh('cd app/ && docker-compose up -d')
            }
        }

        stage('Run integration tests') {
            steps{
                sh('cd tests/integration/ && docker build . -t integration-tests')
                sh('docker run --network=host --name ${TESTS_CONTAINER} integration-tests')
            }
        }

        stage('Push (mock stage)'){
            when {
                expression {
                    params.PUSH_AND_DEPLOY == true
                }
            }
            steps{
                withCredentials([usernamePassword(credentialsId: "azure_registry", passwordVariable: "azure_pass", usernameVariable: "azure_name")]) {
                    sh('docker login -u "${azure_name}" -p "${azure_pass}" testingprimer.azurecr.io')
                    sh('docker tag web-app testingprimer.azurecr.io/web-app')
                    sh('docker push testingprimer.azurecr.io/web-app')
                }
            }
        }
    }

    post {
        always {
            sh('docker cp ${TESTS_CONTAINER}:/allure-results ${WORKSPACE}')
            allure ([results: [[path: 'allure-results']]])
            sh('cd app/ && docker-compose down')
            sh('docker rm ${TESTS_CONTAINER}')
            cleanWs()
        }
        failure {
            sendEmailOnFailure()
        }
    }
}