from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
from doc_processor import process_pdf, save_uploaded_file, cleanup_temp_file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chats
legal_chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "👋 Greetings! I'm your Indian legal assistant. I can help you with questions about Indian law and legal matters. How may I assist you today?"}
    ]
)

doc_chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are a legal document analysis expert. Your task is to analyze legal documents and answer questions about them."},
        {"role": "model", "parts": "I understand. I'll help analyze legal documents and answer questions about their content."}
    ]
)

court_cases_chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are an expert on Indian court cases, particularly landmark and significant cases. Your task is to provide accurate information about these cases."},
        {"role": "model", "parts": "I understand. I'll help provide detailed information about Indian court cases, their rulings, and significance."}
    ]
)

class ChatMessage(BaseModel):
    message: str

def is_greeting(text: str) -> bool:
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste"]
    return any(greeting in text.lower() for greeting in greetings)

def is_legal_query(response: str) -> bool:
    legal_keywords = ["law", "legal", "act", "court", "rights", "crime", "section", "penalty", 
                     "contract", "jurisdiction", "justice", "indian", "constitution"]
    return any(keyword in response.lower() for keyword in legal_keywords)

def format_response(text: str) -> str:
    """Format the response with proper HTML structure and improved styling."""
    import html
    formatted_text = html.escape(text)

    # Convert markdown-style bold to HTML bold
    formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", formatted_text)

    # Convert numbered lists
    formatted_text = re.sub(r"(?:^|\n)(\d+\. .+?)(?=\n|$)", lambda m: '<ol>' + ''.join(f'<li>{item[3:]}</li>' for item in m.group(1).split('\n') if item.strip()) + '</ol>', formatted_text, flags=re.MULTILINE)

    # Convert bullet lists
    formatted_text = re.sub(r"(?:^|\n)(\* .+?)(?=\n|$)", lambda m: '<ul>' + ''.join(f'<li>{item[2:]}</li>' for item in m.group(1).split('\n') if item.strip()) + '</ul>', formatted_text, flags=re.MULTILINE)

    # Convert inline code
    formatted_text = re.sub(r"`([^`]+)`", r"<code>\1</code>", formatted_text)

    # Convert code blocks
    formatted_text = re.sub(r"```([\s\S]+?)```", r"<pre><code>\1</code></pre>", formatted_text)

    # Convert newlines to <br> for paragraphs
    formatted_text = re.sub(r"\n{2,}", "<br><br>", formatted_text)
    formatted_text = re.sub(r"\n", "<br>", formatted_text)

    return formatted_text

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_with_bot(message: ChatMessage):
    user_input = message.message.strip()
    
    if not user_input:
        return JSONResponse({"error": "No input provided"}, status_code=400)
    
    # Handle greetings specially
    if is_greeting(user_input):
        return JSONResponse({
            "response": "👋 <strong>Hello!</strong> I'm your Indian legal assistant. How can I help you with your legal questions today?"
        })
    
    try:
        response = legal_chat.send_message(user_input)
        
        if is_legal_query(response.text):
            formatted_response = format_response(response.text)
            # Add emphasis to important legal terms
            legal_terms = ["act", "section", "article", "law", "court", "rights", "constitution"]
            for term in legal_terms:
                formatted_response = re.sub(
                    f"\\b{term}\\b",
                    f"<strong>{term}</strong>",
                    formatted_response,
                    flags=re.IGNORECASE
                )
            return JSONResponse({"response": formatted_response})
        else:
            return JSONResponse({
                "response": "<strong>Note:</strong> I specialize in Indian legal matters. Please ask me questions related to Indian law and legal system."
            })
    except Exception as e:
        return JSONResponse({
            "error": "❌ An error occurred while processing your request. Please try again."
        }, status_code=500)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return JSONResponse({
            "error": "Please upload a PDF file."
        }, status_code=400)
    
    try:
        # Save uploaded file
        temp_path = save_uploaded_file(file)
        
        # Process the PDF
        text = process_pdf(temp_path)
        
        # Clean up temporary file
        cleanup_temp_file(temp_path)
        
        # Generate summary using Gemini
        summary_prompt = f"Please provide a concise summary of this legal document, highlighting the key points and important sections:\n\n{text[:5000]}"
        summary = doc_chat.send_message(summary_prompt).text
        
        return JSONResponse({
            "summary": format_response(summary),
            "success": True
        })
    except Exception as e:
        return JSONResponse({
            "error": f"Error processing document: {str(e)}"
        }, status_code=500)

@app.post("/doc-chat")
async def chat_about_document(message: ChatMessage):
    try:
        response = doc_chat.send_message(message.message)
        return JSONResponse({
            "response": format_response(response.text)
        })
    except Exception as e:
        return JSONResponse({
            "error": "Error processing your question. Please try again."
        }, status_code=500)

@app.post("/case-chat")
async def chat_about_case(message: ChatMessage):
    try:
        response = court_cases_chat.send_message(f"""Analyze this query about an Indian court case: '{message.message}'
        
        If it's about a specific case, respond in this format:
        
        [Brief introduction confirming the case]
        
        Background and Facts:
        • [Key fact 1]
        • [Key fact 2]
        • [Continue with relevant facts]
        
        Court Ruling:
        • [Main ruling points]
        • [Sentences given]
        • [Appeals and final outcome]
        
        Impact and Legacy:
        • [Major changes in law]
        • [Social impact]
        • [Long-term significance]
        
        Keep the response conversational and well-formatted without excessive bold text.
        If it's not a specific case or unclear, ask for clarification and suggest relevant landmark cases.""")
        
        formatted_response = format_response(response.text)
        
        # Add emphasis to only important legal terms
        legal_terms = ["Supreme Court", "High Court", "verdict", "judgment"]
        for term in legal_terms:
            formatted_response = re.sub(
                f"\\b{term}\\b",
                f"<strong>{term}</strong>",
                formatted_response,
                flags=re.IGNORECASE
            )
        
        return JSONResponse({
            "response": formatted_response
        })
    except Exception as e:
        return JSONResponse({
            "error": "Error processing your question about the court case. Please try again."
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)