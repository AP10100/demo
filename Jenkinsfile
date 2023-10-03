/* groovylint-disable DuplicateStringLiteral, GStringExpressionWithinString, LineLength, NestedBlockDepth, NoDef, VariableTypeRequired */
/* groovylint-disable-next-line CompileStatic */
pipeline {
    agent any

    environment {
            DOCKER_IMAGE = 'apsp/kube-demo-image'
            PORT_NUMBER = '8080'
            TYPE = 'NodePort'
            HELM_RELEASE = 'index'
            HELM_PACKAGE = 'index-chart'
            REPLICA_COUNT = 2
            NODEPORT = 30001
            TAG = "${BUILD_NUMBER}"
            IS_INSTALLED_SAME_PIPELINE = 'NO'
    }
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
                sudo docker build -t \$DOCKER_IMAGE:\${TAG} .
                '''
            }
        }
        stage('push Docker Image') {
            steps {
                sh '''
                sudo docker push \$DOCKER_IMAGE:\${TAG}
                '''
            }
        }
        stage('helm chart creation') {
            steps {
                sh '''
                  helm create \$HELM_PACKAGE | true
                '''
            }
        }
        stage('helm default changes') {
            steps {
                sh '''
               python3 script.py
               nl -b a \$HELM_PACKAGE/values.yaml
               nl -b a \$HELM_PACKAGE/templates/service.yaml
               nl -b a \$HELM_PACKAGE/Chart.yaml
               nl -b a \$HELM_PACKAGE/templates/deployment.yaml
               '''
            }
        }

        stage('implimentation') {
            when {
                expression {
                    IS_INSTALLED != 'YES'
                }
            }
            environment {
                IS_INSTALLED = 'YES'
                IS_INSTALLED_SAME_PIPELINE = 'YES'
            }
            steps {
                sh '''
                sudo helm install \$HELM_RELEASE  \$HELM_PACKAGE
                sudo kubectl get all
                export NODE_PORT=$(sudo kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services index-index-chart)
                export NODE_IP=$(sudo kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
                echo http://$NODE_IP:$NODE_PORT
                '''
            }
        }

        stage('Chart upgrade') {
            when {
                expression {
                    /* groovylint-disable-next-line UnnecessaryBooleanExpression */
                    IS_INSTALLED = 'YES' && IS_INSTALLED_SAME_PIPELINE != 'YES'
                }
            }
            steps {
                sh '''
               sudo helm upgrade \$HELM_RELEASE \$HELM_PACKAGE
               export NODE_PORT=$(sudo kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services \$HELM_RELEASE)
               export NODE_IP=$(sudo kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
               echo http://$NODE_IP:$NODE_PORT
               '''
            }
        }
    // Other stages of your pipeline
    }
}
