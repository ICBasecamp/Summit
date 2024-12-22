import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from social_media.NLPAnalysis import SM_NLPAnalysis
from earnings.NLPAnalysis import ER_NLPAnalysis

async def main():
    # EI_NLPAnalysis()
    ER_NLPAnalysis()
    # await SM_NLPAnalysis()

if __name__ == '__main__':
    asyncio.run(main())

