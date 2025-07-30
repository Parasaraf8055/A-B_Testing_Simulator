# A-B_Testing_Simulator
a Simulator for A and B specially for ml models , strategies and any two items using statistical analysis  

# 🧪 A/B Testing Simulator & Analyzer

An interactive Streamlit web application designed to simulate A/B tests and perform statistical analysis to determine the impact of product features or different models/strategies. This tool helps understand A/B testing principles, estimate statistical significance, and make data-driven decisions.
Preview :- https://abtestingsimulator.streamlit.app/

## ✨ Key Features

* **Synthetic Data Generation:** Quickly generate randomized control and test group datasets with configurable baseline conversion rates and expected uplifts.

* **Custom Data Upload:** Analyze your own real-world A/B test data by uploading CSV files for control and test groups. (CSV files must contain a 'converted' column with 0s and 1s).

* **Statistical Analysis:**
    * Calculates conversion rates and confidence intervals for both groups.
    * Performs Welch's t-test for independent samples to assess statistical significance.
    * Supports two-sided, 'greater than', and 'less than' alternative hypotheses.

* **Clear Visualizations:** Generates a bar plot comparing conversion rates with 95% (or configurable) confidence intervals.

* **Detailed Reports:** Provides a comprehensive textual summary of the experiment's configuration, observed metrics, statistical test results, and a clear conclusion based on the p-value.

* **Reproducibility:** Use a random seed for synthetic data generation to get consistent results across runs.

## 🚀 Why This Project?

A/B testing is fundamental for data-driven decision-making in product development, marketing, and machine learning , specially in data science. This simulator bridges the gap between theoretical understanding and practical application, allowing users to:

* **Learn:** Experiment with different sample sizes, baseline rates, and uplifts to build intuition about statistical significance, p-values, and confidence intervals.

* **Plan:** Gain insights into required sample sizes or the likely outcome of an experiment before running a costly live test.

* **Analyze:** Quickly analyze real-world A/B test results from your own data, making the statistical analysis accessible and interpretable.

* **Compare ML Models/Strategies:** While the simulator doesn't *run* ML models, its statistical analysis framework is precisely what you would use to evaluate the *user-facing impact* (e.g., click-through rate, conversion) of different ML models deployed in a live A/B test.

## 🛠️ Technologies Used

* **Python 3.x**
* **Pandas:** For data manipulation and analysis.
* **NumPy:** For numerical operations, especially in data generation.
* **SciPy:** For statistical functions (t-tests).
* **Matplotlib:** For fundamental plotting.
* **Seaborn:** For enhanced statistical visualizations.
* **Streamlit:** For creating the interactive web user interface.

## ⚙️ Local Setup and Run

To run this application on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/ab-testing-simulator-app.git](https://github.com/YourGitHubUsername/ab-testing-simulator-app.git)
    cd ab-testing-simulator-app
    ```
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the Virtual Environment:**
    * **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the Streamlit Application:**
    ```bash
    streamlit run ab_testing_app.py  # Or whatever your main app file is named (e.g., tester_app.py)
    ```
    (Ensure your main Streamlit app file is at the root of the cloned directory.)

    Your web browser should automatically open the application at `http://localhost:8501`.

## ☁️ Free Cloud Deployment (Streamlit Cloud)

This application can be easily deployed for free using Streamlit Cloud:

1.  **Host on GitHub:** Ensure your project (including `ab_testing_app.py` and `requirements.txt`) is pushed to a **public** GitHub repository.
2.  **Sign in to Streamlit Cloud:** Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3.  **Deploy New App:** Click on "New app", select your repository, choose the main file path (e.g., `ab_testing_app.py`), and click "Deploy!".

Streamlit Cloud will handle the environment setup and provide you with a public URL for your app.

## 🛣️ Future Enhancements (Roadmap)

* [ ] Implement Chi-Squared test for proportions.
* [ ] Add power analysis functionality for experiment design.
* [ ] Introduce more complex data simulation parameters (e.g., overdispersion).
* [ ] Enhance data upload with more robust validation and column mapping.
* [ ] Provide options to export reports (PDF, Markdown, CSV) and plots (PNG).
* [ ] Explore sequential A/B testing methodologies.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, new features, or bug fixes, feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'feat: Add new feature X'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. *(Create a LICENSE file in your repo if you want this, otherwise remove this line)*

## 📧 Contact

Paras Saraf - [sarafparas792@gmail.com]

---
