import os

HELM_RELEASE = os.environ.get('HELM_RELEASE')
HELM_PACKAGE = os.environ.get('HELM_PACKAGE')
TAG = os.environ.get('TAG')
PORT = os.environ.get('PORT_NUMBER')
NODEPORT = os.environ.get('NODEPORT')
REPLICA_COUNT = os.environ.get('REPLICA_COUNT')
TYPE = os.environ.get('TYPE')
DOCKER_IMAGE = os.environ.get('DOCKER_IMAGE')


def replaceChart():
    path = HELM_PACKAGE+'/Chart.yaml'
    with open(path, 'r') as file:
        data = file.read()
        data = data.replace('appVersion: "1.16.0"', '#appVersion: "1.16.0"')
    with open(path, 'w') as file:
        file.write(data)

def replaceValues():
    print(f'tag: {TAG}'-1)
    path = HELM_PACKAGE+'/values.yaml'
    with open(path, 'r') as file:
        data = file.read()
        data = data.replace('replicaCount: 1', f'replicaCount: {REPLICA_COUNT}')
        data = data.replace('type: ClusterIP', f'type: {TYPE}')
        data = data.replace('repository: nginx', f'repository: {DOCKER_IMAGE}')
        data = data.replace(f'tag: {TAG}'-1, f'tag: {TAG}')
        data = data.replace('port: 80',f'port: {PORT} \n  nodePort: {NODEPORT}')
    with open(path, 'w') as file:
        file.write(data)

def replaceServiceAccount():
    path= HELM_PACKAGE+'/templates/serviceaccount.yaml'
    with open(path, 'r') as file:
        data = file.read()
        data = data.replace('automountServiceAccountToken:', '#automountServiceAccountToken:')
    with open(path, 'w') as file:
        file.write(data)

def replaceService():
    path=HELM_PACKAGE+'/templates/service.yaml'
    with open(path, 'r') as file:
        data = file.read()
        data = data.replace('targetPort: http', 'targetPort: http \n      nodePort: {{ .Values.service.nodePort }}')
    with open(path, 'w') as file:
        file.write(data)

def findLineNumber():
    target_word = 'livenessProbe:'
    path = HELM_PACKAGE+'/templates/deployment.yaml'
    line_number = 0
    with open(path, 'r') as file:
        for line in file:
            line_number += 1
            if target_word in line:
                return line_number

def findLineContent(line_number):
    path = HELM_PACKAGE+'/templates/deployment.yaml'
    with open(path, 'r') as file:
        content = file.readlines()
        return content[line_number-1:line_number+4]

def replaceContent(content):
    path = HELM_PACKAGE+'/templates/deployment.yaml'
    with open(path, 'r') as file:
        data = file.read()
        for i in content:
            print(i)
            data = data.replace(i, '#'+i)
    with open(path, 'w') as file:
        file.write(data)

def replaceDeployment():
    line_number = findLineNumber()
    content = findLineContent(line_number)
    replaceContent(content)
 
replaceChart()
replaceValues()
replaceServiceAccount()
replaceService()
replaceDeployment()
