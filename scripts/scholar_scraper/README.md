
# Env

~/miniconda3/bin/conda init zsh

conda create -n latex python=3.9 -y

conda activate latex

pip install ipdb ipython
pip install easydict

pip install scholarly bibtexparser pandas

# Run

python scripts/scholar_scraper/main.py scripts/scholar_scraper/conf/test_papers.txt debug_output/output.bib
