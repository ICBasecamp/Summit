# Summit 📈

**The Ultimate AI-Powered Stock Analysis Platform**

Summit is a comprehensive, real-time stock analysis platform that aggregates and analyzes data from multiple sources to provide investors with actionable insights. By combining social media sentiment, news analysis, earnings reports, and economic indicators, Summit delivers a 360-degree view of any stock's market sentiment and financial health.

[Summit Demo](https://www.linkedin.com/posts/samuils-georgiev_excited-to-share-summit-a-project-ive-been-activity-7285515688859914240-btRA?utm_source=share&utm_medium=member_desktop&rcm=ACoAADjzWe8B8_0Mr2NAGSestqgsnjY6e1y7-m0)

## 🌟 Features

### Multi-Source Analysis Engine
- **📱 Social Media Sentiment**: Real-time analysis from Reddit (r/wallstreetbets), Bluesky, and StockTwits
- **📰 News Analysis**: Sentiment analysis of financial news articles with source attribution
- **📊 Earnings Intelligence**: Deep dive into earnings reports, financial metrics, and analyst estimates
- **🏦 Economic Indicators**: Correlation analysis with macroeconomic data

### AI-Powered Insights
- **🤖 Natural Language Processing**: Advanced sentiment analysis with confidence scores
- **📈 Statistical Analysis**: Feature importance analysis using Random Forest and PCA
- **🔍 Pattern Recognition**: Historical trend analysis and performance predictions
- **💡 Executive Summaries**: AI-generated insights in plain English

### Modern Web Interface
- **⚡ Real-time Processing**: Async data fetching with live progress indicators
- **🎨 Beautiful UI**: Modern design with Aceternity UI components and smooth animations
- **📱 Responsive Design**: Optimized for desktop and mobile experiences
- **🔍 Smart Search**: Intelligent ticker symbol suggestions with company logos

## 🏗️ Architecture

### Backend (Python)
```
├── server.py              # Main analysis orchestrator
├── workflow.py            # Analysis pipeline workflow
├── social_media/          # Social media data collection & analysis
├── news/                  # News sentiment analysis
├── earnings/              # Financial data & earnings analysis
├── economic_indicators/   # Economic data correlation
└── utilities.py           # Helper functions
```

### Frontend (Next.js 15)
```
├── src/app/
│   ├── components/        # Reusable UI components
│   ├── pages/            # Main application pages
│   ├── context/          # React context for state management
│   └── api/              # API routes
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- API keys for:
  - Groq (for AI analysis)
  - Social media platforms
  - Financial data providers

### Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env file

# Run the analysis server
python server.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd ada-frontend-next

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🔧 Tech Stack

### Backend
- **Python 3.8+** - Core analysis engine
- **asyncio** - Asynchronous processing
- **Groq API** - Large language model integration
- **pandas** - Data manipulation and analysis
- **scikit-learn** - Machine learning algorithms
- **dotenv** - Environment configuration

### Frontend
- **Next.js 15** - React framework with App Router
- **React 19** - Latest React features
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **NextUI & Aceternity UI** - Modern component libraries

### APIs & Data Sources
- **Reddit API** - r/wallstreetbets sentiment
- **Bluesky API** - Social media posts
- **StockTwits API** - Financial social network
- **Yahoo Finance** - Stock prices and news
- **Financial data providers** - Earnings and economic data

## 📊 Analysis Modules

### Social Media Analysis
- **Sentiment Classification**: Positive, neutral, negative sentiment scoring
- **Volume Analysis**: Post frequency and engagement metrics
- **Trend Detection**: Emerging topics and discussion themes
- **Source Attribution**: Platform-specific sentiment breakdown

### News Sentiment Analysis
- **Article Processing**: Automatic title and content extraction
- **Sentiment Scoring**: Confidence-weighted sentiment analysis
- **Source Tracking**: News outlet reputation and bias analysis
- **Temporal Analysis**: Sentiment changes over time

### Earnings Intelligence
- **Financial Metrics**: P/E ratios, EPS trends, revenue analysis
- **Analyst Estimates**: Consensus targets and recommendation changes
- **Statistical Models**: Feature importance and predictive analytics
- **Performance Comparison**: Historical and peer benchmarking

### Economic Indicators
- **Correlation Analysis**: Stock performance vs. economic data
- **Feature Importance**: Key economic drivers identification
- **Trend Analysis**: Economic cycle impact assessment
- **Risk Assessment**: Macroeconomic risk factors

## 🎯 Use Cases

- **Individual Investors**: Get comprehensive stock analysis before making investment decisions
- **Day Traders**: Monitor real-time sentiment shifts and news impact
- **Financial Advisors**: Access detailed analysis reports for client consultations
- **Researchers**: Analyze correlation between social sentiment and stock performance
- **Portfolio Managers**: Risk assessment and opportunity identification

## 📈 Sample Analysis Output

For a stock like AAPL, Summit provides:

**Social Media Sentiment**: 67% Bullish (3,247 posts analyzed)
- Reddit: 72% positive sentiment
- Bluesky: 61% positive sentiment  
- StockTwits: 69% positive sentiment

**News Analysis**: 8 articles analyzed, 75% positive sentiment
- Key themes: Product launches, earnings beat, market expansion

**Financial Health**: Strong fundamentals
- P/E Ratio: 28.5 (vs. sector average 24.1)
- Revenue Growth: 8.2% YoY
- Analyst Rating: 85% Buy/Strong Buy

## 🛠️ Configuration

### Environment Variables
```bash
# .env file
GROQ_API_KEY=your_groq_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
BLUESKY_USERNAME=your_bluesky_username
BLUESKY_PASSWORD=your_bluesky_password
```

### Custom Analysis Parameters
Modify analysis parameters in respective module configuration files:
- Social media post limits
- News article date ranges
- Economic indicator correlations
- Statistical analysis methods

## 👥 Team

**Sam and Martin** - *The team that will rule San Francisco* 🌉

---

**⚡ Built with passion for data-driven investing**

*Summit - Where market intelligence meets artificial intelligence*
