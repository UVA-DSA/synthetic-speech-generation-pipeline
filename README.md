# synethic-speech-generation-pipeline
This repository contains code used to generate a synthetic dataset of audio between Emergency Medical Service workers. By modifying the `datagen.py` and `preprocess.py` files, this code can be adapted to generate synethic audio dataset from any text file in a language supported by Google's text-to-speech API. 

The DataGenerator class in `datagen.py` randomly samples all WaveNet voices hosted on Google Cloud. It also randomly samples speaking rates. This code can be modified to sample specific voices, or modify the speaking rate and pitch ranges for the generated audio.

Also provided in the repo is `generate_huggingface_dataset.ipynb` going through the process of creating a custom HuggingFace Audio dataset and uploading it the HF-Hub, where it can be hosted for free.


Note: If you're receiving permission errors when running GCP code, make sure you have added service-account.json path to your environment variables.
`export GOOGLE_APPLICATION_CREDENTIALS=./service-account.json`
