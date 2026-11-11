import pandas as pd

def load_and_wrangled_data(file_path: str) -> pd.DataFrame:
    """
    Loads CSV data, cleans it, and returns a wrangled DataFrame.
    """
    try:
        # Load CSV
        df = pd.read_csv(file_path)

        # Example wrangling: remove duplicates, fill missing values
        df = df.drop_duplicates()
        df = df.fillna({"Released_Year": "default_value"})  # Replace NaNs

        # Example transformation: create a new column
        if "price" in df.columns and "quantity" in df.columns:
            df["total"] = df["price"] * df["quantity"]

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty.")
    except Exception as e:
        raise RuntimeError(f"Error processing data: {e}")

