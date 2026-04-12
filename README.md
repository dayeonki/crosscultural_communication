<div align="center">

 # <i>Reheat Nachos</i> for Dinner? Evaluating AI Support for Cross-Cultural Communication of Neologisms

<p align="center">
<img width="1159" height="460" alt="Screenshot 2026-04-12 at 4 38 21 PM" src="https://github.com/user-attachments/assets/7d699613-28b3-4475-8452-d7542fc3c192" />
</p>

<a href=https://dayeonki.github.io/>Dayeon Ki</a><sup>\*</sup>, <a href=https://houyu0930.github.io/>Yu Hou</a><sup>\*</sup>, <a href=https://rudinger.github.io/>Rachel Rudinger</a>, <a href=https://users.umiacs.umd.edu/~hal3/>Hal Daumé III</a>, <a href=https://www.cs.umd.edu/~marine/>Marine Carpuat<a>, <a href=https://www.fmyang.com/>Fumeng Yang</a> <br>
University of Maryland <br>
*: Equal contribution
<br>

This repository contains the code and dataset for our ACL Findings 2026 paper <br> **Reheat Nachos for Dinner? Evaluating AI Support for Cross-Cultural Communication of Neologisms**.

<p>
  <a href="" target="_blank" style="text-decoration:none">
    <img src="https://img.shields.io/badge/arXiv-Paper-b31b1b?style=flat&logo=arxiv" alt="arXiv">
  </a>
</p>

</div>

---
## 👾 TL;DR
We conduct human-subjects study to assess the promises and gaps of AI tools in supporting informal cross-cultural communication between non-native and native English speakers.

## 📰 News
- **`2026-04-07`** Our paper is accepted to **ACL Findings 2026**!


## ✏️ Content
- [🗺️ Overview](#overview)
- [🚀 Quick Start](#quick_start)
  - [Data Preparation](#data-preparation)
  - [Condition Generation](#condition-generation)
  - [R Analysis](#r-analysis)
- [🤲 Citation](#citation)
- [📧 Contact](#contact)

---

<a id="overview"></a>
## 🗺️ Overview

Neologisms and emerging slang are central to daily conversation, yet challenging for non-native speakers (NNS) to interpret and use appropriately in cross-cultural communication with native speakers (NS). NNS increasingly make use of Artificial Intelligence (AI) tools to learn these words. We study the utility of such tools in mediating an informal communication scenario through a human-subjects study (N=234): NNS participants learn English neologisms with AI support, write messages using the learned word to an NS friend, and judge contextual appropriateness of neologism in two provided writing samples. Using both NS evaluator-rated communicative competence of NNS-produced writing and NNS' contextual appropriateness judgments, we compare three AI-based support conditions: AI Definition, AI Rewrite into simpler English, AI Explanation of meaning and usage, and Non-AI Dictionary for comparison. We show that AI Explanation yields the largest gains over no support in NS-rated competence, while contextual appropriateness judgments show indifference across support. NNS participants' self-reported perceptions tend to overestimate NS ratings, revealing a mismatch between perceived and actual competence. We further observe a significant gap between NNS- and NS-produced writing, highlighting the limitations of current AI tools and informing design for future tools.

### Results

<div align="center">
  <img width="1201" height="249" alt="Screenshot 2026-04-12 at 4 45 03 PM" src="https://github.com/user-attachments/assets/915d8ffd-eb8f-4c44-8f47-4422c5fa1b11" />
  <img width="400" alt="Screenshot 2026-04-12 at 4 45 46 PM" src="https://github.com/user-attachments/assets/31e95785-b752-4687-b79f-9e332c2df8b2" />
  <img width="400" alt="Screenshot 2026-04-12 at 4 46 02 PM" src="https://github.com/user-attachments/assets/e6652467-2ee3-49af-8565-bf32ce9d823f" />
</div>


<a id="quick_start"></a>
## 🚀 Quick Start

### Data Preparation
We can automatically annotate error spans, error type, and severity level using [InstructScore](https://github.com/xu1998hz/SEScore3/tree/main). InstructScore is an explainable text generation evaluation metric, which fine-tunes LLaMA to predict MQM style fine-grained error annotations. This metric only supports Chinese-English.

```bash
python -u code/detect-instructscore.py \
  --instructscore_path $PATH_TO_INPUT_FILE \
  --output_path $PATH_TO_OUTPUT_FILE
```

Arguments for the InstructScore detection script are as follows,
- `--instructscore_path`: Path to input data file
- `--output_path`: Save path of output file (after detection)


We can also automatically annotate error spans and severity level using [xCOMET](https://huggingface.co/Unbabel/XCOMET-XL). xCOMET is an automatic evaluation and quality estimation tool, which fine-tunes XLM-RoBERTa to predict both MQM and Direct Assessment annotations of MT quality. This metric supports all language pairs.
```bash
python -u code/detect-xcomet.py \
  --model_name_hf Unbabel/XCOMET-XL \
  --input_path $PATH_TO_INPUT_FILE \
  --output_path $PATH_TO_OUTPUT_FILE \
  --cache_dir $PATH_TO_CACHE_DIR
```

Arguments for the xCOMET detection script are as follows,
- `--model_name_hf`: The name or path of a transformers-based pre-trained checkpoint. You can directly refer to the Huggingface model `Unbabel/XCOMET-XL` (XL) or `Unbabel/XCOMET-XXL` (XXL).
- `--input_path`: Path to input data file
- `--output_path`: Save path of output file (after detection)
- `--cache_dir`: Cache directory of pre-trained model checkpoints


### Condition Generation
We provide a source text, a MT output and depending on the feedback level, condition some feedback on the quality of MT. We opt to construct our prompting templates in English, rather than the target language, likely due to the greater prevalence of English in the pre-training data.

Our experiment encompasses the following forms of feedback for each model:
  - `Generic`: The model is prompted to improve the initial translation without any specific external feedback.
  - `Score-based`: A single scalar MQM score, reflecting the initial translation's overall quality. We normalize the scores on a range from 0 to 100.
  - `Fine-grained` : Fine-grained feedback (error span, type, severity level) in the MQM style. We use below three methods, which use different severity level ranges.
     - `MQM`: human annotation from the MQM WMT22 dataset.
     - `InstructScore`
     - `xCOMET` (do not provide error type information)

#### (1) Prompting
We set the temperature to 0 for greedy decoding throughout all experiments. For few-shot prompting, we randomly sample in-context examples. To run prompting on LLaMA models,
```
python -u code/prompting/prompt-mqm.py \
  --model_name_hf meta-llama/Llama-2-7b \
  --model_name llama-2-7b \
  --information_type generic \
  --input_path $PATH_TO_INPUT_FILE \
  --output_path $PATH_TO_OUTPUT_FILE \
  --cache_dir $PATH_TO_CACHE_DIR \
  --pool_data_path $PATH_TO_POOL_DATASET \
  --few_shot_type random \
  --num_few_shots $NUM_FEW_SHOTS \
  --source_lang $SOURCE_LANGUAGE \
  --target_lang $TARGET_LANGUAGE
```

Arguments for the prompting script are as follows,
- `--model_name_hf`: Model name from Huggingface. We consider `meta-llama/Llama-2-7b-hf` and `meta-llama/Llama-2-13b-hf`
- `--model_name`: Model nickname used for saving
- `--information_type`: Granularity level of feedback {generic, score, fine-grained}
- `--input_path`: Path to input data file
- `--output_path`: Save path of output file
- `--cache_dir`: Cache directory of pre-trained model checkpoints
- `--pool_data_path`: Path to dataset used for in-context examples (only use for few-shot prompting)
- `--few_shot_type`: How to construct in-context examples {random, error-aligned}
- `--num_few_shots`: Number of in-context examples
- `--source_lang`: Source language in ISO code (ex. en)
- `--target_lang`: Target language in ISO code


#### (2) Evaluation
We report three metrics as our evaluation. Scores for all these metrics are reported in the 0-1 range.
- `BLUE`: Implemented from `sacrebleu` toolkit with exponential smoothing
- `Translation Edit Rate` (TER): The minimum number of edits needed to change a hypothesis so that it exactly matches one of the references, normalized by the average length of the references.
- `COMET (DA)`: Neural metric, reference-based score.
```
python -u code/prompting/evaluate.py \
  --generic_input_path $GENERIC_OUTPUT_FILE \
  --score_input_path $SCORE_OUTPUT_FILE \
  --specific_input_path $MQM_OUTPUT_FILE \
  --instructscore_input_path $INSTRUCTSCORE_OUTPUT_FILE \
  --xcomet_input_path $XCOMET_OUTPUT_FILE \
```

Arguments for the evaluation script are as follows,
- `--generic_input_path`: Path to generation output file using generic feedback
- `--score_input_path`: Path to generation output file using score feedback
- `--specific_input_path`: Path to generation output file using MQM fine-grained feedback
- `--instructscore_input_path`: Path to generation output file using InstructScore fine-grained feedback
- `--xcomet_input_path`: Path to generation output file using xCOMET fine-grained feedback

Exemplar output of evaluation are as follows,
```
DEVICE:  cuda:0
+----------------------+----------+---------------------+------------------------+
|                      |   Metric | t-statistics        | p-value                |
+======================+==========+=====================+========================+
| BLEU (Original)      |     0.43 | -                   | -                      |
+----------------------+----------+---------------------+------------------------+
| BLEU (Generic)       |     0.61 | -16.86252170477477  | 3.2960479662367076e-40 |
+----------------------+----------+---------------------+------------------------+
| BLEU (Score)         |     0.59 | -31.57232245321125  | 4.3125238432423411e-41 |
+----------------------+----------+---------------------+------------------------+
| BLEU (Fine-grained)  |     0.6  | -17.374328057092807 | 9.418568326469382e-42  |
+----------------------+----------+---------------------+------------------------+
...
```

### R Analysis
For fine-tuning with error annotations, we construct MQM error annotations into instruction-following style. We adopt QLoRA, quantized version of LoRA for parameter-efficient fine-tuning.
| LoRA config | Value |
| - | - |
LoRA rank | 16
Scaling parameter | 32
Dropout probability | 0.05

Fine-tuning config | Value 
| - | - |
Optimizer | Adam
Initial learning rate | 2e-4
Batch size | 2
Gradient accumulation | 4 steps
Warmup phase | 20 steps
Train epochs | 5

Below are the preliminary steps for making fine-tuning datasets. We reformulate all annotations in an instruction-following style. We automatically filter out instances that share identical source or target sentences with those in the test set to ensure a clean train/test separation.
#### Step 0. Making Fine-tuning Templates
```
python -u code/fine-tuning/make-template.py \
  --input_path $PATH_TO_MQM_DATA \
  --output_path $PATH_TO_OUTPUT_FILE \
  --test_path $TEST_DATA_FILE \
  --dev_path $DEV_DATA_FILE \
  --source_lang $SOURCE_LANGUAGE \
  --target_lang $TARGET_LANGUAGE
```

Arguments for template creation script are as follows,
- `--input_path`: Path to input data file
- `--output_path`: Save path of output file
- `--test_path`: Path to test data file
- `--dev_path`: Path to development data file
- `--source_lang`: Source language in ISO code (ex. en)
- `--target_lang`: Target language in ISO code


#### Step 1. Randomly Shuffle Instructions
```
python -u code/fine-tuning/random-shuffle.py \
  --file_path $PATH_TO_INSTRUCTIONS \
  --output_path $PATH_TO_OUTPUT_FILE
```
After shuffling, we push the dataset to Huggingface to load efficiently during fine-tuning.

#### Step 2. Fine-tune with LLaMA-2 Models
We can fine-tune with LLaMA-2 7B (`fine-tune-7b.py`) or 13B (`fine-tune-13b.py`). After fine-tuning, the script will produce (1) Trainer file, (2) Tokenizer file of the instruction fine-tuned model.
```
python -u code/fine-tuning/fine-tune-7b.py \
  --hf_dataset $PATH_TO_HF_DATASET \
  --output_dir $PATH_TO_OUTPUT_FILE \
  --trainer_save_dir $PATH_TO_OUTPUT_TRAINER \
  --tokenizer_save_dir $PATH_TO_OUTPUT_TOKENIZER \
  --cache_dir $PATH_TO_CACHE_DIR
```

Arguments for fine-tuning script are as follows,
- `--hf_dataset`: Name of the huggingface dataset
- `--output_dir`: Save path of output file
- `--trainer_save_dir`: Save path of fine-tuned trainer file
- `--tokenizer_save_dir`: Save path of fine-tuned tokenizer file
- `--cache_dir`: Cache directory of pre-trained model checkpoints or dataset

#### Step 3. Evaluation
We can evaluate with our custom fine-tuned model.
```
python -u code/fine-tuning/evaluate.py \
  --pickle_dir $OUTPUT_TRANSLATIONS_FILE \
  --test_data_path $PATH_TO_OUTPUT_FILE
```

Arguments are as follows,
- `--pickle_dir`: Path to output model pickle file
- `--test_data_path`: Path to input test data file


---

<a id="citation"></a>
## 🤲 Citation
If you find our work useful in your research, please consider citing our work:
```
TBD
```


<a id="contact"></a>
## 📧 Contact
For questions, issues, or collaborations, please reach out to [dayeonki@umd.edu](mailto:dayeonki@umd.edu) or [houyu@umd.edu](mailto:houyu@umd.edu).
