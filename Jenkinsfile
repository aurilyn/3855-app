pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout the code from the repository
                    checkout scm
                }
            }
        }
        stage('Linting') {
            steps {
                script {
                    // Define the folders to lint
                    def foldersToLint = ['folder1', 'folder2', 'folder3', 'folder4']

                    // Install dependencies (if needed)
                    sh 'pip install pylint'

                    // Lint each folder
                    for (folder in foldersToLint) {
                        echo "Linting ${folder}..."
                        
                        // Run pylint command
                        sh "pylint ${folder}"
                    }
                }
            }
        }
    }
}
