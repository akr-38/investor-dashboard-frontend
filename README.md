

# Investor Dashboard - Frontend

This repository contains the interactive frontend for the Investor Dashboard, built with Streamlit. It allows users to visualize and analyze vehicle registration data by interacting with a clean, user-friendly interface.
This is just a part of the whole investor dashboard project: **[Investor Dashboard Project](https://github.com/akr-38/investors-dashboard-project/blob/main/README.md)**


## ⚙️ Tech Stack

  * **Framework:** Streamlit
  * **API Interaction:** `requests`
  * **Data Handling:** `pandas`
  * **Charting:** `plotly`
  * **Environment Management:** `python-dotenv`

-----

## 🛠️ Getting Started

Follow these steps to set up and run the frontend dashboard.

### Prerequisites

  * **Python 3.9+**
  * **A running backend API server** from the [Investor Dashboard Backend](https://github.com/akr-38/investor-dashboard-backend) repository.

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/akr-38/investor-dashboard-frontend.git
cd investor-dashboard-frontend
```

### Step 2: Set up the Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required Python packages:

```bash
pip install streamlit requests pandas plotly python-dotenv
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project's root directory and add the URL of your running backend API.

```ini
# .env
BASE_URL="http://127.0.0.1:8000"
```

### Step 5: Run the Streamlit Application

With all dependencies installed and the `.env` file configured, you can launch the dashboard with the following command:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

-----

## 🖥️ Dashboard Features

The dashboard provides a powerful and flexible interface for analyzing automobile registration data.

### Interactive Controls

<img width="916" height="328" alt="{E60907DF-76EE-4B3B-81BE-F922B4AAFE85}" src="https://github.com/user-attachments/assets/557749a7-e1d1-451c-8c36-77780c0d1db6" />


The main interface features a series of selectors and inputs to refine your data view:

  * **Select Vehicle Category:** Choose between "All Categories" or specific types like `2W`, `3W`, and `4W`.
  * **Select Manufacturer:** Filter by a specific manufacturer or view all.
  * **Date Range:** Use the "Start Year" and "End Year" selectors, along with "Start Quarter" and "End Quarter," to define your analysis period.

### Data Analysis and Visualization

<img width="960" height="540" alt="{A1B7F07C-9042-4FA6-B067-70F58AB3805D}" src="https://github.com/user-attachments/assets/1ea5c8b3-2d7a-46d0-9beb-1ad4d9cbfbfe" />

<img width="960" height="540" alt="{E9587318-CE03-4B5F-8304-C88EEEC44908}" src="https://github.com/user-attachments/assets/27c0c61b-b908-4a7e-b71b-0d599433fcc5" />

<img width="960" height="540" alt="{D4280DA8-3725-46E3-83D6-BA4866699445}" src="https://github.com/user-attachments/assets/f9e7c3ef-fb30-458d-97db-5dcaa0e5a683" />


Once you submit your selections, the dashboard displays a comprehensive analysis, including:

  * **Key Performance Indicators:** The average Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth percentages are displayed prominently.
  * **Time-Series Charts:**
      * **Registrations by Year:** A line chart showing total registrations over the full years in the selected range.
      * **Registrations by Quarter:** A line chart showing a sequential view of registrations by quarter.
  * **Detailed Tables:** Data tables provide the underlying numbers for the visualizations, including calculated YoY and QoQ percentages.
