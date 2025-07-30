from data_generator import ABTestDataSet
import pandas as pd
import numpy as np
from scipy import stats
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ABTestAnalyzer:
    """
    Performs statistical analysis on A/B test data.
    """
    def __init__(self, dataset: ABTestDataSet):
        """
        Initializes the analyzer with an ABTestDataSet.
        """
        self.dataset = dataset
        self.config = dataset.config
        self._results: dict = {}
        logger.info("ABTestAnalyzer initialized.")

    def _calculate_conversion_rate(self, data: pd.DataFrame) -> float:
        """Helper to calculate conversion rate."""
        if 'converted' not in data.columns:
            raise ValueError("DataFrame must contain a 'converted' column.")
        return data['converted'].mean()

    def _calculate_confidence_interval(self, data: pd.DataFrame) -> tuple[float, float]:
        """
        Calculates the confidence interval for a proportion (conversion rate).
        Uses Wald interval (Normal Approximation).
        """
        n = len(data)
        if n == 0:
            return (np.nan, np.nan)
        p = self._calculate_conversion_rate(data)
        if p == 0 or p == 1: # Handle edge cases for SE calculation
            logger.warning(f"Conversion rate is {p}. Confidence interval may be degenerate.")
            return (p, p)
        se = np.sqrt(p * (1 - p) / n)
        z_score = stats.norm.ppf(1 - self.config.alpha / 2)
        margin_of_error = z_score * se
        return (p - margin_of_error, p + margin_of_error)

    def _perform_t_test(self, control_data: pd.DataFrame, test_data: pd.DataFrame) -> tuple[float, float]:
        """
        Performs Welch's t-test for independent samples.
        """
        t_stat, p_value = stats.ttest_ind(
            control_data['converted'],
            test_data['converted'],
            equal_var=False, # Welch's t-test, doesn't assume equal variances
            alternative=self.config.alternative_hypothesis
        )
        return t_stat, p_value

    def run_analysis(self) -> dict:
        """
        Executes all statistical analyses and stores results.
        """
        logger.info("Running statistical analysis...")
        control_df = self.dataset.get_control_data()
        test_df = self.dataset.get_test_data()

        if control_df.empty or test_df.empty:
            raise ValueError("Cannot perform analysis on empty datasets.")

        self._results['control_conversion'] = self._calculate_conversion_rate(control_df)
        self._results['test_conversion'] = self._calculate_conversion_rate(test_df)
        self._results['observed_difference'] = self._results['test_conversion'] - self._results['control_conversion']

        ci_control_lower, ci_control_upper = self._calculate_confidence_interval(control_df)
        ci_test_lower, ci_test_upper = self._calculate_confidence_interval(test_df)
        self._results['ci_control_lower'] = ci_control_lower
        self._results['ci_control_upper'] = ci_control_upper
        self._results['ci_test_lower'] = ci_test_lower
        self._results['ci_test_upper'] = ci_test_upper

        self._results['t_statistic'], self._results['p_value'] = \
            self._perform_t_test(control_df, test_df)

        self._results['alpha'] = self.config.alpha
        self._results['alternative_hypothesis'] = self.config.alternative_hypothesis
        self._results['control_size'] = len(control_df)
        self._results['test_size'] = len(test_df)

        print(f"printing the result : {self._results['control_conversion']}")

        logger.info("Analysis complete.")
        return self._results

    def get_results(self) -> dict:
        """Returns the stored analysis results."""
        if not self._results:
            logger.warning("Analysis has not been run yet. Call run_analysis() first.")
        return self._results
