from fastapi import FastAPI , Query ,UploadFile ,File , HTTPException
from io import BytesIO
from google import genai
from google.genai import types
from dotenv import load_dotenv
import PyPDF2
import docx

load_dotenv()
client = genai.Client()

app = FastAPI()


@app.get("/")
def home():
    return{"message" : "Text Summarization api"}


@app.get("/summarization")
def summarization(text: str = Query(..., description="Text to summarize")):
     prompt = "Summarize the following text:\n" + text
     response = client.models.generate_content(model = 'gemini-2.0-flash' , contents=prompt ,config = types.GenerateContentConfig(temperature=0.1 , top_k=1 , top_p = 0.6))
     return {"original_text": text, "summary": response.text}

def extract_text_from_pdf(file_bytes : bytes)->str:
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text =""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_doc(file_bytes : bytes)->str:
    doc = docx.Document(BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(file_bytes : bytes) -> str:
    return file_bytes.decode('utf-8')


@app.post("/read-doc/")
async def read_doc(file : UploadFile =File(...)):
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(content)
    elif filename.endswith('.docx'):
        text = extract_text_from_doc(content)
    elif filename.endswith('.txt'):
        text = extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400 , detail = "Unsupported file format. Please upload PDF, DOCX, or TXT.")
    
    
    prompt = "Summarize the following text:\n" + text
    response = client.models.generate_content(model = 'gemini-2.0-flash' , contents=prompt ,config = types.GenerateContentConfig(temperature=0.1 , top_k=1 , top_p = 0.6))
    return {"original_text": text, "summary": response.text}

