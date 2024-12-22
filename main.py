import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from earnings.NLPAnalysis import main as ER_NLPAnalysis

async def main():
    EI_NLPAnalysis()
    await ER_NLPAnalysis()

if __name__ == '__main__':
    asyncio.run(main())