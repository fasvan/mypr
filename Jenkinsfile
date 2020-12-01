def sendEmailOnFailure() {
    emailext(attachLog: true, body: "$BUILD_URL", subject: "Failure: $JOB_NAME #${env.BUILD_NUMBER}",
        recipientProviders: [[$class: 'RequesterRecipientProvider'], [$class: 'DevelopersRecipientProvider']])
}

pipeline {
    agent any

    environment {
        TESTS_CONTAINER = 'integ-tests'
    }

    options{
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }

    stages {
        stage('Build image') {
            steps{
                sh('docker build . -t httpd')
            }
        }

        stage('Start service') {
            steps{
                sh('cd app/ && docker-compose up -d')
            }
        }

        stage('Run httpd tests') {
            steps{
                sh('cd httpd/ && docker build . -t httpd-tests')
                sh('docker run --network=host --name ${TESTS_CONTAINER} httpd-tests')
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