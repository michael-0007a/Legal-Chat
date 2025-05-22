# LegalChat: AI-Powered Legal Assistant

LegalChat is an advanced legal assistant platform designed to provide instant access to Indian legal information, document analysis, and case exploration through AI-powered interactions.

## Features

### 1. Legal Consultation
- Real-time legal query responses
- Access to Indian law information
- Context-aware legal guidance
- Natural language understanding

### 2. Document Analysis
- PDF document processing
- Legal document summarization
- Key points extraction
- Interactive document Q&A

### 3. Court Case Explorer
- Access to landmark Indian cases
- Detailed case analysis
- Historical context and impact
- Precedent exploration

## Technical Stack

### Frontend
- HTML5/CSS3
- JavaScript (Vanilla)
- Responsive Design
- Glassmorphism UI

### Backend
- FastAPI
- Google Gemini AI
- PyPDF2 for document processing
- Jinja2 templating

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/legalchat.git
cd legalchat
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file and add:
```
API_KEY=your_gemini_api_key
```

5. Run the application:
```bash
uvicorn app:app --reload
```

## Project Structure

```
legalchat/
├── app.py                 # Main FastAPI application
├── static/               # Static files
│   ├── styles.css       # CSS styles
│   ├── video.mp4        # Background video
│   └── icon.png         # Favicon
├── templates/           # HTML templates
│   └── index.html      # Main page template
├── doc_processor.py     # Document processing utilities
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Features in Detail

### Legal Consultation
The platform provides instant responses to legal queries using the Gemini AI model, trained on Indian legal context. It can handle questions about:
- Constitutional law
- Criminal law
- Civil law
- Family law
- Property law
- Corporate law

### Document Analysis
Users can upload legal documents for AI-powered analysis:
- Automatic summarization
- Key points extraction
- Interactive Q&A about the document
- Support for PDF format

### Court Case Explorer
Explore landmark Indian court cases:
- Detailed case backgrounds
- Court rulings and judgments
- Impact and significance
- Historical context

## Security Features

- End-to-end encryption for communications
- Secure document processing
- No permanent storage of personal information
- Regular security audits
- Compliance with data protection regulations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support:
- Email: michaelBenedict0007b@gmail.com
- Phone: +91 7207420835
- Location: Anurag University, Venkatapur, Ghatkesar Rd, Hyderabad, Telangana 500088 