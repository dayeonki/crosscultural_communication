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
  <a href="https://arxiv.org/abs/2604.23842" target="_blank" style="text-decoration:none">
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
  - [Condition Generation](#condition-generation)
  - [Data Preparation](#data-preparation)
  - [R Analysis](#r-analysis)
- [🤲 Citation](#citation)
- [📧 Contact](#contact)

---

<a id="overview"></a>
## 🗺️ Overview

Neologisms and emerging slang are central to daily conversation, yet challenging for non-native speakers (NNS) to interpret and use appropriately in cross-cultural communication with native speakers (NS). 
We study the utility of AI tools in mediating an informal communication scenario through a human-subjects study: NNS participants learn English neologisms with AI support, write messages using the learned word to an NS friend, and judge contextual appropriateness of neologism in two provided writing samples. 

We compare three AI-based support conditions: AI Definition, AI Rewrite into simpler English, AI Explanation of meaning and usage, and Non-AI Dictionary for comparison. We show that AI Explanation yields the largest gains over no support in NS-rated competence, while contextual appropriateness judgments show indifference across support. NNS participants' self-reported perceptions tend to overestimate NS ratings, revealing a mismatch between perceived and actual competence. We further observe a significant gap between NNS- and NS-produced writing, highlighting the limitations of current AI tools and informing design for future tools.

### Results

<div align="center">
  <img width="1201" height="249" alt="Screenshot 2026-04-12 at 4 45 03 PM" src="https://github.com/user-attachments/assets/915d8ffd-eb8f-4c44-8f47-4422c5fa1b11" />
  <img width="400" alt="Screenshot 2026-04-12 at 4 45 46 PM" src="https://github.com/user-attachments/assets/31e95785-b752-4687-b79f-9e332c2df8b2" />
  <img width="400" alt="Screenshot 2026-04-12 at 4 46 02 PM" src="https://github.com/user-attachments/assets/e6652467-2ee3-49af-8565-bf32ce9d823f" />
</div>


<a id="quick_start"></a>
## 🚀 Quick Start

### Condition Generation

Using the prompt in `condition/llm_prompt.py`, we can generate each condition with `condition/llm_query.py`:

```bash
python -u llm_query.py \
  --task TASK_TYPE \
  --input PATH_TO_INPUT_FILE
```

Arguments for condition generation are as follows:
- `--task`: Type of the task (options: `ai-define`, `ai-rewrite`, `ai-explain` depending on the condition)
- `--input`: Path to input data file


### Data Preparation

For each of the generated conditions, we prepare the final set of 8 neologisms using their error rates to ensure that each condition includes a relatively balanced number of examples with both correct and incorrect AI outputs.

We can compute each condition's error rate using `data/get_error_rate.py`:

```bash
python -u get_error_rate.py \
  --input_path PATH_TO_INPUT_FILE \
  --output_path PATH_TO_OUTPUT_FILE \
  --reference_csv PATH_WITH_GROUND_TRUTH \
  --reference_dict_jsonl PATH_TO_GROUND_TRUTH_JSONL \
  --task TASK_TYPE
```

Arguments for computing error rates are as follows:
- `--input_path`: Path to input data file (each jsonl in `data/per_condition/*`)
- `--output_path`: Path to output save file (each jsonl in `data/error_rate/*`)
- `--reference_csv`: Path to csv file used as reference (`data/per_condition/ref_dictionary_page.csv`)
- `--reference_dict_jsonl`: Path to jsonl file used as reference (`data/per_condition/nonai_dictionary.jsonl`)
- `--task`: Type of the task (options: `define`, `rewrite`, `explain` depending on the condition)


### R Analysis

R analyses for the paper are provided in `analysis/main_analysis.html`.
Participant data files are not included in this repository for privacy reasons. If you are interested in the data, please contact the authors.

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
