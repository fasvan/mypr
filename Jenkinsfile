pipeline {
    agent any

    options{
        disableConcurrentBuilds()
        timeout(time: 5, unit: 'MINUTES')
    }

    stages {
        stage('Build image') {
            steps{
                sh('cd httpd/ && docker build . -t httpd')
            }
        }
    }

    post {
        always {
            allure ([results: [[path: 'allure-results']]])
            cleanWs()
        }
        failure {
            sendEmailOnFailure()
        }
    }
}