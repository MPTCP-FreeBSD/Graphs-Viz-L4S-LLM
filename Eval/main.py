import os
from config.settings import GRAPH_SAVE_FOLDER, DATA_SAVE_FOLDER, LOG_FILE_ORIGINAL, LOG_FILE_LLM, SAVE_FORMATS, DPI
from utils.dataframe_utils import create_dataframe,load_logs, extract_data
from utils.plotter import plot_line_comparison, plot_box_comparison

def main():
    eval_tag = "llama_eval"
    # Ensure the save folders exist
    os.makedirs(GRAPH_SAVE_FOLDER, exist_ok=True)
    os.makedirs(DATA_SAVE_FOLDER, exist_ok=True)
    
    # Load and extract data
    original_logs = load_logs(LOG_FILE_ORIGINAL)
    llm_logs = load_logs(LOG_FILE_LLM)
    steps_original, queue_delays_original, packet_lengths_original, losses_original = extract_data(original_logs)
    steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm = extract_data(llm_logs)
    
    # Create DataFrame
    df = create_dataframe(steps_original, queue_delays_original, packet_lengths_original, losses_original,
                          steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm)
    
    # Save processed DataFrame (optional)
    df.to_csv(f"{DATA_SAVE_FOLDER}/processed_data.csv", index=True)

    # Add a tag to the folder for better organization
    tagged_folder = os.path.join(GRAPH_SAVE_FOLDER, eval_tag)

    # Ensure the tagged folder exists
    os.makedirs(tagged_folder, exist_ok=True)
    
    # Plot queue delay comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Original Queue Delay', 'LLM Queue Delay'],
        xlabel='Step Number',
        ylabel='Queue Delay',
        title='Queue Delay Comparison: Original vs LLAMA',
        filename=f"{eval_tag}_queue_delay_comparison",
        folder=tagged_folder,
        formats=SAVE_FORMATS,
        dpi=DPI
    )

    # Plot queue delay box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Original Queue Delay', 'LLM Queue Delay'],
        ylabel='Queue Delay',
        title='Queue Delay Comparison (Box Plot): Original vs LLAMA',
        filename=f"{eval_tag}_queue_delay_box_comparison",
        folder=tagged_folder,
        formats=SAVE_FORMATS,
        dpi=DPI
    )

    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Original Throughput', 'LLM Throughput'],
        xlabel='Step Number',
        ylabel='Throughput',
        title='Throughput Comparison: Original vs LLAMA',
        filename=f"{eval_tag}_throughput_comparison",
        folder=tagged_folder,
        formats=SAVE_FORMATS,
        dpi=DPI
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Original Throughput', 'LLM Throughput'],
        ylabel='Throughput',
        title='Throughput Comparison (Box Plot): Original vs LLAMA',
        filename=f"{eval_tag}_throughput_box_comparison",
        folder=tagged_folder,
        formats=SAVE_FORMATS,
        dpi=DPI
    )


if __name__ == "__main__":
    main()
