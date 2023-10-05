import os
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    def __init__(self, job_description_folder, cv_folder, output_folder):
        self.job_description_folder = job_description_folder
        self.cv_folder = cv_folder
        self.output_folder = output_folder

        os.makedirs(self.output_folder, exist_ok=True)

    def load_embeddings(self, folder):
        embeddings = {}
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".npy"):
                    embedding = np.load(os.path.join(root, file))
                    key = os.path.splitext(file)[0]  # Remove file extension from the key
                    embeddings[key] = embedding.tolist()  # Convert NumPy array to Python list
        return embeddings

    def match_candidates_to_jobs(self):
        # Load embeddings for job descriptions and CVs
        job_description_embeddings = self.load_embeddings(self.job_description_folder)
        cv_embeddings = self.load_embeddings(self.cv_folder)

        # Match CVs to job descriptions and rank based on similarity
        result_data = {}
        for job_name, job_embedding in job_description_embeddings.items():
            similarities = cosine_similarity([job_embedding], list(cv_embeddings.values()))
            ranked_indices = np.argsort(similarities[0])[::-1]  # Sort in descending order
            top_candidates = [{"CV_File": list(cv_embeddings.keys())[j], "Similarity": similarities[0][j]} for j in ranked_indices[:5]]
            result_data[job_name] = {
                "Top_Candidates": top_candidates
            }

        # Save the results as JSON
        output_json_path = os.path.join(self.output_folder, 'candidate_job_matching_results.json')
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(result_data, json_file, ensure_ascii=False, indent=4)

        return result_data

if __name__ == "__main__":
    job_description_folder = r"C:\Users\ideapad\Desktop\ats\data\JD_Wordembeddings"
    cv_folder = r"C:\Users\ideapad\Desktop\ats\data\wordembedded_resume"
    output_folder = r"C:\Users\ideapad\Desktop\ats\data\matching results"

    matcher = JobMatcher(job_description_folder, cv_folder, output_folder)

    # Match candidates to jobs and get the top 5 CVs for each job description
    matching_results = matcher.match_candidates_to_jobs()

    # Print or process the matching results as needed
    print(matching_results)