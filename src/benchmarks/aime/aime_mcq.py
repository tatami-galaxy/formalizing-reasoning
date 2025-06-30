from dataclasses import dataclass, field
from tqdm.auto import tqdm
import csv
import random

from transformers import (
    HfArgumentParser,
    AutoModelForCausalLM,
    AutoTokenizer,
)

from datasets import load_dataset


@dataclass
class GenerationArguments:

    runs: int = field(default=8)
    num_options: int = field(default=4) 
    temperature: float = field(default=0.6)
    top_k: int = field(default=20)          
    top_p: float = field(default=0.95)    
    max_new_tokens: int = field(default=32768)                     
    mixed_precision: str = field(
        default="fp16",
        metadata={"help": "choose from : ['no', 'fp16', 'bf16', 'fp8']"}
    )
    thinking: bool = field(default=False)

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


def eval(model_args, gen_args, data_args):

    # load dataset
    aime = load_dataset(data_args.dataset_path)
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
    prefix = "Please reason step by step, and put your final answer within \boxed{}. Final answer is among the following comma separated integers : " 

    # number of runs
    runs = gen_args.runs

    # file for results
    data_path = data_args.dataset_path.split('/')[1]
    model_path = '_' + model_args.model_name.split('/')[1]
    think = '_' + 'think' if gen_args.thinking else ''
    mcq_str = '_' + str(gen_args.num_options) + '_options'
    runs_str = '_' + 'runs_' + str(runs)

    filename = data_path + model_path + think + mcq_str + runs_str
    r_file = open(filename+'.csv', 'w', newline ='')
    header = ['ID', 'Answer', 'Generated',]

    with r_file:
        writer = csv.DictWriter(r_file, fieldnames = header)
        writer.writeheader()

        for run in range(runs) : 
            print('run : {}'.format(run+1))

            # eval
            progress_bar = tqdm(range(len(aime)))

            for x in aime:

                p_id = x['ID']
                problem = x['Problem']
                answer = x['Answer']

                # generate other wrong answers for multiple choice format
                # aime answers are between 0 and 999
                # make sure true answer not in options
                num_incorr_options = gen_args.num_options - 1
                options = random.sample(list(range(1000)), num_incorr_options )
                while answer in options:
                    options = random.sample(list(range(1000)), num_incorr_options )
                # now add answer
                options.append(answer)
                # shuffle
                random.shuffle(options)
                # int to str
                options = [str(o) for o in options]
                # add to prefix
                options_prefix = ', '.join(options)
                prefix = prefix + options_prefix + '.'

                # prompt
                messages = [
                    {"role": "system", "content": prefix},
                    {"role": "user", "content": problem}
                ]

                # chat template
                if gen_args.thinking:
                    text = tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True,
                        enable_thinking=True,
                    )
                else:
                    text = tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True,
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

                # write to csv file
                writer.writerow(
                    {'ID' : p_id, 
                    'Answer': answer, 
                    'Generated': content,
                    }
                )

                progress_bar.update(1)




if __name__ == "__main__":

    # parse cl arguments
    parser = HfArgumentParser((ModelArguments, GenerationArguments, DataArguments))
    model_args, gen_args, data_args = parser.parse_args_into_dataclasses()

    # run eval
    eval(model_args, gen_args, data_args)
