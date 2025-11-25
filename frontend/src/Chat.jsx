import { useState, useEffect } from "react";
import { uploadPdf, askQuestion, listDocuments } from "./api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";

// Modern, professional UI using Tailwind
export default function Chat() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    // Fetch the list of documents on component load
    const fetchDocuments = async () => {
      try {
        const docs = await listDocuments();
        setDocuments(docs || []);
      } catch (error) {
        console.error("Failed to fetch documents:", error);
      }
    };

    fetchDocuments();
  }, []);

  const handleFileUpload = async () => {
    if (!file) {
      alert("Please select a PDF file to upload.");
      return;
    }
    setStatus("Uploading file...");
    try {
      const response = await uploadPdf(file);
      setStatus(`Upload successful: ${JSON.stringify(response)}`);

      // Refresh the document list after a successful upload
      const updatedDocs = await listDocuments();
      setDocuments(updatedDocs || []);
    } catch (error) {
      setStatus("File upload failed. Please try again.");
    }
  };

  const handleQuestionSubmission = async () => {
    if (!question.trim()) {
      alert("Please enter a question before submitting.");
      return;
    }
    setStatus("Processing your query...");
    try {
      const response = await askQuestion(question);
      setAnswer(response);
      setStatus("Query completed successfully.");
    } catch (error) {
      console.error(error);
      setStatus("Failed to process your query. Please try again.");
    }
  };

  return (
    <div className="w-full h-screen flex flex-col p-6 bg-gray-50 text-gray-900">
      {/* Header */}
      <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
        AI Knowledge Assistant
      </h1>

      <div className="flex flex-1 gap-6 text-left">
        {/* Left Panel */}
        <div className="w-1/3 bg-white shadow-md rounded-2xl p-6 border border-gray-200">
          <h3 className="text-xl font-semibold mb-4 text-gray-700">Knowledge Base</h3>

          <label
            for="file"
            class="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer bg-gray-50 hover:bg-gray-100 transition"
          >
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg aria-hidden="true" class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6h.1a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12">
                </path>
              </svg>
              <p class="mb-2 text-sm text-gray-500">
                <span class="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p class="text-xs text-gray-400">PDF files only</p>
            </div>
            <input id="file" type="file" class="hidden" accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])} />
          </label>

          {file && (
          <p className="mt-3 text-sm text-gray-700 text-center">{file.name}</p>
        )}

 
          <button
            onClick={handleFileUpload}
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition font-medium mt-2"
          >
            Upload & Ingest
          </button>

          <h3 className="text-lg font-semibold mt-6 mb-2 text-gray-700">Indexed Documents</h3>
          <div className="max-h-48 overflow-y-auto border border-gray-300 rounded-lg p-3 bg-gray-50 text-sm">
            <ol>
              {documents.map((doc) => (
                <li key={doc.id}>{doc}</li>
              ))}
            </ol>
          </div>
        </div>

        {/* Right Panel */}
        <div className="flex-1 bg-white shadow-md rounded-2xl p-6 border border-gray-200 flex flex-col">
          <h3 className="text-xl font-semibold mb-4 text-gray-700">Ask Your PDFs</h3>

          {/* Input Bar */}
          <div className="flex mb-4">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Type your question here..."
              className="flex-1 p-3 border border-gray-300 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-green-400"
            />

            <button
              onClick={handleQuestionSubmission}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleQuestionSubmission();
                }
              }}
              className="px-6 bg-green-600 hover:bg-green-700 text-white rounded-r-xl transition font-medium"
            >
              ➤
            </button>
          </div>

          {/* Answer Box */}
          <div className="mt-4 text-gray-500 text-sm min-h-[40px]">{status}</div>

          <div className="flex-1 p-4 bg-gray-100 border border-gray-300 rounded-xl overflow-auto text-sm leading-relaxed text-left">
            <ReactMarkdown remarkPlugins={[remarkGfm, remarkBreaks]}>
              {answer}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
