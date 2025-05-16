import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import io


def generate_plot(data, x_col, y_col, chart_type, output_format='png'):
    buf = io.BytesIO()
    plt.figure(figsize=(10, 6))

    if chart_type == 'Line Chart':
        sns.lineplot(data=data, x=x_col, y=y_col)
    elif chart_type == 'Bar Chart':
        sns.barplot(data=data, x=x_col, y=y_col)
    elif chart_type == 'Scatter Plot':
        sns.scatterplot(data=data, x=x_col, y=y_col)
    elif chart_type == 'Histogram':
        sns.histplot(data[y_col], kde=True)
    elif chart_type == 'Pie Chart':
        # Pie chart must use value counts
        pie_data = data[y_col].value_counts()
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        plt.ylabel('')
    else:
        raise ValueError("Unsupported chart type")

    plt.tight_layout()
    plt.savefig(buf, format=output_format)
    buf.seek(0)

    if output_format in ['jpg', 'jpeg']:
        img = Image.open(buf).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format=output_format.upper())
        buf.seek(0)

    return buf
