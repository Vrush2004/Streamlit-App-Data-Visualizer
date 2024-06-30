import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Data Visualizer",
    layout="centered",
    page_icon="📊"
)

# Title
st.title("📊 Data Visualizer - Web App")

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = f"{working_dir}/data"

# List the files present in 'data' folder
files_list = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Dropdown for all the files
selected_file = st.selectbox("Select a file", files_list, index=None)

if selected_file:
    # Get the complete path of the selected file
    file_path = os.path.join(folder_path, selected_file)

    # Reading the CSV file as a pandas dataframe
    df = pd.read_csv(file_path)

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        # Selection of columns
        x_axis = st.selectbox("Select the X-axis", options=columns + ["None"], index=None)
        y_axis = st.selectbox("Select the Y-axis", options=columns + ["None"], index=None)

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot', 'Box Plot', 'Heatmap', 'Violin Plot']
        selected_plot = st.selectbox("Select a Plot", options=plot_list, index=None)

    # Button to generate plots
    if st.button("Generate Plot"):
        fig, ax = plt.subplots(figsize=(6, 4))

        if selected_plot == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)

        elif selected_plot == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)

        elif selected_plot == 'Box Plot':
            sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)

        elif selected_plot == 'Heatmap':
            if x_axis != "None" and y_axis != "None":
                heatmap_data = df.pivot_table(index=y_axis, columns=x_axis, aggfunc='size', fill_value=0)
                sns.heatmap(heatmap_data, ax=ax, cmap="YlGnBu")
            else:
                st.error("Heatmap requires both X-axis and Y-axis to be selected")

        elif selected_plot == 'Violin Plot':
            sns.violinplot(x=df[x_axis], y=df[y_axis], ax=ax)

        # Adjust label sizes
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Title axes labels
        plt.title(f"{selected_plot} of {y_axis} vs {x_axis}")
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        st.pyplot(fig)

