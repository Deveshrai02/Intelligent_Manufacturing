This project simulates an enterprise genealogy system capturing vehicle-level operational history across stations and vendors. The goal is to design an AI-powered risk intelligence layer that detects anomalies and predicts warranty risk using structured relational data.

High Level Flow -

Data Ingestion -> Data Storage -> Data Preprocessing -> Exploratory Data Analysis -> Feature Engineering ->ML Model Training ->ML Model registry ->FAST API Service ->Docker Deployment

Data Ingestion- Data Ingestion is the process of building a pipeline to get the data from various sources be it the execution system , upstream systems , etc . Realtime data gets populated in the genealogy service from which data would be fetched to do further processes

Data storage - Ingested data needs to be stored . We are going to use relational database to store the data and query it for data retreival and preprocessing. We have chosen to use relational database as in our project the architecture will be based on one to many relationship between two entities , also it aligns perfectly with genealogy data and even enterprise systems are relational

Data Preprocessing - Building Data preprocessing pipeline is very crucial as data coming from various systems might have missing values , duplicated values , etc which might cause issues during futher analysis

EDA - We would try to find out as much info as possible from the data , patterns between various features , which feature is more impacting the labels , what correlations are there in the data , etc. One of the key steps to make the project more informative

Feature Engineering - With all the features we would try to find out if some more features can be extracted , some features can be transformed and mainly all the features should be encoded so that it can become a ML ready dataset

ML Model Training - Various ML models will be tested and the one giving best results in terma of all the parameters will be exported to build the prediction and detection interface




