pipeline {
    agent any

    stages {
        stage('Docker Login') {
            steps {
                script {
                    def dockerCredentialsId = 'daecaa81-f96c-442b-b2a2-c337d5348879' // Use the ID you specified
                    withCredentials([usernamePassword(credentialsId: dockerCredentialsId, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "sudo docker login -u \$DOCKER_USERNAME -p \$DOCKER_PASSWORD"
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh '''
                sudo docker build -t index-image .
                '''
            }
        }
        stage('push Docker Image') {
            steps {
                sh '''
                sudo docker tag index-image apsp/index-image
                sudo docker push apsp/index-image
                '''
            }
        }
        stage('helm chart creation'){
            steps {
               sh '''
               rm -r my-chart/index-chart | true
               mkdir my-chart | true
               helm create my-chart/index-chart
               ''' 
            }
        }
        // Other stages of your pipeline
    }

}
