from rich.text import Text


class Monitor:
    """A monitoring class that tracks metrics during agent execution.
    
    This class is responsible for:
    1. Tracking step durations of agent operations
    2. Counting input and output tokens if the model supports it
    3. Logging metrics using a rich text logger
    
    Attributes:
        step_durations (list): List of durations for each step
        tracked_model: The model being monitored
        logger: Logger instance for output
        total_input_token_count (int): Running total of input tokens
        total_output_token_count (int): Running total of output tokens
    """
    def __init__(self, tracked_model, logger):
        self.step_durations = []
        self.tracked_model = tracked_model
        self.logger = logger
        if getattr(self.tracked_model, "last_input_token_count", "Not found") != "Not found":
            self.total_input_token_count = 0
            self.total_output_token_count = 0

    def get_total_token_counts(self):
        """Returns the total input and output token counts.
        
        Returns:
            dict: Contains total input and output token counts
        """
        return {
            "input": self.total_input_token_count,
            "output": self.total_output_token_count,
        }

    def reset(self):
        """Resets all monitoring metrics to initial values."""
        self.step_durations = []
        self.total_input_token_count = 0
        self.total_output_token_count = 0

    def update_metrics(self, step_log):
        """Update the metrics of the monitor.

        Args:
            step_log ([`AgentStepLog`]): Step log to update the monitor with.
        """
        step_duration = step_log.duration
        self.step_durations.append(step_duration)
        console_outputs = f"[Step {len(self.step_durations) - 1}: Duration {step_duration:.2f} seconds"

        if getattr(self.tracked_model, "last_input_token_count", None) is not None:
            self.total_input_token_count += self.tracked_model.last_input_token_count
            self.total_output_token_count += self.tracked_model.last_output_token_count
            console_outputs += (
                f"| Input tokens: {self.total_input_token_count:,} | Output tokens: {self.total_output_token_count:,}"
            )
        console_outputs += "]"
        self.logger.log(Text(console_outputs, style="dim"), level=1)


__all__ = ["Monitor"]
