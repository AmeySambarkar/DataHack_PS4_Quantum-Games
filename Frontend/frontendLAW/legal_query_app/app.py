import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
from flask import Flask, render_template, request, jsonify
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import HuggingFaceHub
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from tempfile import NamedTemporaryFile

app = Flask(__name__)

# Initialize the backend components
embeddings = HuggingFaceEmbeddings()
llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 1, "max_length": 1000000})
qa = None  # Initialize with no retriever

# Define the home route
@app.route("/")
def home():
    return render_template("index.html")

# Define an endpoint to handle PDF upload
@app.route("/upload", methods=["POST"])
def upload_document():
    global qa  # Use the global variable
    if "pdf-upload" in request.files:
        pdf_file = request.files["pdf-upload"]

        if pdf_file and pdf_file.filename.endswith(".pdf"):
             # Save the uploaded PDF file to a temporary file
            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                pdf_file.save(temp_file.name)

                # Load the PDF from the temporary file
                loader = PyPDFLoader(temp_file.name)
            # Load the uploaded PDF file
                pages = loader.load_and_split()
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1024,
                    chunk_overlap=64,
                    separators=['\n\n', '\n', '(?=>\. )', ' ', '']
                  )
                pdf_docs = text_splitter.split_documents(pages)

            # Set up the QA chain with a retriever
                db = FAISS.from_documents(pdf_docs, embeddings)
                qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever(search_kwargs={"k": 3}))

            return jsonify({"message": "PDF uploaded and analyzed."})

    return jsonify({"error": "Invalid PDF upload"})

# Define an endpoint to handle the search query
@app.route("/query", methods=["POST"])
def query_document():
    if "search-query" in request.form:
        query = request.form["search-query"]

        if qa is not None:
            # Process the query
            answers = qa.run(query)

            return jsonify({"answers": answers})
        else:
            return jsonify({"error": "PDF not uploaded or analyzed"})

    return jsonify({"error": "Invalid query"})

if __name__ == "__main__":
    app.run(debug=True)
