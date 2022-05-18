from flask import Flask, request
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
connectionString = "DefaultEndpointsProtocol=https;AccountName=uploadfileimg;AccountKey=NekWp7RJDchJTGZ076EecB3linFo/J/lkUU3hrxuGv5W1khPgpFNA/CfWcMnzM8nnHVFibvkUp3C+AStCt9sUA==;EndpointSuffix=core.windows.net"
container_name = "uploads"

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connectionString)
container_client = blob_service_client.get_container_client(container= container_name)
container_client.get_container_properties()
@app.route("/")
def upload():
    blob_items = container_client.list_blobs()
    img_html = ""
    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name)
        img_html += "<img src='{}' width='auto' height='200'/>".format(blob_client.url)
    return '''
        <h1>Upload New File</h1>
        <form method="post" action="/uploadFiles" enctype="multipart/form-data">
            <input type="file" name="files" multiple>
            <input type="submit">
        </form>
        '''+ img_html
        
@app.route("/uploadFiles", methods=["POST"])
def uploadFiles():
    for file in request.files.getlist("files"):
        try:
            container_client.upload_blob(file.filename, file)
        except Exception as e:
            print(e)
    return "<p>Uploaded</p>"

if __name__ == "__main__":
    app.run()