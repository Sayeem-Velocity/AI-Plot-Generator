import streamlit as st
import pandas as pd
from plot_generator import generate_plot

st.set_page_config(page_title="📊 Smart Plot Generator", layout="wide")

st.title("📊 Smart Plot Generator")
st.markdown("Upload a spreadsheet (.csv, .xls, .xlsx), choose your plot type and customizations, and export it as an image!")

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xls", "xlsx"])

if uploaded_file:
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
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

        x_col = st.multiselect("Select X-axis Column(s)", all_columns)
        y_col = st.multiselect("Select Y-axis Column(s)", numeric_columns)

        title = st.text_input("Chart Title", "My Plot")
        xlabel = st.text_input("X-axis Label", x_col[0] if x_col else "")
        ylabel = st.text_input("Y-axis Label", y_col[0] if y_col else "")
        legend = st.checkbox("Show Legend", value=True)
        color = st.color_picker("Pick a color", "#1f77b4")

        if st.button("Generate Plot"):
            buf = generate_plot(df, x_col, y_col, chart_type, color=color, title=title, xlabel=xlabel, ylabel=ylabel, legend=legend)
            st.image(buf, caption="Generated Plot", use_container_width=True)

            st.download_button(
                label="📥 Download Plot",
                data=buf,
                file_name="plot.png",
                mime="image/png"
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a CSV or Excel file to begin.")

st.markdown("""
---
<div style='text-align: center; color: white;'>
    <a href="https://github.com/Sayeem-Velocity" target="_blank" style="text-decoration: none;">
        <img src="https://img.icons8.com/ios-filled/24/ffffff/github.png" alt="GitHub" style="margin-right: 10px;"/>
    </a>
    <a href="https://www.linkedin.com/in/s-m-shahriar-56a263178/" target="_blank" style="text-decoration: none;">
        <img src="https://img.icons8.com/ios-filled/24/ffffff/linkedin.png" alt="LinkedIn" style="margin-right: 10px;"/>
    </a>
    <a href="mailto:sayeem26s@gmail.com" style="text-decoration: none;">
        <img src="https://img.icons8.com/ios-filled/24/ffffff/new-post.png" alt="Email"/>
    </a>
    <p style='margin-top: 10px;'>Developed by <strong>S.M. Shahriar</strong></p>
</div>
""", unsafe_allow_html=True)

