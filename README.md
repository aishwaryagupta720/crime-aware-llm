# California Violent Crime Visualization & Analysis 📊🚨

## Project Overview

Explore an interactive and intelligent data visualization platform designed to analyze violent crime rates across California from 2000 to 2013. This project combines powerful data visualization tools and advanced AI to offer valuable insights into crime trends, hotspots, and safety dynamics.

## Key Features

- 🔥 **[Heatmaps](heatmap.png)**: Quickly identify geographic crime density patterns across California counties.\


- 📈 **[Line Graphs](line_chart.png) & [Pie Charts](pie_chart.png)**: Easily visualize historical trends and breakdown of violent crime types.\
  \


- 📍 **[Geospatial Clustering](geospace.png)**: Utilizes K-Means clustering to highlight crime hotspots and regional safety profiles.\


- 🤖 **[AI-powered Chatbot](chatbot.png)**: Built with [PandasAI's Bamboo LLM](https://github.com/pandas-ai/pandas-ai), providing dynamic, instant data-driven insights.\


## Data Preprocessing

- Utilized Python Pandas library
- Trimmed columns with irrelevant features
- Calculated rate percentage using reported crimes and populations
- Analyzed and aggregated data by county
- Normalized data by removing counties that did not report crime (empty rows)
- Renamed columns to provide meaningful input for the LLM model

## Technologies Used

- **Backend**: Python, Pandas, NumPy
- **Visualization Libraries**: JavaScript, D3.js, Plotly
- **Interactive UI**: Streamlit
- **AI Integration**: PandasAI (Bamboo LLM)

## Why this Matters

Understanding crime trends helps improve community safety, inform potential homebuyers, guide tourists, and assist law enforcement with targeted resource allocation. This interactive tool enhances user experience, making complex data accessible and actionable.

## Getting Started

This project uses both a Streamlit frontend and a custom LLM backend Flask API to handle intelligent chat queries. Follow the steps below to run both components smoothly.

1. Clone this repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the custom Flask API chatbot (LLM Backend):

```bash
cd LLM
docker build -t crime-llm-backend .
docker run -p 5000:5000 crime-llm-backend
```

> ℹ️ This runs the intelligent Flask API on port `5000`, which is used to respond to user queries in the Streamlit interface.

> Make sure `crime_data_california.csv` is in the same directory as `llm_handler.py` inside the Docker context.


4. Run the Streamlit application:

```bash
streamlit run app.py
```

## Contributing

Your contributions are welcome! Feel free to open issues, submit feature requests, or create pull requests to enhance this project.

## Connect

Feel free to reach out for feedback, suggestions, or collaborations!

Enjoy exploring data, empowered by visualization and AI! 🌟

\#DataVisualization #MachineLearning #AI #BackendDevelopment #Python #JavaScript #CommunitySafety

