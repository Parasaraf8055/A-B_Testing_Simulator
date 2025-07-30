import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ABTestConfig:
    """
    Configuration parameters for the A/B testing simulation.
    """
    def __init__(self,
                 n_control: int = 1000,
                 n_test: int = 1000,
                 baseline_conversion_rate: float = 0.10,
                 expected_uplift: float = 0.00,
                 alpha: float = 0.05,
                 random_seed: int = 42,
                 alternative_hypothesis: str = 'two-sided'):
        """
        Initializes the A/B test configuration.

        Args:
            n_control (int): Number of users in the control group.
            n_test (int): Number of users in the test group.
            baseline_conversion_rate (float): The base conversion rate for the control group (0.0 to 1.0).
            expected_uplift (float): The absolute increase in conversion rate for the test group (0.0 to 1.0).
            alpha (float): Significance level for hypothesis testing and confidence intervals (e.g., 0.05 for 95% CI).
            random_seed (int): Seed for reproducibility of data generation.
            alternative_hypothesis (str): Defines the alternative hypothesis for the t-test.
                                          Options: 'two-sided', 'less', or 'greater'.
        """
        if not (0 <= baseline_conversion_rate <= 1):
            raise ValueError("Baseline conversion rate must be between 0 and 1.")
        if not (0 <= baseline_conversion_rate + expected_uplift <= 1.0001): # Add small tolerance for float arithmetic
            logger.warning(f"Combined conversion rate ({baseline_conversion_rate + expected_uplift:.2f}) "
                           f"might exceed 1.0. It will be capped at 1.0 during data generation.")
        if n_control <= 0 or n_test <= 0:
            raise ValueError("Sample sizes (n_control, n_test) must be positive integers.")
        if not (0 < alpha < 1):
            raise ValueError("Alpha (significance level) must be between 0 and 1.")
        if alternative_hypothesis not in ['two-sided', 'less', 'greater']:
            raise ValueError("Alternative hypothesis must be 'two-sided', 'less', or 'greater'.")

        self.n_control = n_control
        self.n_test = n_test
        self.baseline_conversion_rate = baseline_conversion_rate
        self.expected_uplift = expected_uplift
        self.alpha = alpha
        self.random_seed = random_seed
        self.alternative_hypothesis = alternative_hypothesis

        logger.info("ABTestConfig initialized successfully.")