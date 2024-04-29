# Schopenhauer (SCH) argumentative agent

## Generate fine-tuning dataset
0. `export MISTRAL_API_KEY=xxx`
1. `python backend\generate_convs.py`
2. `python backend\tree.py`
3. `python backend\conv4train.py`

## Fine-tune
4. Use `fine_tune.ipynb`

## Demo
5. TODO

## Resources
- Pitch deck: [Google Slides](https://docs.google.com/presentation/d/15JW2U2Y1SuPgasuZ5mO-8KWMynflSZjbztj-KGzhNpM/)
- HuggingFace dataset: [schopenhauer-debate](https://huggingface.co/datasets/raphaaal/schopenhauer-debate)
- HuggingFace model: [llama3-8b-schopenhauer](https://huggingface.co/basilePlus/llama3-8b-schopenhauer)
