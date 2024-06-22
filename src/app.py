from flask import Flask, render_template, url_for

app = Flask(__name__)
app.config.from_object("gui.config.Config")
db = SQLAlchemy(app)


# テーブルモデルの定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# データベースの初期化
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        # サンプルデータの挿入
        sample_users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
            User(name="Charlie", email="charlie@example.com"),
        ]
        db.session.bulk_save_objects(sample_users)
        db.session.commit()


@app.route("/")
def index():
    users = User.query.all()
    return render_template("table.html", users=users)


@app.route("/user/<int:user_id>")
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
