import React, { useState } from "react";
import axios from "axios";
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [out, setOut] = useState(null);

const handleRun = async () => {
  const form = new FormData();
  form.append("file", file);

  try {
  const res = await axios.post("https://transportrequestprocessor.onrender.com/process", form);

    setOut(res.data);
  } catch (err) {
    alert(err.response?.data?.error || "Include at least one TR in the file");
  }
};


  return (
    <div className="container">
      <h2>TR File Processor</h2>

      <input
        type="file"
        accept=".txt"
        onChange={(e) => setFile(e.target.files[0])}
        className="file-input"
      />

      <button onClick={handleRun}>Process File</button>

      {out && (
        <div className="result-box">
          <p>
            <strong>Total Lines:</strong> {out.count}
          </p>

          <div className="download-links">
            <a
            href={`https://transportrequestprocessor.onrender.com/download?path=${out.cofile_path}`}
              download
            >
              Download Cofile
            </a>
            <a
            href={`https://transportrequestprocessor.onrender.com/download?path=${out.datafile_path}`}
              download
            >
              Download Datafile
            </a>
          </div>
        </div>
      )}

      <footer>Processed using SAP TR formatting logic</footer>
    </div>
  );
}

export default App;
