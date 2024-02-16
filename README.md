# NBA Odds Predictor
## Project Overview

Welcome to the internal documentation for the NBA Odds Predictor project. This repository houses our ongoing efforts to develop a machine learning model aimed at predicting NBA game odds. The project is currently in the data collection and preprocessing phase, and this documentation is intended for team members and specific collaborators.

### Current Implementation

The repository currently includes a Python script that interfaces with the NBA API to fetch and process basketball game data. Key features of the script:

- Retrieves data for NBA seasons from 2015 to 2018.
- Collects player statistics, team information, and game results.
- Structures data into a format suitable for machine learning models.
- Cleans and preprocesses the data for optimal analysis.

### Project Goals

Our roadmap for this project includes:

- Developing and refining a machine learning model using the collected data.
- Evaluating the model's ...

## Repository Contents

### Scripts for Model Training and Prediction

1. **Total Assists Training Code** (`final_version_ou_player_total_assists_training_code_probabilities.py`):
   - Trains a model using Random Forest Regressor to predict the total assists by NBA players.

2. **Total Free Throws Made (FTM) Training Code** (`final_version_ou_player_total_ftm_training_code_probabilities.py`):
   - Focuses on predicting total free throws made (FTM) using a Random Forest Regressor.

3. **Total Points Training Code** (`final_version_ou_player_total_points_training_code_probabilities.py`):
   - Employs TensorFlow and Keras to train a neural network model for predicting total points scored.

4. **Total Rebounds Training Code** (`final_version_ou_player_total_rebounds_training_code_probabilities.py`):
   - Neural network-based prediction of total rebounds using TensorFlow and Keras.

5. **Total Steals Training Code** (`final_version_ou_player_total_steals_training_code_probabilities.py`):
   - Uses a Random Forest Regressor to predict the total number of steals.

6. **Total Three-Pointers Made (TPM) Training Code** (`final_version_ou_player_total_tpm_training_code_probabilities.py`):
   - Predicts total three-pointers made using a Random Forest Regressor.

7. **Total Turnovers Training Code** (`final_version_ou_player_turnovers_training_code_probabilities.py`):
   - Random Forest Regressor-based model for predicting total turnovers.

8. **Player Predictor with Input Parameters** (`ou_player_predictor_probabilities_with_input_all_parameters.py`):
   - Utility script for making predictions with uncertainty using the trained models.

9. **Total Blocks Training Code** (`final_version_ou_player_blocks_training_code_probabilities.py`):
    - Trains a Random Forest Regressor model to predict the total number of blocks by NBA players.

10. **Field Goal Attempts (FGA) Training Code** (`final_version_ou_player_fga_code_probabilities.py`):
    - Uses TensorFlow and Keras to train a neural network model for predicting the number of field goal attempts (FGA).

11. **Input Document Generation** (`generate_input_document_optimized.py`):
    - Generates input data for models, likely by fetching and processing player data.

12. **Data Comparator for All Criteria** (`final_data_comparator_for_all_criterias_with_actual_data_from_first_match.py`):
    - Compares predictions with actual game performance data, focusing on the first game for each player.

### Data and Resources

- The scripts utilize a variety of data sources, primarily historical player performance data, to train and validate the models. Detailed information about these data sources can be found in the respective scripts.

## Usage

- Each script is designed for a specific part of the model training and prediction process. Please refer to the individual scripts for detailed usage instructions and requirements.

## Contributions

- Contributions to this project are currently limited to team members and specific collaborators. If you're interested in contributing, please contact the project lead for more information.

## Contact

- For any queries or further information regarding this project, please reach out to Alexandru Borza.

# Web Application Project Architecture

This document provides an overview of the architecture for a web application designed to display player statistics and predictions across various sports. The application utilizes Django for the frontend and backend, interfaces with a PostgreSQL database, and transitions from CSV to an API for data sourcing. It's containerized with Docker, orchestrated with Kubernetes, and includes a CI/CD pipeline with Jenkins/Tekton, all while securely managing secrets with Vault.

## Architecture Overview

The application's architecture comprises several key components, each playing a critical role in the system's functionality:

1. **Django Web Application**: Manages both the frontend and backend, displaying data related to player statistics and game predictions.
2. **Data Source Transition**: Initially uses CSV files for data, transitioning to an external API for real-time updates.
3. **PostgreSQL Database**: Stores application and user data.
4. **Docker**: Containerizes the application, ensuring consistency across different environments.
5. **Kubernetes**: Orchestrates container deployment, scaling, and management.
6. **CI/CD Pipeline**: Utilizes GitHub for source control, with Jenkins/Tekton for build, test, and deployment automation. Includes separate environments for development and production.
7. **Vault**: Secures sensitive information such as API keys and database credentials.

### Simplified Architectural Diagram Representation

Since markdown does not support embedding graphical diagrams directly, here's a textual representation of the system architecture:

- `Django Web Application` interacts with both `CSV/External API` for data sourcing and the `PostgreSQL Database` for data storage.
- The application is `Containerized with Docker` and managed by `Kubernetes` for orchestration.
- `GitHub` hosts the code repository, which integrates with `Jenkins/Tekton` for continuous integration and deployment across `Dev and Prod` environments.
- `Vault` securely manages all secrets required by the application and the CI/CD pipeline.

## Getting Started

### Setting up the Django Application

1. Initialize your Django project and application.
2. Define models for your data and views to present it.
3. Write scripts to load data from CSV files, planning to switch to API calls.

### Dockerization and Kubernetes Setup

1. Create a `Dockerfile` for your application.
2. Use `Docker Compose` for local development and testing.
3. Configure `Kubernetes` for production deployment and scaling.

### CI/CD Pipeline Configuration

1. Store your code in `GitHub`, utilizing branches for workflow management.
2. Setup `Jenkins` or `Tekton` for automating builds, tests, and deployments.
3. Integrate `Vault` for managing secrets within your pipeline.

## Development, Testing, and Deployment

- Develop and test locally using Docker.
- Automate testing within your CI/CD pipeline.
- Deploy via Kubernetes, monitoring your application's performance and health.
