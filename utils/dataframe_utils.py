import pandas as pd
import json
from config.settings import COL_DICT

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


def create_dataframe(steps_original, queue_delays_original, packet_lengths_original, losses_original, 
                     steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm):
    """Create a DataFrame with extracted data."""
    min_length = min(len(steps_original), len(queue_delays_original), len(packet_lengths_original),
                     len(losses_original), len(steps_llm), len(queue_delays_llm), 
                     len(packet_lengths_llm), len(losses_llm))
    
    data = {
        'Original Loss': losses_original[:min_length],
        'Original Queue Delay': queue_delays_original[:min_length],
        'Original Packet Length': packet_lengths_original[:min_length],
        'LLM Loss': losses_llm[:min_length],
        'LLM Queue Delay': queue_delays_llm[:min_length],
        'LLM Packet Length': packet_lengths_llm[:min_length],
    }
    
    # Add throughput calculations as floats
    data['Original Throughput'] = [
        float(packet) / float(delay) if delay != 0 else 0.0 
        for packet, delay in zip(packet_lengths_original, queue_delays_original)
    ]
    data['LLM Throughput'] = [
        float(packet) / float(delay) if delay != 0 else 0.0 
        for packet, delay in zip(packet_lengths_llm, queue_delays_llm)
    ]
    
    return pd.DataFrame(data, index=steps_original[:min_length])
