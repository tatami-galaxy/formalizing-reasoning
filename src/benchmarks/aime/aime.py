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
    max_new_tokens: int = field(default=32768)                     
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

    # dataset
    # ID, Problem, Solution, Answer
    aime = aime['train']

    # model
    model = AutoModelForCausalLM.from_pretrained(
        model_args.model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    # generation config
    model.generation_config.temperature = gen_args.temperature
    model.generation_config.top_k = gen_args.top_k
    model.generation_config.top_p = gen_args.top_p

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_args.model_name)

    # COT prompt
    prefix = "Please reason step by step, and put your final answer within \boxed{}. " 

    # get start time
    start_time = timeit.default_timer()

    # eval
    progress_bar = tqdm(range(len(aime)))
    for x in aime:

        problem = x['Problem']
        answer = x['Answer']
        
        # prompt
        messages = [
            {"role": "system", "content": prefix},
            {"role": "user", "content": problem}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # inputs
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        # generate
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=gen_args.max_new_tokens,
        )

        # decode
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # extract answer with format checking
        box = 'boxed{'
        box_begin = content.find(box)
        box_end = box_begin + content[box_begin:].find('}')
        gen_ans = content[box_begin+len(box):box_end]

        print('box_begin : {}'.format(box_begin))
        print('gen_ans : {}, answer : {}'.format(gen_ans, answer))

        # get time elapsed
        elapsed = timeit.default_timer() - start_time
        print('time_elapsed : {}'.format(elapsed))

        progress_bar.update(1)

        quit()



if __name__ == "__main__":

    # parse cl arguments
    parser = HfArgumentParser((ModelArguments, GenerationArguments, DataArguments))
    model_args, gen_args, data_args = parser.parse_args_into_dataclasses()

    # load dataset
    aime = load_dataset(data_args.dataset_path)

    # run eval
    eval(model_args, gen_args, aime)
