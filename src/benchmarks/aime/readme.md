#### Run models with default configs

#### gen

uv run python aime.py --dataset_path Maxwell-Jia/AIME_2024 --model_name Qwen/Qwen2.5-Math-7B-Instruct --temperature 0.6 --top_k 20 --top_p 0.95 --runs 8

uv run python aime.py --dataset_path Maxwell-Jia/AIME_2024 --model_name Qwen/Qwen3-8B --temperature 0.6 --top_k 20 --top_p 0.95 --runs 8

uv run python aime.py --dataset_path Maxwell-Jia/AIME_2024 --model_name Qwen/Qwen3-8B --temperature 0.6 --top_k 20 --top_p 0.95 --thinking --runs 8

uv run python aime.py --dataset_path Maxwell-Jia/AIME_2024 --model_name Qwen/Qwen3-8B --temperature 0.6 --top_k 20 --top_p 0.95 --max_new_tokens 38912 --runs 8

#### gen mcq

uv run python aime_mcq.py --dataset_path Maxwell-Jia/AIME_2024 --model_name Qwen/Qwen3-8B --temperature 0.6 --top_k 20 --top_p 0.95 --max_new_tokens 38912 --num_options 4 --runs 8

#### eval

uv run python aime_acc.py --results_file `result_file`