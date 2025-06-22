from dataclasses import dataclass, field
import typing
from typing import List
from tqdm.auto import tqdm
import timeit

import torch

from transformers import (
    HfArgumentParser,
    AutoConfig, 
    AutoModelForCausalLM,
    AutoTokenizer,
)

from datasets import load_dataset


@dataclass
class GenerationArguments:

    temperature: float = field(default=0.6)
    top_k: int = field(default=20)          
    top_p: float = field(default=0.95)                         
    mixed_precision: str = field(
        default="fp16",
        metadata={"help": "choose from : ['no', 'fp16', 'bf16', 'fp8']"}
    )

    def __post_init__(self):
        pass


@dataclass
class DataArguments:

    dataset_path: str = field(
        default="Maxwell-Jia/AIME_2024",
    )


@dataclass
class ModelArguments:

    model_name: str = field(
        default="Qwen/Qwen2.5-Math-7B-Instruct",
    )


def eval(model_args, gen_args, aime):

    print(len(aime['train']))
    print(aime['train'][0]['Answer'])

    step = 0 
    total_time_elapsed = 0
    new_time = 0

    # get start time
    #step_start_time = timeit.default_timer()

    #progress_bar = tqdm(range(len(aime)))

    # get time elapsed
    #elapsed = timeit.default_timer() - step_start_time
    #new_time = new_time + elapsed



if __name__ == "__main__":

    # parse cl arguments
    parser = HfArgumentParser((ModelArguments, GenerationArguments, DataArguments))
    model_args, gen_args, data_args = parser.parse_args_into_dataclasses()

    # load dataset
    aime = load_dataset(data_args.dataset_path)

    # run eval
    eval(model_args, gen_args, aime)
