from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import streamlit as st
import json

class SkillMatch(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    match_percentage: float

class SkillMatchAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0,
            api_key=api_key,
            model="gpt-4"  # Using GPT-4 for more reliable JSON formatting
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a JSON-only response bot. You must ONLY return a properly formatted JSON object.
             DO NOT include any explanations, notes, or other text before or after the JSON.
             The JSON must contain exactly these keys: matched_skills, missing_skills, additional_skills, and match_percentage."""),
            ("human", """Extract skills from this job description and resume:

Job Description:
{job_description}

Resume:
{resume}

Return a JSON object with these exact keys:
- matched_skills (array of strings): skills present in both
- missing_skills (array of strings): skills in job description but missing from resume
- additional_skills (array of strings): skills in resume but not required in job description
- match_percentage (number): percentage of job requirements matched

RESPOND WITH ONLY THE JSON OBJECT.""")
        ])

    def analyze_skills(self, job_description: str, resume: str) -> SkillMatch:
        messages = self.prompt.format_messages(
            job_description=job_description,
            resume=resume
        )
        
        try:
            response = self.llm.invoke(messages)
            raw_response = response.content
            
            # Debug: Show the raw response
            st.write("Raw response from LLM:")
            st.code(raw_response, language='json')
            
            # Force the response into proper JSON format
            try:
                # Try direct JSON parsing first
                parsed_response = json.loads(raw_response)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the response
                start_idx = raw_response.find('{')
                end_idx = raw_response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = raw_response[start_idx:end_idx]
                    parsed_response = json.loads(json_str)
                else:
                    raise ValueError("Could not find valid JSON in response")

            # Create SkillMatch object
            result = SkillMatch(
                matched_skills=parsed_response['matched_skills'],
                missing_skills=parsed_response['missing_skills'],
                additional_skills=parsed_response['additional_skills'],
                match_percentage=float(parsed_response['match_percentage'])
            )
            return result
            
        except Exception as e:
            st.error(f"Error details: {str(e)}")
            st.error(f"Raw response was: {raw_response}")
            raise

def main():
    st.set_page_config(page_title="Resume Skill Matcher", layout="wide")
    st.title("Resume Skill Matcher")

    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        st.caption("Your API key is not stored and will be cleared when you refresh the page.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume")
        resume = st.text_area("", placeholder="Paste your resume here...", height=400)

    with col2:
        st.subheader("Job Description")
        job_description = st.text_area("", placeholder="Paste the job description here...", height=400)

    if st.button("Analyze Skills Match"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        elif not resume or not job_description:
            st.error("Please provide both resume and job description.")
        else:
            with st.spinner("Analyzing skills match..."):
                try:
                    agent = SkillMatchAgent(api_key)
                    result = agent.analyze_skills(job_description, resume)
                    
                    st.subheader("Skills Analysis")
                    
                    match_color = 'green' if result.match_percentage >= 70 else 'orange' if result.match_percentage >= 50 else 'red'
                    st.markdown(f"### Match Percentage: <span style='color:{match_color}'>{result.match_percentage:.1f}%</span>", 
                              unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### ✅ Matched Skills")
                        for skill in sorted(result.matched_skills):
                            st.markdown(f"- {skill}")
                    
                    with col2:
                        st.markdown("#### ❌ Missing Skills")
                        for skill in sorted(result.missing_skills):
                            st.markdown(f"- {skill}")
                    
                    with col3:
                        st.markdown("#### 📚 Additional Skills")
                        for skill in sorted(result.additional_skills):
                            st.markdown(f"- {skill}")

                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()

