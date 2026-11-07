from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Category": ["A", "B", "A", "C"],
    "Score": [85, 90, 78, 92]
}
df = pd.DataFrame(data)

@app.route('/')
def test():
    # Get optional filter parameter from query string
    category = request.args.get('category')

    # Filter DataFrame if parameter is provided
    if category:
        filtered_df = df[df["Category"] == category]
    else:
        filtered_df = df

    # Convert DataFrame to list of dicts for Jinja2
    table_data = filtered_df.to_dict(orient="records")
    columns = filtered_df.columns.tolist()

    return render_template("table.html", columns=columns, rows=table_data, category=category)

if __name__ == '__main__':
    app.run(debug=True)
