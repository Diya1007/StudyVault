from flask import Flask, render_template,request, send_file, redirect, url_for
from io import BytesIO

import boto3
app = Flask(__name__)

s3 = boto3.client("s3")
textract = boto3.client("textract",region_name="us-east-2")

BUCKET_NAME = "engcloud007"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["file"]

    if file:

        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            file.filename
        )

        response = textract.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": BUCKET_NAME,
                    "Name": file.filename
                }
            }
        )
        extracted_text = ""

        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"

        # Save extracted text locally
        with open(f"text_{file.filename}.txt", "w") as f:
            f.write(extracted_text)


        return "Upload Successful!"
    
@app.route("/files")
def files():

        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        file_list = []

        if "Contents" in response:
            for obj in response["Contents"]:
                file_list.append(obj["Key"])

        return render_template("files.html", files=file_list)

@app.route("/download/<filename>")
def download_file(filename):

    file_obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )

    return send_file(
        BytesIO(file_obj["Body"].read()),
        download_name=filename,
        as_attachment=True
    )


@app.route("/delete/<filename>")
def delete_file(filename):

    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )

    return redirect(url_for("files"))

@app.route("/search", methods=["GET", "POST"])
def search():

    results = []

    if request.method == "POST":

        keyword = request.form["keyword"].lower()

        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        if "Contents" in response:

            for obj in response["Contents"]:

                filename = obj["Key"]

                # skip text files
                if filename.endswith(".txt"):
                    continue

                try:
                    with open(f"text_{filename}.txt") as f:
                        content = f.read().lower()

                        if keyword in content:
                            results.append(filename)

                except:
                    pass

    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)