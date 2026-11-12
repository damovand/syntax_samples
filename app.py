
import pandas as pd

from omdbapi.movie_search import GetMovie
from pprint import pprint
import requests
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os
import get_movie
app = Flask(__name__)
load_dotenv()
api_key = os.getenv("OMDB_API_KEY")

# Sample data (replace with DB query or file read)
# Example DataFrame
def merge_movie_data():
    try:
        if 'My_Movies_Detailed' in locals():
            print("DataFrame exists in locals")
        elif 'My_Movies_Detailed' in globals():
            print("DataFrame exists in globals")
        else:
            print("DataFrame does not exist")
            Movies = pd.read_csv("data/IMDB_top_1000_movie_sum_plot.csv")
            Owned_Movies = pd.read_csv("data/My Movies.csv")
    except FileNotFoundError as e:
        print(f"Error loading data === Fix the error: {e}") 
        exit()  
    finally: 
        print("Finished loading data")

    # merge the two DataFrames on 'Title' to grab details from downloaded(from hugging face) movies dataset
    Movies_merged = Owned_Movies.merge(Movies, on='Title', how='outer')
    # filter the merged DataFrame to only include movies that are in the Owned_Movies DataFrame
    My_Movies_Detailed = Movies_merged[Movies_merged['Title'].isin(Owned_Movies['Title'])]
    #Movies_merged.to_csv('merged_Movies_Detailed.csv', encoding='utf-8', index=False)
    # save the filtered DataFrame to a CSV file for future use in jupyter notebook
    My_Movies_Detailed.to_csv('data/my_Movies_Detailed.csv', encoding='utf-8', index=False)
    #print(Movies_merged.head(5))
    '''
    movie_details_missing = My_Movies_Detailed[(My_Movies_Detailed["Released_Year"].isna()) &
        (My_Movies_Detailed["Genre"].isna()) &
        (My_Movies_Detailed["Star1"].isna()) &
        (My_Movies_Detailed["Director"].isna()) ]
    movie_details_missing.to_csv('movie_details_missing.csv', encoding='utf-8', index=False)
    print(" ==== Final ===")
    '''
    print(My_Movies_Detailed[['Title', 'Released_Year']].head(5))

try:
    My_Movies_Detailed = pd.read_csv('data/my_Movies_Detailed.csv')
except FileNotFoundError:
    merge_movie_data()
    My_Movies_Detailed = pd.read_csv('data/my_Movies_Detailed.csv')
# Convert DataFrame to list of dicts for Jinja2

@app.route("/")
def index():
    # Convert DataFrame to list of dicts for Jinja2
    selected_columns = ['Title', 'Released_Year']
    info_columns = My_Movies_Detailed[selected_columns]
    show_columns = info_columns.columns.tolist()
    table_data = info_columns.to_dict(orient="records")

    return render_template("index.html", columns=show_columns, rows=table_data)

@app.route("/omdb_details", methods=["GET"])
def omdb_details():
    API_KEY = api_key
    '''
    mask = (My_Movies_Detailed['Title'] == 'foo') & (My_Movies_Detailed['Released_Year'] == 'one')
    filtered = My_Movies_Detailed.loc[mask]  # label-based selection
    row_index = My_Movies_Detailed.index[mask].tolist()
    print(row_index[0])
    
    '''
    # Extract parameters safely
    param1 = request.args.get('title', default=None, type=str)  # default=None if missing
    param2 = request.args.get('year', default=None, type=str)     # default=0 if missing

    # Handle missing parameters
    if param1 is None:
        return {"error": "param1 is required"}, 400
    
    MOVIE_TITLE = param1
    MOVIE_YEAR = param2
    print("----- look for movie:  ", MOVIE_TITLE, "  AND YEAR ",MOVIE_YEAR)
    #MOVIE_TITLE = "A Haunting in Venice"
    #MOVIE_TITLE = "A.I. Artificial Intelligence"
    # Run the test
    response = get_movie.omdb_movie_details(API_KEY, MOVIE_TITLE, MOVIE_YEAR)
    print(" == Done! ==============")
    return response
    
@app.route("/omdb_bulk_update")
def omdb_bulk_update():
    try:
        My_Movies_Detailed = pd.read_csv('data/my_Movies_Detailed.csv')
    except FileNotFoundError:
        merge_movie_data()
    
    get_movie.bulk_update_movie(My_Movies_Detailed)
    
    return redirect(url_for("index"))

@app.route("/add")
def add_item():
    return redirect(url_for("index"))  # placeholder; could POST to add

@app.route("/bulk_load", methods=["POST"])
def bulk_load():
    # Example: read CSV from request file
    if "csv_file" in request.files:
        file = request.files["csv_file"]
        if file.filename:
            with file.stream() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # process row (e.g., append to DB)
                    pass
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8040, debug=True)
