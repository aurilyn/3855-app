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
        stage('Security') {
            steps {
                script {
                    def foldersToLint = ['Audit', 'Receiver', 'Storage', 'Processing']
                    
                    for (folder in foldersToLint) {
                        echo "Scanning ${folder}..."
                        sh "pip install safety --break-system-packages"
                        sh "safety check --full-report --json --file ${folder}/requirements.txt"
                    }
                }
            }
        }
    }
}
