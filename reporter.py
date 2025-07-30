import matplotlib.pyplot as plt
import seaborn as sns
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ABTestReporter:
    """
    Generates reports and visualizations for A/B test results.
    Modified to return outputs for Streamlit.
    """
    def __init__(self, analysis_results: dict):
        """
        Initializes the reporter with analysis results from ABTestAnalyzer.
        """
        if not isinstance(analysis_results, dict) or not analysis_results:
            raise ValueError("analysis_results must be a non-empty dictionary.")
        self.results = analysis_results
        self.alpha = self.results.get('alpha', 0.05) # Default if missing from results
        logger.info("ABTestReporter initialized for Streamlit.")

    def get_conversion_rates_plot(self) -> plt.Figure:
        """
        Creates and returns a matplotlib Figure object for conversion rates.
        """
        labels = ['Control', 'Test']
        conversions = [self.results['control_conversion'], self.results['test_conversion']]
        ci_lowers = [self.results['ci_control_lower'], self.results['ci_test_lower']]
        ci_uppers = [self.results['ci_control_upper'], self.results['ci_test_upper']]

        print("conversions:%s ", conversions)

        # Calculate error bar heights
        errors = [[conversions[i] - ci_lowers[i] for i in range(2)],
                  [ci_uppers[i] - conversions[i] for i in range(2)]]
        errors = pd.DataFrame(errors, index=labels, columns=['Lower', 'Upper'])
        
        print(f"conversion rates errors: {errors}")

        fig, ax = plt.subplots(figsize=(10, 7))

        plot_df = pd.DataFrame({
            'Group': labels,
            'Conversions': conversions,
            'Lower': ci_lowers,
            'Upper': ci_uppers,

        })
        

        sns.barplot(x='Group', y='Conversions', data=plot_df, legend=False ,ax=ax, color='skyblue')
        ax.errorbar(x=[0, 1],y=conversions,yerr=errors,fmt='none',c='black',capsize=10)
        ax.set_ylabel('Conversion Rate')
        ax.set_title(f'A/B Test Conversion Rates with {int((1-self.alpha)*100)}% Confidence Intervals')
        ax.set_ylim(0, max(conversions) * 1.2 if max(conversions) * 1.2 > 0.1 else 0.15) # Ensure y-axis starts reasonably
        ax.grid(axis='y', linestyle='--', alpha=0.7)


        # Add p-value and t-stat text
        ax.text(0.5, ax.get_ylim()[1] * 0.95,
                 f"P-value: {self.results['p_value']:.4f}\nT-stat: {self.results['t_statistic']:.2f}",
                 horizontalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.7),
                 transform=ax.transAxes) # Use transform=ax.transAxes for relative position

        logger.info("Conversion rates plot generated.")
        return fig

    def get_summary_markdown_string(self) -> str:
        """
        Generates and returns a detailed textual summary as a Markdown string.
        """
        summary_lines = []
        summary_lines.append(f"## A/B Test Results Summary")
        summary_lines.append(f"\n### Experiment Configuration:")
        summary_lines.append(f"  * Control Group Size:           `{self.results['control_size']}`")
        summary_lines.append(f"  * Test Group Size:              `{self.results['test_size']}`")
        summary_lines.append(f"  * Significance Level (alpha):   `{self.results['alpha']:.3f}`")
        summary_lines.append(f"  * Alternative Hypothesis:       `'{self.results['alternative_hypothesis']}'`")

        summary_lines.append(f"\n### Observed Metrics:")
        summary_lines.append(f"  * Control Conversion Rate:      `{self.results['control_conversion']:.4f}` "
                             f"(`{self.results['ci_control_lower']:.4f}`, `{self.results['ci_control_upper']:.4f}`)")
        summary_lines.append(f"  * Test Conversion Rate:         `{self.results['test_conversion']:.4f}` "
                             f"(`{self.results['ci_test_lower']:.4f}`, `{self.results['ci_test_upper']:.4f}`)")
        summary_lines.append(f"  * Observed Absolute Difference: `{self.results['observed_difference']:.4f}`")
        if self.results['control_conversion'] > 0:
            summary_lines.append(f"  * Observed Relative Difference: `{(self.results['observed_difference'] / self.results['control_conversion']):.2%}`")
        else:
            summary_lines.append(f"  * Observed Relative Difference: `N/A (Control Conversion is 0)`")

        summary_lines.append(f"\n### Statistical Test Results (Welch's t-test):")
        summary_lines.append(f"  * T-statistic:                  `{self.results['t_statistic']:.4f}`")
        summary_lines.append(f"  * P-value:                      `{self.results['p_value']:.4f}`")

        conclusion = ""
        if self.results['p_value'] < self.alpha:
            conclusion = f"The p-value (`{self.results['p_value']:.4f}`) is less than alpha (`{self.alpha:.3f}`).\n" \
                         f"We **reject the null hypothesis**. There is a statistically significant difference " \
                         f"in conversion rates between the control and test groups."
            if self.results['observed_difference'] > 0 and self.results['alternative_hypothesis'] == 'greater':
                 conclusion += "\n_The test group showed a statistically significant **increase**._"
            elif self.results['observed_difference'] < 0 and self.results['alternative_hypothesis'] == 'less':
                 conclusion += "\n_The test group showed a statistically significant **decrease**._"
            elif self.results['alternative_hypothesis'] == 'two-sided':
                 conclusion += "\n_There is a statistically significant difference (positive or negative)._"
        else:
            conclusion = f"The p-value (`{self.results['p_value']:.4f}`) is greater than or equal to alpha (`{self.alpha:.3f}`).\n" \
                         f"We **fail to reject the null hypothesis**. There is no statistically significant " \
                         f"difference in conversion rates observed between the control and test groups."

        summary_lines.append(f"\n### Conclusion:\n{conclusion}")
        logger.info("Textual report string generated.")
        return "\n".join(summary_lines)
