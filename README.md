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

## Run chatbot.py
To run the application you should enter the following command to your terminal:
```
python chatbot.py
```

### Enter your Question and get alan kay Ai response:
Example question:
```
Ask Alan Kay a question: Why was there a mismatch between Xerox management and PARC?
```

Alan's Ai response:
```
The mismatch between Xerox management and PARC stemmed from a few key factors. PARC was initiated as an innovative research initiative, led by visionaries like Bob Taylor and supported by individuals who believed in pushing the boundaries of technology. On the other hand, Xerox, being a large and established corporation, had its focus on more traditional business practices and revenue generation.

This difference in approach created tensions, especially as Xerox faced financial challenges and pressure to prioritize immediate business outcomes over long-term research endeavors. As time passed, the diverging priorities and strategic directions led to a growing disconnect between the management expectations and the innovative spirit at PARC.

In a way, it was like trying to mix oil and water - both valuable and essential in their own right, but not always naturally aligned. And as we know, oil and water don't mix well, especially in a copier! *chuckles*
```