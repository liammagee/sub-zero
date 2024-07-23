python llm_bias_2.py
python llm_bias_2_gpt_direct.py
python llm_bias_2_llama3_direct.py


pandoc data/output_gpt-4-turbo_2.md -o data/output_gpt-4-turbo_2.html
pandoc data/output_gpt-4-turbo_4.md -o data/output_gpt-4-turbo_4.html

open data/output_gpt-4-turbo_2.html
open data/output_gpt-4-turbo_4.html



pandoc data/output_claude-3-opus-20240229_1.md -o data/output_claude-3-opus-20240229_1.html
pandoc data/output_claude-3-opus-20240229_3.md -o data/output_claude-3-opus-20240229_3.html

open data/output_claude-3-opus-20240229_1.html
open data/output_claude-3-opus-20240229_3.html


pandoc data/output_llama3-70b-8192_2.md -o data/output_llama3-70b-8192_2.html
pandoc data/output_llama3-70b-8192_4.md -o data/output_llama3-70b-8192_4.html

open data/output_llama3-70b-8192_2.html
open data/output_llama3-70b-8192_4.html


python compare_scores.py
python compare_dichotomous.py
