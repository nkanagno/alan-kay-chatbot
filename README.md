# How to run and set up
To run the Alan Kay chatbot application, you need to set up your Python environment, configure your OpenAI API key, and then execute it via the command line. Once running, you can freely interact with the Alan Kay chatbot.
## Set up python
First set up your python environment with the following command
```
python -m venv myenv
```
and activate it with
```
source myenv/bin/activate
```
on Linux/Mac users or 
```
myenv\Scripts\activate
```
for window users.

After activation, you can install the applications requirements (python 3.10.0 recommended) with:
```
pip install -r requirements.txt
```

## Configure your OpenAi api key

To configure your OpenAI API key, navigate to the main [OpenAI platform website](https://platform.openai.com/).

After obtaining your API key, add it to a `.env` file in your project root with the following format:
```
OPENAI_API_KEY=your_api_key_here
```

## Run Custom API
The following command runs a custom api server that so the webapp chatbot can send post requests and receives the necessary responses:
```
uvicorn API:app --reload
```

## Run webapp.py
To run the application you should enter the following command to your terminal:
```
streamlit run webapp.py
```

## Example:
<img width="1510" alt="Alan kay Ai chatbot" src="https://github.com/user-attachments/assets/7d736399-855a-4e5c-aa35-9b3b9e2231a1" />

