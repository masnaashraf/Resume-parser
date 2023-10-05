import os
from datasets import load_dataset
import json
import re

class FetchData():
    def __init__(self,jobdescription_link):
        self.data_link=jobdescription_link
        self.dataset=self.download_dataset()
        self.data_folder=r"C:\Users\ideapad\Desktop\ats\data\job_description_folder"

        # Create the output folder if it does not exist
        os.makedirs(self.data_folder, exist_ok=True)

    def download_dataset(self):
        dataset=load_dataset(self.data_link)
        return dataset
    
    def job_description(self):
        return self.dataset['train']['job_description']
    

    def company_name(self):
        return self.dataset['train']['company_name']
    
    def position_titles(self):
        return self.dataset['train']['position_title']
    

    def clean_filenames(self,filename):
        # Remove characters that are not safe in filenames

        cleaned_filename=re.sub(r'[\/:*?"<>|]', '_', filename)
        return cleaned_filename
    
    def save_job_desc_as_text(self):
        company_name=self.company_name()

        job_desc=self.job_description()
        position_titles=self.position_titles()

        for i ,desc in enumerate(job_desc):
            if i < len(company_name):
                current_company_name = self.clean_filenames(company_name[i])
            else:
                current_company_name = "NoCompany"  # Use a default value when there is no company name
            position_title = position_titles[i]
            clean_pos_title = self.clean_filenames(position_title)

            output_filename = f"{current_company_name}_{clean_pos_title}.txt"
            output_path = os.path.join(self.data_folder, output_filename)
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(desc)

    
    def save_job_desc_as_json(self):
        company_name = self.company_name()
        job_desc = self.job_description()
        position_titles = self.position_titles()

        for i, desc in enumerate(job_desc):
            if i < len(company_name):
                current_company_name = self.clean_filenames(company_name[i])
            else:
                current_company_name = "NoCompany"  # Use a default value when there is no company name
            position_title = position_titles[i]
            clean_pos_title = self.clean_filenames(position_title)

            output_filename = f"{current_company_name}_{clean_pos_title}.json"
            output_path = os.path.join(self.data_folder, output_filename)

            job_desc_dict = {"job_description": desc}
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(job_desc_dict, json_file, ensure_ascii=False, indent=4)
    




    def print_job_desc(self):
        job_desc=self.job_description()
        for i, desc in enumerate(job_desc):
            print(f"Job Description {i + 1}:")
            print("\n")
            print(desc)
            print("\n")






if __name__=="__main__":
    data= FetchData("jacob-hugging-face/job-descriptions")

     # Print job descriptions
    data.print_job_desc()

     # Save job descriptions as text and JSON files with sanitized position titles as filenames
    data.save_job_desc_as_text()
    data.save_job_desc_as_json()