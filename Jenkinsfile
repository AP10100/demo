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
                sudo docker images -q apsp/index-image_new | xargs sudo docker rmi -f | true
                sudo docker images -q index-image_new | xargs sudo docker rmi -f | true
                sudo docker build -t index-image_new:\${BUILD_NUMBER} .
                '''
            }
        }
        stage('push Docker Image') {
            steps {
                sh '''
                sudo docker tag index-image_new:\${BUILD_NUMBER} apsp/index-image_new:\${BUILD_NUMBER}
                sudo docker push apsp/index-image_new:\${BUILD_NUMBER}
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
               sudo helm uninstall index | true
               rm -r my-chart/index-chart | true
               mkdir my-chart | true
               helm create my-chart/index-chart
               ''' 
            }
        }
        stage('helm default changes'){
            steps {
               sh '''
               sed -i '24s/^/# /' my-chart/index-chart/Chart.yaml
               sed -i '5s/replicaCount: 1/replicaCount: 2/' my-chart/index-chart/values.yaml
               sed -i '40s/type: ClusterIP/type: NodePort/' my-chart/index-chart/values.yaml
               sed -i '40,47 s/^/#/' my-chart/index-chart/templates/deployment.yaml
               sed -i '41s/port: 80/port: 8080/' my-chart/index-chart/values.yaml 
               sed -i '8s/^/# /' my-chart/index-chart/values.yaml
               sed -i '11s/^/# /' my-chart/index-chart/values.yaml
               sed -i "12i\r  tag: ${BUILD_NUMBER}" my-chart/index-chart/values.yaml
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
                sudo helm install index my-chart/index-chart
                sudo kubectl get all
                export NODE_PORT=$(sudo kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services index-index-chart)
                export NODE_IP=$(sudo kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
                echo http://$NODE_IP:$NODE_PORT
                '''
            } 
        }
        // Other stages of your pipeline
    }

}
