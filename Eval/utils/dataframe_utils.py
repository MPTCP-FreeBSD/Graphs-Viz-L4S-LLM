import pandas as pd
import json
from config.settings import COL_DICT
import numpy as np

def load_logs(log_file):
    """Load logs from a JSON file."""
    with open(log_file, 'r') as file:
        return json.load(file)

def extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    for step_log in logs['steps']:
        steps.append(step_log['step'])
        queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
        packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
        losses.append(step_log['test_loss'])
    return steps, queue_delays, packet_lengths, losses

def return_extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    returns = []
    for step_log in logs['steps']:
        steps.append(step_log['step'])
        queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
        packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
        losses.append(step_log['test_loss'])
        returns.append(step_log['returns'][0][0][0])
        # print(step_log['returns'][0][0][0])
    return steps, queue_delays, packet_lengths, losses, returns

import numpy as np
import pandas as pd

def create_dataframe(steps_original, queue_delays_original, packet_lengths_original, losses_original, 
                     steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm):
    """Create a DataFrame with extracted data and calculate CDFs."""
    
    # Ensure the data is of the same length by trimming the longest data set
    min_length = min(len(steps_original), len(queue_delays_original), len(packet_lengths_original),
                     len(losses_original), len(steps_llm), len(queue_delays_llm), 
                     len(packet_lengths_llm), len(losses_llm))
    
    # Create the initial data dictionary
    data = {
        'Original Loss': losses_original[:min_length],
        'Original Queue Delay': queue_delays_original[:min_length],
        'Original Packet Length': packet_lengths_original[:min_length],
        'LLM Loss': losses_llm[:min_length],
        'LLM Queue Delay': queue_delays_llm[:min_length],
        'LLM Packet Length': packet_lengths_llm[:min_length],
    }
    
    # Calculate throughput for Original and LLM
    data['Original Throughput'] = [
        float(packet/1024) / float(delay/1000000) if delay != 0 else 0.0 
        for packet, delay in zip(packet_lengths_original, queue_delays_original)
    ]
    data['LLM Throughput'] = [
        float(packet/1024) / float(delay/1000000) if delay != 0 else 0.0 
        for packet, delay in zip(packet_lengths_llm, queue_delays_llm)
    ]
    
    # Function to calculate CDF
    def calculate_cdf(values):
        sorted_data = np.sort(values)
        cumulative_data = np.cumsum(sorted_data) / np.sum(sorted_data)
        return sorted_data, cumulative_data
    
    # Calculate CDF for each relevant column and store sorted data & cumulative values
    cdf_data = {}
    for column_name in ['Original Loss', 'Original Queue Delay', 'Original Packet Length', 
                        'LLM Loss', 'LLM Queue Delay', 'LLM Packet Length', 
                        'Original Throughput', 'LLM Throughput']:
        values = data[column_name]
        sorted_data, cumulative_data = calculate_cdf(values)
        cdf_data[column_name + ' Sorted'] = sorted_data
        cdf_data[column_name + ' CDF'] = cumulative_data
    
    # Create the CDF DataFrame
    cdf_df = pd.DataFrame(cdf_data)
    
    # Create the main DataFrame
    df = pd.DataFrame(data, index=steps_original[:min_length])
    
    # Convert queue delay columns to appropriate units
    df['Original Queue Delay'] = df['Original Queue Delay'] / 1000000  # Convert microseconds to seconds
    df['LLM Queue Delay'] = df['LLM Queue Delay'] / 1000000  # Convert microseconds to seconds

    # Print summary statistics
    print(df.describe())
    print("-" * 20)
    print(cdf_df.describe())
    
    return df, cdf_df

