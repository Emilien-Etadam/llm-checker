"""
Simplified Model Database for LLM Checker
Contains popular Ollama models with different quantizations
"""


def get_popular_models():
    """
    Returns a curated list of popular Ollama models
    Each model has: name, family, params_b, size_gb, quantization, context_length
    """
    models = [
        # Qwen 2.5 Coder - Top coding model
        {'name': 'qwen2.5-coder:7b-instruct-q8_0', 'family': 'qwen2.5-coder', 'params_b': 7, 'size_gb': 7.6, 'quantization': 'Q8_0', 'context_length': 32768},
        {'name': 'qwen2.5-coder:7b-instruct-q6_k', 'family': 'qwen2.5-coder', 'params_b': 7, 'size_gb': 6.0, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'qwen2.5-coder:7b-instruct-q4_k_m', 'family': 'qwen2.5-coder', 'params_b': 7, 'size_gb': 4.7, 'quantization': 'Q4_K_M', 'context_length': 32768},
        {'name': 'qwen2.5-coder:14b-instruct-q8_0', 'family': 'qwen2.5-coder', 'params_b': 14, 'size_gb': 15.2, 'quantization': 'Q8_0', 'context_length': 32768},
        {'name': 'qwen2.5-coder:14b-instruct-q6_k', 'family': 'qwen2.5-coder', 'params_b': 14, 'size_gb': 11.8, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'qwen2.5-coder:14b-instruct-q4_k_m', 'family': 'qwen2.5-coder', 'params_b': 14, 'size_gb': 8.9, 'quantization': 'Q4_K_M', 'context_length': 32768},
        {'name': 'qwen2.5-coder:32b-instruct-q6_k', 'family': 'qwen2.5-coder', 'params_b': 32, 'size_gb': 26.5, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'qwen2.5-coder:32b-instruct-q4_k_m', 'family': 'qwen2.5-coder', 'params_b': 32, 'size_gb': 20.0, 'quantization': 'Q4_K_M', 'context_length': 32768},

        # Qwen 2.5 - General purpose
        {'name': 'qwen2.5:7b-instruct-q8_0', 'family': 'qwen2.5', 'params_b': 7, 'size_gb': 7.7, 'quantization': 'Q8_0', 'context_length': 128000},
        {'name': 'qwen2.5:7b-instruct-q6_k', 'family': 'qwen2.5', 'params_b': 7, 'size_gb': 6.0, 'quantization': 'Q6_K', 'context_length': 128000},
        {'name': 'qwen2.5:7b-instruct-q4_k_m', 'family': 'qwen2.5', 'params_b': 7, 'size_gb': 4.7, 'quantization': 'Q4_K_M', 'context_length': 128000},
        {'name': 'qwen2.5:14b-instruct-q8_0', 'family': 'qwen2.5', 'params_b': 14, 'size_gb': 15.8, 'quantization': 'Q8_0', 'context_length': 128000},
        {'name': 'qwen2.5:14b-instruct-q6_k', 'family': 'qwen2.5', 'params_b': 14, 'size_gb': 12.0, 'quantization': 'Q6_K', 'context_length': 128000},
        {'name': 'qwen2.5:14b-instruct-q4_k_m', 'family': 'qwen2.5', 'params_b': 14, 'size_gb': 9.0, 'quantization': 'Q4_K_M', 'context_length': 128000},
        {'name': 'qwen2.5:32b-instruct-q6_k', 'family': 'qwen2.5', 'params_b': 32, 'size_gb': 27.0, 'quantization': 'Q6_K', 'context_length': 128000},
        {'name': 'qwen2.5:32b-instruct-q4_k_m', 'family': 'qwen2.5', 'params_b': 32, 'size_gb': 20.5, 'quantization': 'Q4_K_M', 'context_length': 128000},
        {'name': 'qwen2.5:72b-instruct-q4_k_m', 'family': 'qwen2.5', 'params_b': 72, 'size_gb': 45.0, 'quantization': 'Q4_K_M', 'context_length': 128000},

        # Llama 3.3
        {'name': 'llama3.3:70b-instruct-q8_0', 'family': 'llama3.3', 'params_b': 70, 'size_gb': 75.0, 'quantization': 'Q8_0', 'context_length': 128000},
        {'name': 'llama3.3:70b-instruct-q6_k', 'family': 'llama3.3', 'params_b': 70, 'size_gb': 57.0, 'quantization': 'Q6_K', 'context_length': 128000},
        {'name': 'llama3.3:70b-instruct-q4_k_m', 'family': 'llama3.3', 'params_b': 70, 'size_gb': 43.0, 'quantization': 'Q4_K_M', 'context_length': 128000},

        # Llama 3.2
        {'name': 'llama3.2:1b-instruct-q8_0', 'family': 'llama3.2', 'params_b': 1, 'size_gb': 1.3, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'llama3.2:1b-instruct-q4_k_m', 'family': 'llama3.2', 'params_b': 1, 'size_gb': 0.9, 'quantization': 'Q4_K_M', 'context_length': 131072},
        {'name': 'llama3.2:3b-instruct-q8_0', 'family': 'llama3.2', 'params_b': 3, 'size_gb': 3.4, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'llama3.2:3b-instruct-q6_k', 'family': 'llama3.2', 'params_b': 3, 'size_gb': 2.6, 'quantization': 'Q6_K', 'context_length': 131072},
        {'name': 'llama3.2:3b-instruct-q4_k_m', 'family': 'llama3.2', 'params_b': 3, 'size_gb': 2.0, 'quantization': 'Q4_K_M', 'context_length': 131072},

        # Llama 3.1
        {'name': 'llama3.1:8b-instruct-q8_0', 'family': 'llama3.1', 'params_b': 8, 'size_gb': 8.5, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'llama3.1:8b-instruct-q6_k', 'family': 'llama3.1', 'params_b': 8, 'size_gb': 6.6, 'quantization': 'Q6_K', 'context_length': 131072},
        {'name': 'llama3.1:8b-instruct-q4_k_m', 'family': 'llama3.1', 'params_b': 8, 'size_gb': 5.0, 'quantization': 'Q4_K_M', 'context_length': 131072},
        {'name': 'llama3.1:70b-instruct-q6_k', 'family': 'llama3.1', 'params_b': 70, 'size_gb': 57.0, 'quantization': 'Q6_K', 'context_length': 131072},
        {'name': 'llama3.1:70b-instruct-q4_k_m', 'family': 'llama3.1', 'params_b': 70, 'size_gb': 43.0, 'quantization': 'Q4_K_M', 'context_length': 131072},

        # DeepSeek R1
        {'name': 'deepseek-r1:7b-q8_0', 'family': 'deepseek-r1', 'params_b': 7, 'size_gb': 7.9, 'quantization': 'Q8_0', 'context_length': 32768},
        {'name': 'deepseek-r1:7b-q6_k', 'family': 'deepseek-r1', 'params_b': 7, 'size_gb': 6.1, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'deepseek-r1:7b-q4_k_m', 'family': 'deepseek-r1', 'params_b': 7, 'size_gb': 4.7, 'quantization': 'Q4_K_M', 'context_length': 32768},
        {'name': 'deepseek-r1:14b-q8_0', 'family': 'deepseek-r1', 'params_b': 14, 'size_gb': 15.5, 'quantization': 'Q8_0', 'context_length': 32768},
        {'name': 'deepseek-r1:14b-q6_k', 'family': 'deepseek-r1', 'params_b': 14, 'size_gb': 12.0, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'deepseek-r1:14b-q4_k_m', 'family': 'deepseek-r1', 'params_b': 14, 'size_gb': 9.0, 'quantization': 'Q4_K_M', 'context_length': 32768},
        {'name': 'deepseek-r1:70b-q4_k_m', 'family': 'deepseek-r1', 'params_b': 70, 'size_gb': 42.0, 'quantization': 'Q4_K_M', 'context_length': 32768},

        # DeepSeek Coder V2
        {'name': 'deepseek-coder-v2:16b-lite-instruct-q8_0', 'family': 'deepseek-coder-v2', 'params_b': 16, 'size_gb': 16.5, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'deepseek-coder-v2:16b-lite-instruct-q6_k', 'family': 'deepseek-coder-v2', 'params_b': 16, 'size_gb': 12.8, 'quantization': 'Q6_K', 'context_length': 131072},
        {'name': 'deepseek-coder-v2:16b-lite-instruct-q4_k_m', 'family': 'deepseek-coder-v2', 'params_b': 16, 'size_gb': 9.8, 'quantization': 'Q4_K_M', 'context_length': 131072},

        # Phi-4
        {'name': 'phi4:14b-q8_0', 'family': 'phi-4', 'params_b': 14, 'size_gb': 15.0, 'quantization': 'Q8_0', 'context_length': 16384},
        {'name': 'phi4:14b-q6_k', 'family': 'phi-4', 'params_b': 14, 'size_gb': 11.5, 'quantization': 'Q6_K', 'context_length': 16384},
        {'name': 'phi4:14b-q4_k_m', 'family': 'phi-4', 'params_b': 14, 'size_gb': 8.8, 'quantization': 'Q4_K_M', 'context_length': 16384},

        # Phi-3.5
        {'name': 'phi3.5:3.8b-mini-instruct-q8_0', 'family': 'phi-3.5', 'params_b': 3.8, 'size_gb': 4.2, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'phi3.5:3.8b-mini-instruct-q4_k_m', 'family': 'phi-3.5', 'params_b': 3.8, 'size_gb': 2.5, 'quantization': 'Q4_K_M', 'context_length': 131072},

        # Gemma 2
        {'name': 'gemma2:9b-instruct-q8_0', 'family': 'gemma2', 'params_b': 9, 'size_gb': 9.8, 'quantization': 'Q8_0', 'context_length': 8192},
        {'name': 'gemma2:9b-instruct-q6_k', 'family': 'gemma2', 'params_b': 9, 'size_gb': 7.6, 'quantization': 'Q6_K', 'context_length': 8192},
        {'name': 'gemma2:9b-instruct-q4_k_m', 'family': 'gemma2', 'params_b': 9, 'size_gb': 5.8, 'quantization': 'Q4_K_M', 'context_length': 8192},
        {'name': 'gemma2:27b-instruct-q6_k', 'family': 'gemma2', 'params_b': 27, 'size_gb': 22.0, 'quantization': 'Q6_K', 'context_length': 8192},
        {'name': 'gemma2:27b-instruct-q4_k_m', 'family': 'gemma2', 'params_b': 27, 'size_gb': 16.5, 'quantization': 'Q4_K_M', 'context_length': 8192},

        # Mistral
        {'name': 'mistral:7b-instruct-v0.3-q8_0', 'family': 'mistral', 'params_b': 7, 'size_gb': 7.7, 'quantization': 'Q8_0', 'context_length': 32768},
        {'name': 'mistral:7b-instruct-v0.3-q6_k', 'family': 'mistral', 'params_b': 7, 'size_gb': 6.0, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'mistral:7b-instruct-v0.3-q4_k_m', 'family': 'mistral', 'params_b': 7, 'size_gb': 4.7, 'quantization': 'Q4_K_M', 'context_length': 32768},

        # Mixtral
        {'name': 'mixtral:8x7b-instruct-v0.1-q6_k', 'family': 'mixtral', 'params_b': 47, 'size_gb': 38.0, 'quantization': 'Q6_K', 'context_length': 32768},
        {'name': 'mixtral:8x7b-instruct-v0.1-q4_k_m', 'family': 'mixtral', 'params_b': 47, 'size_gb': 29.0, 'quantization': 'Q4_K_M', 'context_length': 32768},

        # CodeLlama
        {'name': 'codellama:7b-instruct-q8_0', 'family': 'codellama', 'params_b': 7, 'size_gb': 7.4, 'quantization': 'Q8_0', 'context_length': 16384},
        {'name': 'codellama:7b-instruct-q4_k_m', 'family': 'codellama', 'params_b': 7, 'size_gb': 4.5, 'quantization': 'Q4_K_M', 'context_length': 16384},
        {'name': 'codellama:13b-instruct-q8_0', 'family': 'codellama', 'params_b': 13, 'size_gb': 13.8, 'quantization': 'Q8_0', 'context_length': 16384},
        {'name': 'codellama:13b-instruct-q4_k_m', 'family': 'codellama', 'params_b': 13, 'size_gb': 8.5, 'quantization': 'Q4_K_M', 'context_length': 16384},

        # Yi Coder
        {'name': 'yi-coder:9b-chat-q8_0', 'family': 'yi-coder', 'params_b': 9, 'size_gb': 9.6, 'quantization': 'Q8_0', 'context_length': 131072},
        {'name': 'yi-coder:9b-chat-q4_k_m', 'family': 'yi-coder', 'params_b': 9, 'size_gb': 5.8, 'quantization': 'Q4_K_M', 'context_length': 131072},

        # Smaller models for lower-end hardware
        {'name': 'tinyllama:1.1b-chat-v1.0-q8_0', 'family': 'tinyllama', 'params_b': 1.1, 'size_gb': 1.3, 'quantization': 'Q8_0', 'context_length': 2048},
        {'name': 'tinyllama:1.1b-chat-v1.0-q4_k_m', 'family': 'tinyllama', 'params_b': 1.1, 'size_gb': 0.8, 'quantization': 'Q4_K_M', 'context_length': 2048},
        {'name': 'smollm:360m-instruct-q8_0', 'family': 'smollm', 'params_b': 0.36, 'size_gb': 0.4, 'quantization': 'Q8_0', 'context_length': 2048},
        {'name': 'smollm:1.7b-instruct-q8_0', 'family': 'smollm', 'params_b': 1.7, 'size_gb': 1.9, 'quantization': 'Q8_0', 'context_length': 2048},
        {'name': 'smollm:1.7b-instruct-q4_k_m', 'family': 'smollm', 'params_b': 1.7, 'size_gb': 1.2, 'quantization': 'Q4_K_M', 'context_length': 2048},
    ]

    return models
