from flask import Flask, render_template, request, send_file, jsonify
from playhouse.shortcuts import model_to_dict
import markdown
from db.model import (
    Paper,
    Author,
    PaperAuthor,
    get_cloudfilepath_from_paper_id,
    insert_paper_record_to_db,
    update_paper_record,
    get_llm_summary_from_db,
    get_llmprompt_list_as_list,
    get_paper_list_as_list,
    get_paper_metainfo_from_db,
    insert_llmsummary_record_to_db,
    get_llmprompt_id_name_list,
)
import os
from cloud.azureStorageClient import AzuriteStorageClient, generate_unique_paper_uuid
import tempfile
from flask_cors import CORS

app = Flask(__name__, template_folder="./gui/template/", static_folder="./gui/resource")
app.config.from_object("gui.config.Config")
CORS(app)


@app.route("/")
def index():
    papers = Paper.select()
    return render_template("paper_list.html", papers=papers)


@app.route("/paper/<paper_id>")
def paper(paper_id):
    prompt_id = "L-00001"

    paper = Paper.select().where(Paper.paper_id == paper_id).first()
    summary = get_llm_summary_from_db(paper_id, prompt_id)
    if summary is None:
        summary = "No Summary"

    authors = Author.select().join(PaperAuthor, on=(Author.author_id == PaperAuthor.author_id)).where(PaperAuthor.paper_id == paper_id)
    return render_template("paper_detail.html", paper=paper, authors=authors, summary=markdown.markdown(summary))


@app.route("/edit/<paper_id>")
def edit(paper_id):
    return f"Edit paper with ID: {paper_id}"


@app.route("/api/get-paper-metainfo/<paper_id>")
def get_paper_metainfo(paper_id: str):
    metainfo = get_paper_metainfo_from_db(paper_id)

    if metainfo is None:
        return jsonify(success=False, message="No title part")

    return jsonify(success=True, metainfo=metainfo)


@app.route("/api/get-paper-summary/<paper_id>/<prompt_id>")
def get_paper_summary(paper_id: str, prompt_id: str):
    summary = get_llm_summary_from_db(paper_id, prompt_id)

    if summary is None:
        return jsonify(success=False, message="There is no prompt")

    return jsonify(success=True, summary=summary)


@app.route("/api/get-paper-pdf/<paper_id>")
def get_paper_pdf(paper_id):
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


# データ取得エンドポイント
@app.route("/api/get-paper-list", methods=["GET"])
def get_papers():
    return jsonify(get_paper_list_as_list())


@app.route("/api/get-prompt-list", methods=["GET"])
def get_prompt_list():
    return jsonify(get_llmprompt_list_as_list())


@app.route("/api/get-prompt-id-name-list", methods=["GET"])
def get_prompt_id_name_list():
    retlist = get_llmprompt_id_name_list()
    if retlist is None:
        return jsonify(success=False, prompts="No prompt")

    return jsonify(prompts=get_llmprompt_id_name_list(), success=True)


@app.route("/api/dummy/query-to-llm-about-paper/<paper_id>/<prompt_id>", methods=["GET"])
def query_to_llm_about_paper(paper_id: str, prompt_id: str):
    from time import sleep
    from datetime import datetime

    sample_message = f"query result about {paper_id} and {prompt_id} at {datetime.now().isoformat()}"
    sleep(1)

    ret = insert_llmsummary_record_to_db(paper_id=paper_id, prompt_id=prompt_id, summary=sample_message, exist_ok=True)

    if ret:
        return jsonify(success=True, prompts=sample_message)
    else:
        return jsonify(success=False, prompts="Failed to insert summary")


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
    paperid = request.form.get("paper_id")
    title = request.form.get("title")
    abstract = request.form.get("abstract")
    source_reference = request.form.get("source")
    url = request.form.get("url")
    public_date = request.form.get("publication")

    print(paperid, title, abstract, source_reference, url, public_date)
    result = update_paper_record(paperid, title, abstract, source_reference, url, public_date)

    if result:
        ret = jsonify(success=True, message="Paper information updated successfully")
    else:
        ret = jsonify(success=True, message="Paper information updated failed")

    # ret = jsonify(success=False, message="Paper information updated failed")
    # print(ret)
    return ret


@app.route("/delete/<paper_id>")
def delete(paper_id):
    # 論文を削除する処理
    return f"delete paper with ID: {paper_id}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
