import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Alpha Wear - Stock Management", layout="wide")

st.title("Alpha Wear - Stock Management System")
st.markdown("---")

# File path for permanent local storage
DATA_FILE = "stock_database.csv"


# Initialize database file if it doesn't exist
def init_db():
  if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(
        columns=[
            "PRODUCT TYPE",
            "COLOR",
            "SIZE",
            "QUANTITY",
            "PURCHASE PRICE",
            "SELL PRICE",
        ]
    )
    df.to_csv(DATA_FILE, index=False)


init_db()


# Function to load data
def load_data():
  try:
    return pd.read_csv(DATA_FILE)
  except Exception as e:
    return pd.DataFrame(
        columns=[
            "PRODUCT TYPE",
            "COLOR",
            "SIZE",
            "QUANTITY",
            "PURCHASE PRICE",
            "SELL PRICE",
        ]
    )


# Sidebar Form for Adding Stock
st.sidebar.header("Add New Product")

with st.sidebar.form("stock_form", clear_on_submit=True):
  category_input = st.selectbox("Category", ["Men", "Women", "Kids", "Unisex"])
  product_types = [
      "Shirt",
      "T-Shirt",
      "Polo Shirt",
      "Panjabi",
      "Lungi",
      "Pant",
      "Jacket",
  ]
  selected_type = st.selectbox("Product Type", product_types)
  custom_type = st.text_input("Or Type New Product Name", "")

  final_product = (
      custom_type.strip() if custom_type.strip() else selected_type
  )

  color_input = st.text_input("Color", "Black")
  size_input = st.text_input("Size", "M")
  quantity_input = st.number_input("Quantity", min_value=1, value=1, step=1)
  purchase_price = st.number_input(
      "Purchase Price", min_value=0.0, value=380.0
  )
  sell_price = st.number_input("Sell Price", min_value=0.0, value=690.0)

  submit_button = st.form_submit_button(label="Add to Stock")

  if submit_button:
    current_df = load_data()

    new_row = pd.DataFrame({
        "PRODUCT TYPE": [final_product],
        "COLOR": [color_input.upper()],
        "SIZE": [size_input.upper()],
        "QUANTITY": [quantity_input],
        "PURCHASE PRICE": [purchase_price],
        "SELL PRICE": [sell_price],
    })

    updated_df = pd.concat([current_df, new_row], ignore_index=True)
    updated_df.to_csv(DATA_FILE, index=False)

    st.sidebar.success(
        f"Successfully added {quantity_input}x {final_product}!"
    )
    st.rerun()

# Main Section: Display Stock Table
st.subheader("Current Stock Table")

stock_data = load_data()

if not stock_data.empty:
  st.dataframe(stock_data, use_container_width=True)
else:
  st.info("No stock data found. Use the sidebar to add products.")
