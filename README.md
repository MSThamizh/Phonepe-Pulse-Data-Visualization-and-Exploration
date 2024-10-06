# PhonePe Pulse Data Visualization and Exploration

This project provides an interactive platform for visualizing and exploring transaction data from the PhonePe Pulse repository. Users can gain insights into transaction trends across different parameters through dynamic visualizations.

## Features

- **Data Extraction & Transformation**: Python scripts for cloning the PhonePe Pulse dataset and cleaning it for analysis.
- **Database Integration**: Cleaned data is stored in a **MySQL** database for efficient data retrieval.
- **Interactive Dashboard**: Built with **Streamlit** and **Plotly**, offering a user-friendly interface with multiple dropdown options to filter and visualize different insights.
- **Real-time Geo-visualizations**: Interactive maps displaying transaction data across various regions and timeframes.
- **Secure & Scalable**: Designed to maintain data integrity and ensure efficient performance.
  
## Workflow

The workflow of this project can be summarized as follows:

1. **Data Acquisition**: Clone the PhonePe Pulse GitHub repository to access the dataset. Identify relevant data files containing transaction details.
2. **Data Extraction**: Write a Python script to extract data from the cloned repository. Implement data loading logic to read and process the dataset.
3. **Data Transformation**: Transform the dataset into a structured format suitable for analysis. Use Pandas for data manipulation and transformation tasks.
4. **Data Storage**: Set up a MySQL database to store the cleaned and transformed data. Load the transformed data into the MySQL database for easy access.
5. **Dashboard Development**: Create an interactive dashboard using Streamlit. Implement visualizations using Plotly for geo-mapping and other data representations. Design multiple dropdown filters to enable users to explore different aspects of the data.

## Technologies Used

- **Python**: Main programming language used for scripting and development.
- **Libraries**: Pandas, Plotly, Streamlit
- **Database**: MySQL
- **Visualization**: Geo-mapping and Data Visualizations using Plotly and Streamlit

## References

- **Python**: [https://docs.python.org/3/](https://docs.python.org/3/)
- **Pandas Dataframe**: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)]
- **Plotly Documentation**: [https://plotly.com/python/](https://plotly.com/python/)
- **MySQL Documentation**: [https://www.mysql.com/](https://www.mysql.com/)
- **Streamlit Documentation**: [https://docs.streamlit.io/library/api-reference](https://docs.streamlit.io/library/api-reference)
- **Dataset**: [https://github.com/PhonePe/pulse#readme](https://github.com/PhonePe/pulse#readme)
