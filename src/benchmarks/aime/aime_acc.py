from dataclasses import dataclass, field
import pandas as pd

from transformers import HfArgumentParser

@dataclass
class GeneralArguments:
    results_file: str = field(default=None)


if __name__ == "__main__":

    # parse cl arguments
    parser = HfArgumentParser((GeneralArguments))
    args = parser.parse_args_into_dataclasses()[0]
    
    results_df = pd.read_csv(args.results_file)
    answers = results_df['Answer'].values.tolist()
    generations = results_df['Generated'].values.tolist()
    
    # eval
    acc = 0
    incorrect_gen = 0
    for gen, ans in zip(generations, answers):

        # box logic -> change
        box = 'boxed{'
        box_begin = gen.find(box)
        box_end = box_begin + gen[box_begin:].find('}')
        gen_ans = gen[box_begin+len(box):box_end]
        
        try:
            gen_ans= int(gen_ans)
            if gen_ans == ans : acc += 1
        # incorrect gen
        except ValueError:
            incorrect_gen += 1

    print('accuracy : {}'.format(acc/len(generations)))
    print('incorrect generations : {}'.format(incorrect_gen))