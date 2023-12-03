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
        stage('Build') {
                steps {
                    script {
                        def folders = ['Audit', 'Receiver', 'Storage', 'Processing']
                        for (folder in folders) {
                            sh 'pip install -r requirements.txt --break-system-packages'
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
                        sh 'pylint --fail-under 5.0 ${folder}/*.py'
                    }
                }
            }
        }
    }
}
