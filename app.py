
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

    #Movies_merged = Movies.merge(Owned_Movies, on='Title', how='outer')
Movies_merged = Owned_Movies.merge(Movies, on='Title', how='outer')

My_Movies_Detailed = Movies_merged[Movies_merged['Title'].isin(Owned_Movies['Title'])]

Movies_merged.to_csv('merged_Movies_Detailed.csv', encoding='utf-8', index=False)
My_Movies_Detailed.to_csv('my_Movies_Detailed.csv', encoding='utf-8', index=False)
#print(Movies_merged.head(5))

movie_details_missing = My_Movies_Detailed[(My_Movies_Detailed["Released_Year"].isna()) &
(My_Movies_Detailed["Genre"].isna()) &
(My_Movies_Detailed["Star1"].isna()) &
(My_Movies_Detailed["Director"].isna()) ]

print(" ==== Final ===")
print(My_Movies_Detailed[['Title', 'Released_Year']].head(5))

movie_details_missing.to_csv('movie_details_missing.csv', encoding='utf-8', index=False)

# Convert DataFrame to list of dicts for Jinja2

@app.route("/")
def index():
    # Convert DataFrame to list of dicts for Jinja2
    selected_columns = ['Title', 'Released_Year']
    info_columns = My_Movies_Detailed[selected_columns]
    show_columns = info_columns.columns.tolist()
    table_data = info_columns.to_dict(orient="records")

    return render_template("index.html", columns=show_columns, rows=table_data)

@app.route("/OMDBAPI")
def omdb_details():
    API_KEY = api_key
    MOVIE_TITLE = "Exorcist"
    MOVIE_YEAR = "1973"
    #MOVIE_TITLE = "A Haunting in Venice"
    #MOVIE_TITLE = "A.I. Artificial Intelligence"
    # Run the test
    response = get_movie.omdb_movie_details(API_KEY, MOVIE_TITLE, MOVIE_YEAR)
    print(" ================ Returned to the main program ==============")
    return response
    


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
