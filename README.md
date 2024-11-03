# Resume Skill Matcher

A Streamlit-based web application that analyzes the match between a job description and a resume using GPT-4. The app extracts skills from both documents and provides detailed matching analysis, helping job seekers understand how well their skills align with job requirements.


## Features

- 🔍 Skill extraction from both resume and job description
- 📊 Percentage match calculation
- ✅ Identification of matching skills
- ❌ Highlights missing required skills
- 📚 Lists additional skills from your resume
- 🎯 Real-time analysis using GPT-4
- 🔒 Secure API key handling

## Installation

1. Create a Python 3.10 environment:
```bash
conda create -n skill_matcher python=3.10
conda activate skill_matcher
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-skill-matcher.git
cd resume-skill-matcher
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/)

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. In the web interface:
   - Enter your OpenAI API key in the sidebar
   - Paste your resume in the left text area
   - Paste the job description in the right text area
   - Click "Analyze Skills Match"

## Requirements

- Python 3.10+
- OpenAI API key
- Required packages (see requirements.txt):
  - langchain-community
  - langchain
  - pydantic
  - streamlit
  - openai
  - typing-extensions

## How It Works

1. The application uses GPT-4 through the OpenAI API to analyze both the resume and job description
2. Skills are extracted from both documents
3. The system compares the skills and categorizes them into:
   - Matched skills (present in both documents)
   - Missing skills (required but not in resume)
   - Additional skills (in resume but not required)
4. A match percentage is calculated based on the requirements met

## Privacy

- API keys are not stored and are cleared when the page is refreshed
- Documents are processed in memory and are not stored
- All analysis is done through secure API calls to OpenAI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the wonderful web framework
- Langchain for the LLM integration tools

