# Mercedes-Benz Valuation Engine : End-to-End Price Predictor
An end-to-end Machine Learning pipeline that collects real-time vehicle listings via web scraping, conducts extensive exploratory data analysis (EDA), implements advanced feature engineering, and deploys a high-performance LightGBM Regressor achieving a 96% prediction accuracy. The final model is fully deployed as an interactive web dashboard using Streamlit.
## Project Architecture
├── Notebook/
    └──Car's price predictor.ipynb   # EDA, Feature Engineering, Modeling & Evaluation
├── Code/
│   └── scraper.py                   # Data extraction module using automated prompting
├── Deployment/
│   └── Streamlit_app.bat            # Windows batch file to launch the application
├── Data/
│   └── mercedes_data_full.csv       # Full dataset containing scraped car listings
├── LICENSE                          # MIT License
├── README.md                        # Project documentation
└── requirements.txt                 # File containing required packages for reproduction
