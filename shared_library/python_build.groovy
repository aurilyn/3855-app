def call(dockerRepoName, imageName, portNum) {
    
    pipeline {
        agent any

        parameters {
            booleanParam(defaultValue: false, description: 'Deploy the App', name: 'DEPLOY')
        }

        stages {

            stage('Build') {
                steps {
                    sh 'pip install -r requirements.txt --break-system-packages'
                    sh 'pip install --upgrade flask --break-system-packages'
                }
            }

            stage('Python Lint') {
                steps {
                    sh 'pylint --fail-under 5.0 *.py'
                }
            }

            stage('Test and Coverage') {
                steps {
                    script {
                        def test_reports_exist = fileExists 'test-reports'
                        if (test_reports_exist) {
                            sh 'rm test-reports/*.xml || true'
                        }
                        def api_test_reports_exist = fileExists 'api-test-reports'
                        if (api_test_reports_exist) {
                            sh 'rm api-test-reports/*.xml || true'
                        }
                    }

                    script {
                        def filesToTest = findFiles(glob: '**/test*.py')

                        for (testFile in filesToTest) {
                            def testFileName = testFile.name
                            sh "coverage run --omit '*/site-packages/*','*/dist-packages/*' $testFileName"
                        }

                        sh 'coverage report'
                    }

                    script {
                        def test_reports_exist = fileExists 'test-reports'
                        if (test_reports_exist) {
                            junit 'test-reports/*.xml'
                        }
                        def api_test_reports_exist = fileExists 'api-test-reports'
                        if (api_test_reports_exist) {
                            junit 'api-test-reports/*.xml'
                        }
                    }
                }
            }

            stage('Zip Artifacts') {
                steps {
                    sh 'zip -r app.zip *.py'
                    archiveArtifacts artifacts: 'app.zip', allowEmptyArchive: true
                }
            }

            stage('Check Git Branch') {
                steps {
                    script {
                        echo "Current GIT_BRANCH: ${env.GIT_BRANCH}"
                    }
                }
            }


            stage('Package') {
                when {
                    expression { env.GIT_BRANCH == 'origin/main' }
                }
                steps {
                    withCredentials([string(credentialsId: 'DockerHub', variable: 'TOKEN')]) {
                        sh "docker login -u 'bennycao06' -p '$TOKEN' docker.io"
                        sh "docker build -t ${dockerRepoName}:latest --tag bennycao06/${dockerRepoName}:${imageName} ."
                        sh "docker push bennycao06/${dockerRepoName}:${imageName}"
                    }
                }   
            }

            stage('Deliver') {
                when {
                    expression { params.DEPLOY }
                }
                steps {
                    sh "docker stop ${dockerRepoName} || true && docker rm ${dockerRepoName} || true"
                    sh "docker run -d -p ${portNum}:${portNum} --name ${dockerRepoName} ${dockerRepoName}:latest"
                }
            }

        }
    }
}
