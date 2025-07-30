import pandas as pd
import numpy as np
from config import ABTestConfig
import logging



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ABTestDataSet:
    """
    Manages A/B test data, including generation of synthetic data or loading existing data.
    """
    def __init__(self, config: ABTestConfig, control_df: pd.DataFrame = None, test_df: pd.DataFrame = None):
        """
        Initializes the data set. If control_df and test_df are provided, they are used.
        Otherwise, synthetic data is generated.

        Args:
            config (ABTestConfig): Configuration object for parameters.
            control_df (pd.DataFrame, optional): Pre-existing control group data.
            test_df (pd.DataFrame, optional): Pre-existing test group data.
        """
        self.config = config
        self._control_df: pd.DataFrame = pd.DataFrame()
        self._test_df: pd.DataFrame = pd.DataFrame()

        if control_df is not None and test_df is not None:
            self._load_existing_data(control_df, test_df)
        else:
            self.generate_synthetic_data()

        logger.info(f"ABTestDataSet ready: Control samples={len(self._control_df)}, Test samples={len(self._test_df)}")

    def _load_existing_data(self, control_df: pd.DataFrame, test_df: pd.DataFrame):
        """Internal method to load existing dataframes."""
        if 'converted' not in control_df.columns or 'converted' not in test_df.columns:
            raise ValueError("Both control_df and test_df must contain a 'converted' column.")
        # Ensure 'converted' column is numeric (0 or 1)
        if not pd.api.types.is_numeric_dtype(control_df['converted']) or \
           not pd.api.types.is_numeric_dtype(test_df['converted']):
            raise ValueError("The 'converted' column in existing data must be numeric (0 or 1).")

        self._control_df = control_df.copy()
        self._test_df = test_df.copy()
        # Update config n_control/n_test if using existing data, for consistency in reporting
        self.config.n_control = len(self._control_df)
        self.config.n_test = len(self._test_df)
        logger.info("ABTestDataSet loaded from existing data.")


    def generate_synthetic_data(self):
        """
        Generates synthetic A/B test data based on the provided configuration.
        """
        if self.config.random_seed is not None:
            np.random.seed(self.config.random_seed)

        # Control Group Data
        control_conversions = np.random.binomial(1, self.config.baseline_conversion_rate, self.config.n_control)
        self._control_df = pd.DataFrame({
            'user_id': range(self.config.n_control),
            'group': 'control',
            'converted': control_conversions
        })

        # Test Group Data
        test_conversion_rate = self.config.baseline_conversion_rate + self.config.expected_uplift
        test_conversion_rate = min(test_conversion_rate, 1.0) # Cap at 1.0
        test_conversions = np.random.binomial(1, test_conversion_rate, self.config.n_test)
        self._test_df = pd.DataFrame({
            'user_id': range(self.config.n_control, self.config.n_control + self.config.n_test),
            'group': 'test',
            'converted': test_conversions
        })
        logger.info("ABTestDataSet generated synthetic data.")

    def get_control_data(self) -> pd.DataFrame:
        """Returns the control group DataFrame."""
        return self._control_df

    def get_test_data(self) -> pd.DataFrame:
        """Returns the test group DataFrame."""
        return self._test_df

    def get_combined_data(self) -> pd.DataFrame:
        """Returns a concatenated DataFrame of both control and test groups."""
        return pd.concat([self._control_df, self._test_df], ignore_index=True)
