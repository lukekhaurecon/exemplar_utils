# Exemplar Utilities 🦾

Some basic files for getting chat completions from OpenAI

## Getting started

### Check python version
First check you have python version 3.11+ installed by running
```sh
$ python --version
```

### Activate virtual environment

If your version of python is 3.11 or greater, open a terminal in this folder and create a virtual environment by running
```sh
$ python -m venv venv
```
and then activate this environment using
```sh
$ source venv/bin/activate
```
in a bash-like terminal or
```ps
$ venv\Scripts\activate.ps1
```
in windows PowerShell.

If you've done this correctly, the text `(venv)` should now appear in your terminal input.

### Install dependencies

Now install the dependencies using
```sh
(venv) $ pip install -r requirements.txt
```
and you should be ready to go.

## Configuration

Ensure you set the Azure OpenAI config variables:
* API_BASE
* API_KEY
* DEPLOYMENT_NAME
appropriately.

## Running Templates

### Chatbot

You can test the chatbot streamlit template by running
```sh
$ streamlit run st_chatbot.py
```
which should open a browser window containing the streamlit application.

### Notebook

Run the command
```sh
$ jupyter lab
```
and it should start jupyter. Open the `Template.ipynb` inside the file explorer to see a template notebook with some basic OpenAI code.
