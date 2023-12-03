pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }
        stage('Linting') {
            steps {
                script {
                    def foldersToLint = ['Audit', 'Receiver', 'Storage', 'Processing']
                    
                    sh 'apt install -y python3-pip'
                    sh 'pip install pylint'
                    
                    for (folder in foldersToLint) {
                        echo "Linting ${folder}..."
                        sh 'pip install -r requirements.txt'
                        sh "pylint ${folder}"
                    }
                }
            }
        }
    }
}
