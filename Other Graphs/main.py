from plotter import plot_bar
# Pre-defined variables (to be filled by the user)
methods = ['Full Fine-Tune', 'NetLLM', 'L4S-LLM']
trainable_params = [100, 0.31, 1.005]
gpu_memory = [65.88, 27.24, 23.838]

# Plot configurations
PLOT_SAVE_FOLDER = "Graph Output"  # Folder to save plots

# Plot Trainable Parameters
plot_bar(
    data=trainable_params,
    labels=methods,
    ylabel='Trainable Parameters (%)',
    title='Fraction of Trainable Parameters',
    filename="Trainable_Parameters_Graph",
    folder=PLOT_SAVE_FOLDER
)

# Plot GPU Memory Utilization
plot_bar(
    data=gpu_memory,
    labels=methods,
    ylabel='GPU Memory Utilization (GB)',
    title='GPU Memory Utilization',
    filename="GPU_Memory_Utilization_Graph",
    folder=PLOT_SAVE_FOLDER
)

# Data and paths
models = ['Llama2-7B', 'NetLLM']
valid_answer_percentages = [98, 99.96]
times = [0.2, 0.04]  # Example times in seconds

# Plot valid answer percentages
plot_bar(
    data=valid_answer_percentages,
    labels=models,
    ylabel='Generating Valid Answer (%)',
    title='Valid Answer Percentage by Model',
    filename="Valid_Answer_Percentage_Graph",
    folder=PLOT_SAVE_FOLDER
)

# Plot average answer generation times
plot_bar(
    data=times,
    labels=models,
    ylabel='Average Answer Generation Time (s)',
    title='Average Answer Generation Time by Model',
    filename="Answer_Generation_Time_Graph",
    folder=PLOT_SAVE_FOLDER
)