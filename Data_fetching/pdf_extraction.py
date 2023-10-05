import spacy
from spacy.matcher import Matcher

import os
import glob

from PyPDF2 import PdfReader
import json

class ResumeParser:
    def __init__(self, pdf_folder):
        self.pdf_folder = pdf_folder
        self.nlp = spacy.load("en_core_web_lg")
        self.matcher = Matcher(self.nlp.vocab)
        self.define_matcher_patterns()

    def define_matcher_patterns(self):
        # Define a list of job title keywords
        job_title_keywords = ["TUTORING", "CONSULTANT", "job", "category", "role", "engineer", "developer", "analyst",
                              "manager", "designer", "scientist", "accountant", "hr", "trainer",
                              "accountant", "advocate", "agriculture", "apparel", "artist", "automobile",
                              "aviation", "banking", "bpo", "call center", "business development",
                              "chef", "construction", "consultant", "designer", "digital-media",
                              "digital marketing", "engineering", "finance", "financial", "fitness",
                              "healthcare", "human resource", "information technology", "public relations",
                              "sales", "teacher"]

        job_role_pattern = [{"LOWER": {"in": job_title_keywords}}, {"POS": "NOUN"}]
        self.matcher.add("job_role", [job_role_pattern])

        skills_pattern = [{"POS": {"in": ["NOUN", "PROPN"]}}]
        self.matcher.add("skills", [skills_pattern])

    def extract_text_from_pdf(self, pdf_file):
        with open(pdf_file, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

    def extract_keywords(self, resume_text):
        doc = self.nlp(resume_text)
        matches = self.matcher(doc)

        job_role = "Unknown"
        skills = []

        for match_id, start, end in matches:
            match_text = doc[start:end].text
            if self.nlp.vocab.strings[match_id] == 'job_role':
                job_role = match_text
            if self.nlp.vocab.strings[match_id] == 'skills':
                skills.append(match_text)

        return job_role, skills

    def extract_education(self, resume_text):
        doc = self.nlp(resume_text)

        degree = "Unknown"
        institution_names = []

        # Define keywords for education entity recognition
        education_keywords = ["bachelor's", "master's", "phd", "diploma", "degree",
                              "institute", "university", "college"]

        for token in doc:
            if token.text.lower() in education_keywords:
                # Collect words following the education keywords as the degree
                degree = " ".join([t.text for t in token.subtree if not t.is_punct])
                # Break after finding the first degree

        # Extract educational institution names
        for ent in doc.ents:
            if ent.label_ == "ORG":
                org_name = ent.text
                if "college" in org_name.lower() or "university" in org_name.lower():
                    institution_names.append(org_name)

        if not institution_names:
            institution_names.append("Unknown")

        return degree, institution_names

    def process_resumes(self):
        pdf_files = glob.glob(os.path.join(self.pdf_folder, "*.pdf"))
        parsed_resume = []

        for pdf_file in pdf_files:
            resume_text = self.extract_text_from_pdf(pdf_file)
            job_role, skills = self.extract_keywords(resume_text)
            degree, institution_names = self.extract_education(resume_text)

            parsed_resume.append({
                "File": os.path.basename(pdf_file),
                "Category (Job Role)": job_role,
                "Skills": skills,
                "Education": {"Degree": degree, "Institution Names": institution_names}})

        return parsed_resume

if __name__ == "__main__":
    # Root folder containing subfolders with PDFs
    root_folder = r'C:\Users\ideapad\Desktop\ats\data\data'
    
    # Output folder for JSON and text files
    output_folder = r"C:\Users\ideapad\Desktop\ats\data\output_folder"
    os.makedirs(output_folder, exist_ok=True)

    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            resume_parser = ResumeParser(subfolder_path)
            parsed_resume = resume_parser.process_resumes()

            # Create a subfolder for each subfolder in the output directory
            subfolder_output_folder = os.path.join(output_folder, subfolder)
            os.makedirs(subfolder_output_folder, exist_ok=True)

            for resume in parsed_resume:
                output_text_file = os.path.join(subfolder_output_folder, f"{resume['File']}.txt")
                with open(output_text_file, "w", encoding="utf-8") as text_file:
                    text_file.write(f"Category (Job Role): {resume['Category (Job Role)']}\n")
                    text_file.write(f"Skills: {', '.join(resume['Skills'])}\n")
                    text_file.write(f"Education: Degree - {resume['Education']['Degree']}\n")
                    text_file.write(f"Institution Names: {', '.join(resume['Education']['Institution Names'])}\n")










