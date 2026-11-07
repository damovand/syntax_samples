
import pandas as pd

from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Sample data (replace with DB query or file read)
# Example DataFrame
'''
df = pd.DataFrame({
    "Name": ["Anurag", "Manjeet", "Shubham"],
    "Address": ["Patna", "Delhi", "Coimbatore"],
    "ID": [20123, 20124, 20145],
    "Sales": [140000, 300000, 600000]
})

items = [
    {"id": 1, "name": "Item A"},
    {"id": 2, "name": "Item B"},
    {"id": 3, "name": "Item C"},
    {"id": 4, "name": "Item W"},
    {"id": 5, "name": "Item X"},
    {"id": 6, "name": "Item Y"},
]
'''
if 'My_Movies_Detailed' in locals():
   print("DataFrame exists in locals")
elif 'My_Movies_Detailed' in globals():
   print("DataFrame exists in globals")
else:
    print("DataFrame does not exist")
    Movies = pd.read_csv("data/IMDB_top_1000_movie_sum_plot.csv")
    Owned_Movies = pd.read_csv("data/My Movies.csv")

    #Movies_merged = Movies.merge(Owned_Movies, on='Title', how='outer')
    Movies_merged = Owned_Movies.merge(Movies, on='Title', how='outer')

    My_Movies_Detailed = Movies_merged[Movies_merged['Title'].isin(Owned_Movies['Title'])]

    Movies_merged.to_csv('merged_Movies_Detailed.csv', encoding='utf-8', index=False)
    My_Movies_Detailed.to_csv('my_Movies_Detailed.csv', encoding='utf-8', index=False)
    #print(Movies_merged.head(5))
print(" ==== Final ===")
print(My_Movies_Detailed[['Title', 'Released_Year']].head(5))


@app.route("/")
def index():
    selected_columns = ['Title', 'Released_Year']
    info_columns = My_Movies_Detailed[selected_columns]
    table_html = info_columns.to_html(classes='table table-striped', index=False)
    return render_template("index.html", table=table_html)

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
