#importing libraries
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import tkinter as tk
from tkinter import filedialog, messagebox

class MovieRecommender:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommender")
        
        # Creating labels and entry box for movie name
        tk.Label(self.root, text="Enter your favourite movie name:").grid(row=0, column=0, padx=10, pady=10)
        self.movie_name_entry = tk.Entry(self.root, width=50)
        self.movie_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Creating button for selecting CSV file
        tk.Button(self.root, text="Select CSV file", command=self.load_data).grid(row=1, column=0, padx=10, pady=10)
        
        # Creating label for selected CSV file path
        self.csv_path_label = tk.Label(self.root, text="")
        self.csv_path_label.grid(row=1, column=1, padx=10, pady=10)
        
        # Creating button for recommending movies
        tk.Button(self.root, text="Recommend movies", command=self.recommend_movies).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # Initializing class variables
        self.movies_data = None
        self.selected_features = ['genres','keywords','tagline','cast','director']
        self.combined_features = None
        self.feature_vectors = None
        self.similarity = None
        self.list_of_all_titles = None
        
    def load_data(self):
        # Opening file dialog for selecting CSV file
        file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        if file_path:
            try:
                # Loading the data from the CSV file to a pandas dataframe
                self.movies_data = pd.read_csv(file_path)
                
                # Replacing the null values with empty strings
                if self.movies_data.isna().sum().sum() > 0:
                    self.movies_data.fillna('', inplace=True)

                    
                # Combining all the selected features
                self.combined_features = self.movies_data['genres']+' '+self.movies_data['keywords']+' '+self.movies_data['tagline']+' '+self.movies_data['cast']+' '+self.movies_data['director']
                
                # Converting the text data to feature vectors
                vectorizer = TfidfVectorizer()
                self.feature_vectors = vectorizer.fit_transform(self.combined_features)
                
                # Getting the similarity scores using cosine similarity
                self.similarity = cosine_similarity(self.feature_vectors)
                
                # Creating a list with all the movie names given in the dataset
                self.list_of_all_titles = self.movies_data['title'].tolist()
                
                # Updating CSV file path label
                self.csv_path_label.config(text=file_path)
            except:
                messagebox.showerror("Error", "An error occurred while loading the CSV file.")
        
    def recommend_movies(self):
        if self.movies_data is None:
            messagebox.showwarning("Warning", "Please select a CSV file first.")
            return
        
        # Getting the movie name from the user
        movie_name = self.movie_name_entry.get().strip()
        
        # Finding the close match for the movie name given by the user
        find_close_match = difflib.get_close_matches(movie_name, self.list_of_all_titles)
        if not find_close_match:
            messagebox.showwarning("Warning", "No close match found for the movie name. Please try again.")
            return
         # Getting the index of the closest match
        movie_index = self.list_of_all_titles.index(find_close_match[0])
        
        # Getting the similarity scores for the selected movie
        movie_similarities = list(enumerate(self.similarity[movie_index]))
        
        # Sorting the similarity scores in descending order
        sorted_similarities = sorted(movie_similarities,key=lambda x:x[1],reverse=True)[1:]
        
        # Getting the top 10 similar movies
        top_similar_movies = []
        for i in range(10):
            movie_index = sorted_similarities[i][0]
            top_similar_movies.append(self.list_of_all_titles[movie_index])
        
        # Displaying the top 10 similar movies in a message box
        messagebox.showinfo("Recommended Movies", "\n".join(top_similar_movies))

root = tk.Tk()
recommender=MovieRecommender(root)
root.mainloop()