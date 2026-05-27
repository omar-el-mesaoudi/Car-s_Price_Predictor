# Mercedes-Benz Valuation Engine : End-to-End Price Predictor
An end-to-end Machine Learning pipeline that collects real-time vehicle listings via web scraping, conducts extensive exploratory data analysis (EDA), implements advanced feature engineering, and deploys a high-performance LightGBM Regressor achieving a 96% prediction accuracy. The final model is fully deployed as an interactive web dashboard using Streamlit.
## Project Architecture
    └── Code/
        └── scraper.py                    # Data extraction module using automated prompting
    └── Data/
        └── mercedes_data_full.csv        # Full dataset containing scraped car listings
    └── Deployment/
        └── Streamlit_app.bat             # Windows batch file to launch the application
    └── Notebook/
        └── Car's price predictor.ipynb   # EDA, Feature Engineering, Modeling & Evaluation
    └── LICENSE                           # MIT License
    └── README.md                         # Project documentation
    └── requirements.txt                  # File containing required packages for reproduction
## Detailed Workflow & Methodology
### 1. Data Collection (Web Scraping)
Real-time automotive market data was dynamically extracted from "https://www.cars.com". Data extraction was managed programmatically using an automated scraping script powered by Google Antigravity.
* **Prompt Used** : ```Scrap this website : "https://www.cars.com" and gather data about mercedes benz cars from it and save it into a csv file```<br><br>
* **Artifact** : The automation script is saved as ```Code/scraper.py```, and the resulting complete dataset (```mercedes_data_full.csv```) was exported directly to the ```Data/``` folder.
### 2. Exploratory Data Analysis & Cleaning
* **Outlier Handling** : Addressed data discrepancies in the ```mileage``` field by handling extreme outliers (e.g., >500k miles) using median imputation to stabilize variance.
* **Feature Dropping** : Structural dimensionality reduction was completed by removing low-signal features and identifiers (```dealer```, ```url```, ```seller_address```, ```seller_phone```, ```rating```, ```review_count```).
### 3. Feature Engineering
* **Temporal Splitting** : Extracted the structural production year (```car_year```) from raw text attributes.
* **Text Mining & Normalization** : Implemented regular expression patterns to parse text strings, stripping out redundancy to isolate clean vehicle tracking classifications (```model```).
* **High-Cardinality Parsing** : Built a conditional loop mapping system to extract over 45 high-frequency luxury features (e.g., ```Heated Seats```, ```Adaptive Cruise Control```, ```Keyless Entry```) out of semi-structured text blocks, converting them into explicit Boolean flags.
* **Categorical Encoding** : Converted all processed non-numeric features into machine-readable numbers using ```LabelEncoder```.
### 4. Machine Learning Modeling & Evaluation
Multiple regression algorithms were evaluated using Cross-Validation. The final candidate chosen was a LightGBM Regressor (LGBMRegressor) due to its rapid training capabilities and performance on high-cardinality categorical frameworks.
* **Metric Realized** : 96% Accuracy ($R^2$ Score).
* **Inference Demonstration** : The end of the Jupyter notebook includes a fully functional, step-by-step prediction example demonstrating model inference on an unobserved test vehicle configuration.
## Model Deployment & Web App
The analytical model was translated into an interactive consumer interface using Cursor.
* **Prompt Used** : ```create a streamlit application using this code [provided prediction sample code and categorical mappings]```
* **Deployment Automation** : To ensure accessibility, a dedicated Windows Batch file (```Streamlit_app.bat```) was built inside the ```Deployment/``` directory to automate application startup for end-users.
