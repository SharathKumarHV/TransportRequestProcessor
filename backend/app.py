from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Server is running OK"

def count_lines_file(fpath: str) -> int:
    with open(fpath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

def cofile_generator(tr: str) -> str:
    tr = tr.strip()
    cofile = tr[3:] + "." + tr[:3]
    return cofile

def datafile_generator(tr: str) -> str:
    tr = tr.strip()
    sid = tr[:3]
    datafile = "R" + tr[4:] + "." + sid
    return datafile

@app.route("/")
def home():
    return "Server is running OK"

@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]

    upload_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    file.save(upload_tmp.name)
    fpath = upload_tmp.name

    count = count_lines_file(fpath)

    if count == 0:
        return jsonify({
            "error": "Include at least one Transport Request (TR) in the file"
        }), 400

    co_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    da_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")

    with open(fpath, "r", encoding="utf-8") as f, open(co_tmp.name, "a+") as f2, open(da_tmp.name, "a+") as f3:
        for _ in range(count):
            line = f.readline().strip()
            if not line:
                continue
            f2.write(cofile_generator(line) + "\n")
            f3.write(datafile_generator(line) + "\n")

    return jsonify({
        "count": count,
        "cofile": os.path.basename(co_tmp.name),
        "datafile": os.path.basename(da_tmp.name),
        "cofile_path": co_tmp.name,
        "datafile_path": da_tmp.name
    })

@app.route("/download", methods=["GET"])
def download():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

