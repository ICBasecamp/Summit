import json
import os
from groq import Groq
import asyncio
from dotenv import load_dotenv
from featureImportance import calculate_feature_importance

average_correlations = calculate_feature_importance()

# Load the JSON results file
# with open('economic_indicators/results/average_correlations.json', 'r') as f:
#     average_correlations = json.load(f)

# Combine all results into a single dictionary
combined_results = {
    'average_correlations': average_correlations
}

# Convert the combined results to a string for NLP processing
combined_results_str = json.dumps(combined_results, indent=4)

# Define a prompt to provide context or specific instructions
prompt = """
Please analyze the following financial data and provide insights on this stock. Provide insights on the data that you see and put it into human language. For context, the average_correlations have the average correlation values for each economic indicator with the earnings reports, stock revenue, earnings history, and EPS trend. To elaborate it is the average pearson correlation therefore a value of 1 indicates a perfect positive linear relationship, -1 indicates a perfect negative linear relationship, and 0 indicates no linear relationship.
I want you to include statistics in the analysis so you would say something like "The most important feature for X has 35% importance indicating Y". Make connections between the results and provide a clear and concise summary of the data. You have to explain what the data means and what it means for the stock, not just state facts. Remember a positive
correlation means they are positively correlated when one goes up the other also goes up. If very negative (close to -1) they are inversely correlated so if one goes up the other goes down, both are equally impactful. Make it in a readable paragraph, not bullet points. Focus on each part of the data equally.

Financial Data:
"""

# Combine the prompt with the combined results
text_to_analyze = prompt + combined_results_str

load_dotenv()
groq_api_key = os.getenv("groq_api_key")
client = Groq(api_key=groq_api_key)

async def call_groqapi_service(text):
    prompt_template = """
    {text}
    """
    prompt = prompt_template.format(text=text)
    chat_completion = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
    )
    return chat_completion.choices[0].message.content.strip()

def EI_NLPAnalysis():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            raise

    insights = loop.run_until_complete(call_groqapi_service(text_to_analyze))
    return insights

    # with open('economic_indicators/results/nlp_insights.txt', 'w') as f:
    #     f.write(insights)

print(EI_NLPAnalysis())