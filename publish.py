import os
import gitlab
import sys

# This script takes 2 input arguments. first is package name and second is path to APK
assert len(sys.argv) == 3, 'script takes 2 argument. packageName and APK path'
packageName = sys.argv[1]
apkPath = sys.argv[2]

privateToken = os.getenv('CI_JOB_TOKEN')
serverUrl = os.getenv('CI_SERVER_URL')
projectId = os.getenv('CI_PROJECT_ID')
currentTag = os.getenv('CI_COMMIT_TAG')

# track of google play to publish on
track = 'production'

gl = gitlab.Gitlab(serverUrl, job_token=privateToken)

project = gl.projects.get(projectId, lazy=True)

# NOTE: we use tags to start our CI/CD and publish the apk. If you don't, below line wont work
release = project.releases.get(currentTag)
releaseNotes = release.description



from google.oauth2 import service_account
import googleapiclient.discovery
import mimetypes

mimetypes.add_type("application/octet-stream", ".apk")
mimetypes.add_type("application/octet-stream", ".aab")

print('start publishing apk in google play')

SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_API_CREDENTIAL')

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = googleapiclient.discovery.build('androidpublisher', 'v3', credentials=credentials)

editResponse = service.edits().insert(body={}, packageName=packageName).execute()
print(editResponse)
editId = editResponse['id']
apkResponse = service.edits().apks().upload(editId=editId, packageName=packageName, media_body=apkPath).execute()
print(f"Version code {apkResponse['versionCode']} has been uploaded")
trackResponse = service.edits().tracks().update(
    editId=editId,
    track=track,
    packageName=packageName,
    body={
        'releases': [{
            'versionCodes': [apkResponse['versionCode']],
            'releaseNotes': [{
                'language': 'en',
                'text': releaseNotes
            }],
            # "userFraction": 0.05,
            # "status": "inProgress",
            'status': 'completed',
        }]
    }).execute()
print(trackResponse)

commitResponse = service.edits().commit(editId=editId, packageName=packageName).execute()
print(commitResponse)
print('publishing succeed')
