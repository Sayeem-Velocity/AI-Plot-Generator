import streamlit as st
import pandas as pd
from plot_generator import generate_plot

st.set_page_config(page_title="📊 AI Plot Generator", layout="wide")

st.title("📊 AI Plot Generator")
st.markdown("Upload a spreadsheet (.csv, .xls, .xlsx), choose your plot type, and export it as an image!")

# Upload file
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "xlsx"])

if uploaded_file:
    try:
        # File reading logic based on file extension
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file type")

        st.success(f"Loaded `{uploaded_file.name}` successfully!")
        st.write("Preview of the Data:")
        st.dataframe(df.head())

        chart_type = st.selectbox("Select Plot Type", [
            "Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Pie Chart"
        ])

        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        all_columns = df.columns.tolist()

        x_col = st.selectbox("X-axis Column", all_columns)
        y_col = st.selectbox("Y-axis Column", numeric_columns)

        output_format = st.selectbox("Download Format", ["png", "jpg", "jpeg"])

        if st.button("Generate Plot"):
            buf = generate_plot(df, x_col, y_col, chart_type, output_format)

            st.image(buf, caption="Generated Plot", use_column_width=True)

            st.download_button(
                label="📥 Download Plot",
                data=buf,
                file_name=f"plot.{output_format}",
                mime=f"image/{output_format}"
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a CSV or Excel file to begin.")
