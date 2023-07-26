@echo off

REM Step 1: Create a new virtual environment
python -m venv openAiEmbeddingExperiment

REM Step 2: Activate the virtual environment
openAiEmbeddingExperiment\Scripts\activate

REM Step 3: Run main.py within the virtual environment
python main.py

REM Step 4: Deactivate the virtual environment (optional)
deactivate
