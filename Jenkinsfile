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
                    
                    sh 'apt-get update'
                    sh 'apt-get upgrade'
                    sh 'apt install python3-pip'
                    sh 'pip install pylint'
                    for (folder in foldersToLint) {
                        echo "Linting ${folder}..."
                    
                        sh "pylint ${folder}"
                    }
                }
            }
        }
    }
}
