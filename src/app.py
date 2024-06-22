from flask import Flask, render_template, url_for
from db.model import Paper, Author, PaperAuthor


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


@app.route("/delete/<paper_id>")
def delete(paper_id):
    # 論文を削除する処理
    return f"delete paper with ID: {paper_id}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
