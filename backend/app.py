import os  # this was missing earlier
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
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

    # Save uploaded file to generated folder
    os.makedirs("generated", exist_ok=True)
    upload_path = os.path.join("generated", file.filename)
    file.save(upload_path)

    count = count_lines_file(upload_path)

    if count == 0:
        return jsonify({"error": "Include at least one TR in the file"}), 400

    # Output file paths (stored on server)
    cofile_path = os.path.join("generated", "cofiles.txt")
    datafile_path = os.path.join("generated", "datafiles.txt")

    # Clear previous content before writing
    open(cofile_path, "w").close()
    open(datafile_path, "w").close()

    with open(upload_path, "r") as f, open(cofile_path, "a+") as f2, open(datafile_path, "a+") as f3:
        for line in f:
            line = line.strip()
            if not line:
                continue
            f2.write(cofile_generator(line) + "\n")
            f3.write(datafile_generator(line) + "\n")

    return jsonify({
        "count":count,
        "cofile_path": cofile_path,
        "datafile_path": datafile_path
    })


@app.route("/download")
def download():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "File not found on server"}), 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

