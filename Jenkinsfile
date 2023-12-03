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
                        def repo = folder.toLowerCase()
                        withCredentials([string(credentialsId: 'DockerHub', variable: 'TOKEN')]) {
                            sh "docker login -u 'bennycao06' -p '$TOKEN' docker.io"
                            sh "docker build -t ${repo}:latest --tag bennycao06/${repo}:latest ./${folder}"
                            sh "docker push bennycao06/${repo}:latest"
                        }
                    }
                }
            }   
        }
        stage('Deploy') {
            steps {
                sshagent(credentials : ['9b469d5e-6263-4a41-b9a7-110010946377']) {
                    sh 'ssh -o StrictHostKeyChecking=no azureuser@3855-benny'
                    sh 'ssh -tt azureuser@3855-benny'
                    sh "docker compose up -d"
                }
            }
        }
    }
}
