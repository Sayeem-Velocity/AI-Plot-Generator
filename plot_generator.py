import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

def generate_plot(data, x_cols, y_cols, chart_type, color='blue', title='', xlabel='', ylabel='', legend=True):
    buf = io.BytesIO()
    plt.figure(figsize=(10, 6))

    if chart_type == 'Line Chart':
        for y in y_cols:
            sns.lineplot(data=data, x=x_cols[0], y=y, label=y if legend else "_nolegend_", color=color)
    elif chart_type == 'Bar Chart':
        for y in y_cols:
            sns.barplot(data=data, x=x_cols[0], y=y, label=y if legend else "_nolegend_", color=color)
    elif chart_type == 'Scatter Plot':
        for y in y_cols:
            sns.scatterplot(data=data, x=x_cols[0], y=y, label=y if legend else "_nolegend_", color=color)
    elif chart_type == 'Histogram':
        for y in y_cols:
            sns.histplot(data[y], kde=True, color=color, label=y if legend else "_nolegend_")
    elif chart_type == 'Pie Chart':
        pie_data = data[y_cols[0]].value_counts()
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        plt.ylabel('')
    else:
        raise ValueError("Unsupported chart type")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if legend and chart_type != 'Pie Chart':
        plt.legend()

    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)

    img = Image.open(buf).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return buf
