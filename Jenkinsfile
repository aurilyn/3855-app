pipeline {
    agent any
    
    stages {
        stage('Build') {
                steps {
                    script {
                        def folders = ['Audit', 'Receiver', 'Storage', 'Processing']
                        for (folder in folders) {
                            echo folder
                            sh "pip install -r ${folder}/requirements.txt --break-system-packages"
                            sh "pip install pip-audit --break-system-packages"
                        }
                    }
                }
            }
        stage('Linting') {
            steps {
                script {
                    def foldersToLint = ['Audit', 'Receiver', 'Storage', 'Processing']
                    
                    for (folder in foldersToLint) {
                        echo "Linting ${folder}..."
                        sh "pylint --fail-under 5.0 ${folder}/*.py"
                    }
                }
            }
        }
        stage('Package') {
            steps {
                script {
                    def folders = ['Audit', 'Receiver', 'Storage', 'Processing']
                    for (folder in folders) {
                        withCredentials([string(credentialsId: 'DockerHub', variable: 'TOKEN')]) {
                            sh "docker login -u 'bennycao06' -p '$TOKEN' docker.io"
                            sh "docker build -t ${folder}:latest --tag bennycao06/${folder}:${folder} ."
                            sh "docker push bennycao06/${folder}:${folder}"
                        }
                    }
                }
            }   
        }
    }
}
