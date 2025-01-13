import json
import os
from groq import Groq
import asyncio
from earnings.FinancialStats import main as calculate_FS
from earnings.NonStatisticalAnalysis import main as calculate_NSA
from earnings.StatisticalAnalysis import preprocess_and_analyze, getDataframes
from dotenv import load_dotenv

async def run_calculations(ticker):
    dataframes_list = await getDataframes(ticker)
    
    # Run the financial stats calculation
    financial_stats_results = await calculate_FS(ticker)

    # Run the non-statistical analysis
    non_statistical_results = await calculate_NSA(ticker)

    # Run the statistical analysis
    statistical_results = []
    for df, name in dataframes_list:
        result = preprocess_and_analyze(df, name)
        statistical_results.append(result)

    # Combine all results into a single dictionary
    combined_results = {
        'financial_stats': financial_stats_results,
        'non_statistical_analysis': non_statistical_results,
        'statistical_analysis': statistical_results
    }

    return combined_results

async def call_groqapi_service(text):
    prompt_template = """
    Please analyze the following financial data and provide insights. Focus on key metrics, trends, and any notable observations. Summarize the data in a clear and concise manner.

    Financial Data:
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

async def ER_NLPAnalysis(ticker):
    combined_results = await run_calculations(ticker)

    combined_results_str = ""
    for key, value in combined_results.items():
        combined_results_str += f"{key}:\n"
        if isinstance(value, list):
            for item in value:
                combined_results_str += f"{item}\n"
        else:
            combined_results_str += f"{value}\n"
            combined_results_str = combined_results_str.strip()
    
    # Define a prompt to provide context or specific instructions
    prompt = f"""
    Please analyze the following financial data and provide insights on this stock: {ticker}. Provide insights on the data that you see and put it into human language. For context
    the statistical_results have feature importance with random forest regression and PCA components for each statistical dataframe. The financial_stats_results have financial metrics like PE Ratio, EPS, and earnings Date. The non_statistical_results have average scores by rating, time series analysis, correlation, margins, quarterly growth rates, and price gap. 
    I want you to include statistics in the analysis so you would say something like "The most important feature for X has 35% importance indicating Y". Make connections between the results and provide a clear and concise summary of the data. You have to explain what the data means and what it means for {ticker} not just state facts, in addition try and make it in
    a readable paragraph not bullet points. I want a paragraph for the analysis on each of the 4 dataframes in the earnings estimate meaning one for 
    earnings, eps trend, earnings-history and revenue. One paragraph focusing on Non-statistical data, and one paragraph focusin on financial stats
    therefore leading to 6 paragraphs of NLP. The paragraphs of statitical analysis should make remarks on BOTH the PCA scores grouping the labels together based on the results
    AND the feature importance scores. The paragraphs should make remarks on everything needed. LABEL each section as **Earnings Estimate**, **Revenue Estimate**, **Earnings History Estimate**, **EPS trend Estimate**, **Non Statistical Estimate**, **Financial Estimate** MAKE sure to include analysis ON EACH OF THESE SECTIONS EQUALLY. Focus on each part of the data equally here are some examples for each part of the data:

    EXAMPLES:
    Non-Statistical Data:
    Analysts with a "Buy" rating have high scores across all metrics, indicating strong confidence in the stock.
    "Outperform" and "Overweight" ratings also show high scores, suggesting positive sentiment.
    "Strong Buy" ratings have slightly lower scores, but still indicate strong confidence.
    Analyst sentiment (Overall Score) and Price Target have shown a decreasing trend from May to November 2024.
    Despite the decrease in Overall Score, the Price Target has increased, indicating higher expected future value.

    Financial Stats:
    FOR FINANCIAL STATS FOCUS ON EVERY PART OF THE FINANCIAL STATS DON't SKIP ANY.
    PE Ratio (TTM) (56.08): This indicates that investors are willing to pay $56.08 for every $1 of earnings over the trailing twelve months. A high P/E ratio can suggest that the stock is overvalued, but it can also indicate strong growth expectations.
    Forward P/E (33.44): This indicates that investors are willing to pay $33.44 for every $1 of expected future earnings. While still high, it is lower than the trailing P/E, suggesting expectations of future earnings growth.
    PEG Ratio (5yr expected) (0.89): A PEG ratio below 1 suggests that the stock may be undervalued relative to its growth prospects. This is a positive indicator.
    Price/Sales (31.27): This high ratio indicates that investors are paying $31.27 for every $1 of sales. This is quite high, suggesting that the market has high expectations for future growth.
    Enterprise Value/EBITDA (46.21): This high ratio suggests that the company is valued highly relative to its earnings before interest, taxes, depreciation, and amortization. This can indicate high growth expectations but also potential overvaluation.

    earnings Estimate:
    Key Features: The Low Estimate and No. of Analysts are the most influential features, indicating that analysts' lower expectations and the number of analysts covering the stock significantly impact the average earnings estimate.
    Historical Performance: The Year Ago EPS also plays a crucial role, suggesting that past performance is a strong indicator of future earnings.
    Statistics: The cross-validation mean MSE of 0.6652 with a standard deviation of 0.8357 indicates moderate prediction accuracy and variability.
    Revenue Estimate:

    Key Features: The Year Ago Sales and Low Estimate are the most critical features, highlighting the importance of historical sales data and conservative estimates in predicting future revenue.
    Growth Projections: The Sales Growth (year/est) has a minimal impact, indicating that growth projections are less influential compared to historical data and analyst estimates.
    Statistics: The cross-validation mean MSE of 1.0205 with a standard deviation of 0.9040 suggests higher prediction error and variability compared to earnings estimates.
    EPS Trend:

    Financial Data:
    """

    # Combine the prompt with the combined results
    text_to_analyze = prompt + combined_results_str

    insights = await call_groqapi_service(text_to_analyze)
    return insights, combined_results_str

async def NLP(ticker):
    load_dotenv()
    groq_api_key = os.getenv("groq_api_key")
    global client
    client = Groq(api_key=groq_api_key)

    insights = await ER_NLPAnalysis(ticker)
    return insights