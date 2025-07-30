import logging
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from config import ABTestConfig
from data_generator import ABTestDataSet
from tester import ABTestAnalyzer
from reporter import ABTestReporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ABTestSimulator:
    """
    Orchestrates the entire A/B testing simulation process.
    """
    def __init__(self, config: ABTestConfig, control_df: pd.DataFrame = None, test_df: pd.DataFrame = None):
        """
        Initializes the simulator with a configuration.
        Optionally takes existing dataframes for analysis.
        """
        self.config = config
        self.control_df_input = control_df
        self.test_df_input = test_df
        self.dataset: ABTestDataSet = None
        self.analyzer: ABTestAnalyzer = None
        self.reporter: ABTestReporter = None
        self.results: dict = {}
        logger.info("ABTestSimulator initialized.")

    def run_simulation(self):
        """
        Runs the full A/B test simulation: data generation/loading, analysis, and reporting.
        Returns the report string and plot figure.
        """
        logger.info(f"Starting A/B Test Simulation with config: {self.config.__dict__}")
        try:
            # 1. Data Generation or Loading
            self.dataset = ABTestDataSet(self.config, control_df=self.control_df_input, test_df=self.test_df_input)

            # 2. Statistical Analysis
            self.analyzer = ABTestAnalyzer(self.dataset)
            self.results = self.analyzer.run_analysis()

            # 3. Reporting
            self.reporter = ABTestReporter(self.results)
            report_markdown = self.reporter.get_summary_markdown_string()
            plot_figure = self.reporter.get_conversion_rates_plot()

            logger.info("A/B Test Simulation completed successfully.")
            return report_markdown, plot_figure

        except ValueError as e:
            logger.error(f"Configuration or Data Error: {e}")
            st.error(f"Error: {e}")
            return None, None # Indicate failure
        except Exception as e:
            logger.error(f"An unexpected error occurred during simulation: {e}", exc_info=True)
            st.error(f"An unexpected error occurred: {e}")
            return None, None # Indicate failure
        
def main():
    st.set_page_config(layout="wide", page_title="A/B Testing Simulator")

    st.title("🧪 A/B Testing Simulator & Analyzer")
    st.markdown("""
        Design and analyze simulated A/B tests or upload your own data to compare product feature impacts.
        This tool uses t-tests to determine statistical significance.
    """)

    # --- Sidebar for Configuration ---
    st.sidebar.header("Experiment Configuration")

    analysis_mode = st.sidebar.radio(
        "Choose Analysis Mode:",
        ("Simulate New Data", "Analyze My Own Data"),
        index=0 # Default to Simulate
    )

    control_df_uploaded = None
    test_df_uploaded = None

    if analysis_mode == "Analyze My Own Data":
        st.sidebar.markdown("---")
        st.sidebar.subheader("Upload Your Data (CSV)")
        st.sidebar.info("Your CSVs must contain a 'converted' column (0 or 1).")

        control_file = st.sidebar.file_uploader("Upload Control Group CSV", type=["csv"], key="control_uploader")
        test_file = st.sidebar.file_uploader("Upload Test Group CSV", type=["csv"], key="test_uploader")

        if control_file is not None:
            try:
                control_df_uploaded = pd.read_csv(control_file)
                st.sidebar.success(f"Control data loaded: {len(control_df_uploaded)} rows.")
                st.sidebar.dataframe(control_df_uploaded.head(3))
            except Exception as e:
                st.sidebar.error(f"Error loading control CSV: {e}")
                control_df_uploaded = None
        if test_file is not None:
            try:
                test_df_uploaded = pd.read_csv(test_file)
                st.sidebar.success(f"Test data loaded: {len(test_df_uploaded)} rows.")
                st.sidebar.dataframe(test_df_uploaded.head(3))
            except Exception as e:
                st.sidebar.error(f"Error loading test CSV: {e}")
                test_df_uploaded = None

        if control_df_uploaded is not None and test_df_uploaded is not None:
            # Override n_control/n_test if using uploaded data
            n_control_default = len(control_df_uploaded)
            n_test_default = len(test_df_uploaded)
            st.sidebar.markdown("---")
            st.sidebar.info(f"Using uploaded data sizes: Control={n_control_default}, Test={n_test_default}")
        else:
            # If files not loaded, default to simulation settings temporarily
            n_control_default = 1000
            n_test_default = 1000

    else: # Simulate New Data
        st.sidebar.markdown("---")
        st.sidebar.subheader("Synthetic Data Parameters")
        n_control_default = st.sidebar.number_input(
            "Control Group Size (n_control)", min_value=10, value=1000, step=200
        )
        n_test_default = st.sidebar.number_input(
            "Test Group Size (n_test)", min_value=10, value=1000, step=200
        )
        baseline_conversion_rate = st.sidebar.slider(
            "Baseline Conversion Rate (Control)", min_value=0.01, max_value=0.50, value=0.10, step=0.005
        )
        expected_uplift = st.sidebar.slider(
            "Expected Absolute Uplift (Test vs. Control)", min_value=-0.05, max_value=0.10, value=0.01, step=0.001, format="%.3f"
        )
        random_seed = st.sidebar.number_input(
            "Random Seed (for reproducibility)", min_value=0, value=42, step=1
        )


    st.sidebar.markdown("---")
    st.sidebar.subheader("Statistical Parameters")
    alpha = st.sidebar.slider(
        "Significance Level (alpha)", min_value=0.001, max_value=0.10, value=0.05, step=0.001, format="%.3f"
    )
    alternative_hypothesis = st.sidebar.selectbox(
        "Alternative Hypothesis",
        ('two-sided', 'greater', 'less'),
        index=0 # Default to two-sided
    )

    st.sidebar.markdown("---")
    run_button = st.sidebar.button("🔬 Run A/B Simulation")

    # --- Main Content Area ---
    if run_button:
        if analysis_mode == "Analyze My Own Data" and (control_df_uploaded is None or test_df_uploaded is None):
            st.error("Please upload both Control and Test CSV files to analyze your own data.")
            run_button = False # Prevent further execution

        if run_button:
            with st.spinner("Running simulation and analysis..."):
                try:
                    # Create config object based on selected mode
                    config = ABTestConfig(
                        n_control=n_control_default,
                        n_test=n_test_default,
                        baseline_conversion_rate=baseline_conversion_rate if analysis_mode == "Simulate New Data" else 0.1, # Dummy if using uploaded, actual not used directly
                        expected_uplift=expected_uplift if analysis_mode == "Simulate New Data" else 0.0, # Dummy
                        alpha=alpha,
                        random_seed=random_seed if analysis_mode == "Simulate New Data" else None, # Seed only for synthetic
                        alternative_hypothesis=alternative_hypothesis
                    )

                    # Instantiate simulator, passing uploaded data if available
                    simulator = ABTestSimulator(
                        config,
                        control_df=control_df_uploaded,
                        test_df=test_df_uploaded
                    )

                    report_markdown, plot_figure = simulator.run_simulation()

                    if report_markdown and plot_figure:
                        st.success("Simulation Complete!")
                        st.markdown(report_markdown)
                        st.pyplot(plot_figure) # Display the plot
                        plt.close(plot_figure) # Close the figure to free memory

                except ValueError as ve:
                    st.error(f"Configuration Error: {ve}")
                except Exception as e:
                    st.error(f"An unexpected error occurred during simulation: {e}")
                    logger.error(f"Unhandled error in main app: {e}", exc_info=True)


    st.markdown("---")
    st.markdown("Developed by Your Paras Saraf & Team") # Customize this
    st.markdown(f"Current Server Time (Pune, India): {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S IST')}")

if __name__ == "__main__":
    main()