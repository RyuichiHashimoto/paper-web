from flask import Flask, render_template, request, send_file, jsonify
from db.model import Paper, Author, PaperAuthor, get_cloudfilepath_from_paper_id, insert_paper_record_to_db, update_paper_record
import os
from cloud.azureStorageClient import AzuriteStorageClient, generate_unique_paper_uuid
import tempfile

# TEMPLATE_ROOT_PATH = "./gui/template/"

app = Flask(__name__, template_folder="./gui/template/", static_folder="./gui/resource")
app.config.from_object("gui.config.Config")


@app.route("/")
def index():
    papers = Paper.select()
    return render_template("paper_list.html", papers=papers)


@app.route("/paper/<paper_id>")
def paper(paper_id):

    # papers = Paper.select()
    paper = Paper.select().where(Paper.paper_id == paper_id).first()

    authors = Author.select().join(PaperAuthor, on=(Author.author_id == PaperAuthor.author_id)).where(PaperAuthor.paper_id == paper_id)
    return render_template("paper_detail.html", paper=paper, authors=authors)


@app.route("/edit/<paper_id>")
def edit(paper_id):
    # 編集ページへの遷移処理
    # 実際の編集ページの実装は省略
    return f"Edit paper with ID: {paper_id}"


@app.route("/view/<paper_id>")
def view_pdf(paper_id):
    cloudfilepath = get_cloudfilepath_from_paper_id(paper_id)

    if not cloudfilepath:
        return f"paper id {paper_id} is not registered", 404

    try:
        client = AzuriteStorageClient()

        if not client.exist_file(cloudfilepath):
            return "File not found", 404

        with tempfile.TemporaryDirectory() as tempdir:
            local_file_path = os.path.join(tempdir, f"{paper_id}.pdf")
            client.donwload(cloudfilepath, local_file_path)
            return send_file(local_file_path, as_attachment=False)
    except Exception as e:
        return str(e), 500


@app.route("/upload", methods=["POST"])
def upload_file():

    title = request.form.get("title")

    if "pdf" not in request.files:
        return jsonify(success=False, message="No file part")

    if (title is None) or (title == ""):
        return jsonify(success=False, message="No title part")

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify(success=False, message="No selected file")

    if file and file.filename.endswith(".pdf"):
        with tempfile.TemporaryDirectory() as tempdir:
            tmpfile = os.path.join(tempdir, file.filename)
            file.save(tmpfile)

            client = AzuriteStorageClient()
            uuid = generate_unique_paper_uuid()
            client.upload(tmpfile, f"raw/{uuid}.pdf")

            insert_paper_record_to_db(title, f"raw/{uuid}.pdf")

        # file.save("sample.pdf")
        return jsonify(success=True, message="File uploaded successfully")
    else:
        return jsonify(success=False, message="File is not a PDF")


@app.route("/update-paper-detail", methods=["POST"])
def update_paper_detail():
    paperid = request.form.get("paper-id")
    title = request.form.get("title")
    description = request.form.get("description")
    source_reference = request.form.get("source_reference")
    url = request.form.get("url")
    public_date = request.form.get("public_date")

    result = update_paper_record(paperid, title, description, source_reference, url, public_date)

    if result:
        ret = jsonify(success=True, message="Paper information updated successfully")
    else:
        ret = jsonify(success=True, message="Paper information updated failed")

    return ret


@app.route("/delete/<paper_id>")
def delete(paper_id):
    # 論文を削除する処理
    return f"delete paper with ID: {paper_id}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
