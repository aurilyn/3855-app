def call(dockerRepoName, imageName) {
    
    pipeline {
        agent any

        stages {

            stage('Build') {
                steps {
                    sh 'pip install -r requirements.txt --break-system-packages'
                }
            }

            stage('Python Lint') {
                steps {
                    sh 'pylint --fail-under 5.0 *.py'
                }
            }

            stage('Package') {
                steps {
                    withCredentials([string(credentialsId: 'DockerHub', variable: 'TOKEN')]) {
                        sh "docker login -u 'bennycao06' -p '$TOKEN' docker.io"
                        sh "docker build -t ${dockerRepoName}:latest --tag bennycao06/${dockerRepoName}:${imageName} ."
                        sh "docker push bennycao06/${dockerRepoName}:${imageName}"
                    }
                }   
            }
        }
    }
}
