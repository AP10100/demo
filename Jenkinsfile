pipeline {
    agent any

     environment {
            DOCKER_IMAGE = 'apsp/kube-demo-image'
            PORT_NUMBER = '8080'
            TYPE = 'NodePort'
            HELM_RELEASE = 'index'
            HELM_PACKAGE = 'my-chart/index-chart'
            REPLICA_COUNT = 2
            NODEPORT = 30001
            TAG = "${BUILD_NUMBER}"
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
                sudo docker build -t \$DOCKER_IMAGE:\${BUILD_NUMBER} .
                '''
            }
        }
        stage('push Docker Image') {
            steps {
                sh '''
                sudo docker push \$DOCKER_IMAGE:\${BUILD_NUMBER}
                '''
            }
        }
        stage('helm chart creation'){
            steps {
               sh '''
               sudo docker images
               sudo docker image rmi apsp/index-image_new | true
               sudo docker images -f "dangling=true" -q | xargs sudo docker rmi | true
               sudo docker images
               sudo helm uninstall \$HELM_RELEASE | true
               rm -r \$HELM_PACKAGE | true
               mkdir my-chart | true
               helm create \$HELM_PACKAGE
               ''' 
            }
        }
        stage('helm default changes'){
            steps {
               sh '''
               nl -b a my-chart/index-chart/values.yaml 
               nl -b a my-chart/index-chart/templates/service.yaml
               nl -b a my-chart/index-chart/Chart.yaml
               nl -b a my-chart/index-chart/templates/deployment.yaml

               sed -i '24s/^/# /' my-chart/index-chart/Chart.yaml
               sed -i '5s/replicaCount: 1/replicaCount: 2/' my-chart/index-chart/values.yaml
               sed -i '43s/type: ClusterIP/type: NodePort/' my-chart/index-chart/values.yaml
               sed -i '43,50 s/^/#/' \$HELM_PACKAGE/templates/deployment.yaml
               sed -i '44s/port: 80/port: 8080/' my-chart/index-chart/values.yaml 
               sed -i '8s/^/# /' my-chart/index-chart/values.yaml
               sed -i '11s/^/# /' my-chart/index-chart/values.yaml
               sed -i "12i\r  tag: ${BUILD_NUMBER}" \$HELM_PACKAGE/values.yaml
               sed -i "9i\r  repository: apsp/index-image_new" my-chart/index-chart/values.yaml
               sed -i "44i\r  nodePort: 30001" my-chart/index-chart/values.yaml
               sed -i "12i\r      nodePort: {{  .Values.service.nodePort }}" my-chart/index-chart/templates/service.yaml
               
               

               nl -b a my-chart/index-chart/templates/service.yaml
               cd my-chart/index-chart
               nl -b a values.yaml 
               
               
               '''
            }
        }




        
        stage('implimentation'){
            steps {
                sh '''
                sudo helm install \$HELM_RELEASE  \$HELM_PACKAGE
                sudo kubectl get all
                export NODE_PORT=$(sudo kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services \$HELM_RELEASE)
                export NODE_IP=$(sudo kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
                echo http://$NODE_IP:$NODE_PORT
                '''
            } 
        }
        // Other stages of your pipeline
    }

}
