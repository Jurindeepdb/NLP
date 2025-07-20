This project showcases a complete workflow for fine-tuning a MarianMT model from Helsinki-NLP to translate from Assamese to English. The training is done using TensorFlow and Hugging Face's Transformers library.

## Steps to Run

**1. Create and Activate Conda Environment**

```bash
conda env create -f environment.yml
conda activate matrasen
```

**2. Launch the Notebook**

Run the notebook in your local Jupyter environment:

```bash
jupyter notebook hftransfinal.ipynb
```

## Use your own dataset

**Clean Your Dataset**

If you want to use your own parallel dataset:

* Place your raw Assamese–English sentence pairs in a TSV file.
* Use the provided script:

```bash
python cleaner.py --input your_raw_data.tsv --output cleaned_dataset.tsv
```

Then re-run the notebook using the newly cleaned file.

**Dataset Format**

Your dataset should be a tab-separated `.tsv` file with:

```
as<TAB>en
```

Where:

* `as`: Assamese sentence
* `en`: Corresponding english sentence

## References

This project builds on the following resources:

- **Model**:  
  [Helsinki-NLP/opus-mt-mul-en](https://huggingface.co/Helsinki-NLP/opus-mt-mul-en)  
  A multilingual translation model from the OPUS project, used here for transfer learning and finetuning on Assamese-to-English translation.

- **Codebase Inspiration**:  
  [entbappy/NLP-Projects-Notebooks](https://github.com/entbappy/NLP-Projects-Notebooks)  
  Parts of the notebook structure and training pipeline were adapted from this repository.

