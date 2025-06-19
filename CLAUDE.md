# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- `python3 main.py` - Run the main strategy agent application
- `./run.sh` - Run the application with proper environment setup (sets PKG_CONFIG_PATH and DYLD_LIBRARY_PATH for WeasyPrint dependencies)

### Environment Setup
- `pip install -r requirements.txt` - Install all Python dependencies
- Set up `.env` file with required API keys:
  - `OPENAI_API_KEY` - Required for OpenAI GPT models
  - `ANTHROPIC_API_KEY` - Required for Claude 3.5 Sonnet Refiner Agent
  - `YOUTUBE_API_KEY` - Optional for YouTube data scraping
  - `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` - Optional for Reddit analysis

### Testing and Validation
No specific test framework is configured. The application includes built-in validation through confidence scoring and multi-source verification systems.

## Code Architecture

### High-Level Structure
This is a CrewAI-based multi-agent system for generating comprehensive marketing strategy reports. The system uses multiple specialized AI agents working together to analyze businesses, competitors, and market conditions.

### Core Components

**Main Application Flow** (`main.py`):
- Orchestrates the entire strategy generation process
- Handles user input collection and validation
- Manages data collection from multiple sources (web scraping, APIs, financial data)
- Coordinates agent execution and report generation
- Outputs structured HTML and Markdown reports with accompanying JSON data

**Agent System** (`agents.py`):
- `WorldClassAgents` class contains 7 specialized AI agents:
  - `quantum_marketing_intelligence_agent()` - Marketing analysis and customer insights
  - `elite_competitive_intelligence_agent()` - Competitor analysis and threat assessment
  - `advanced_marketing_performance_agent()` - Campaign optimization and performance metrics
  - `master_marketing_architect_agent()` - Strategic synthesis and framework design
  - `supreme_strategic_validator_agent()` - Quality assurance and validation
  - `quantum_consumer_insights_agent()` - Consumer behavior and market analysis
  - `world_class_claude_refiner_agent()` - **NEW: Claude 3.5 Sonnet Refiner Agent** - World-class strategy refinement and enhancement
- Each agent has detailed role definitions, capabilities, and validation protocols
- Uses hybrid AI approach: OpenAI models (GPT-3.5, GPT-4, GPT-4-turbo) for analysis + Claude 3.5 Sonnet for final strategy refinement

**Task Management** (`tasks.py`):
- `QuantumStrategicTasks` class defines structured tasks for each agent
- Implements systematic reasoning frameworks and validation protocols
- Tasks include detailed instructions, expected outputs, and quality standards
- Uses incentive systems to encourage high-quality analysis

**Data Collection Systems**:
- `SocialMediaScraper` - Scrapes social media data using free APIs and web scraping
- `CompetitorAdsScraper` - Analyzes competitor advertising strategies
- `SEOAnalyzer` - Performs comprehensive SEO analysis
- `AdvancedIntelligenceEngine` - Processes and validates market intelligence data
- `ValidationEngine` - Ensures data accuracy through multiple validation methods

**Marketing Resources** (`marketing_resources.py`):
- `MarketingResourcesDB` - Comprehensive knowledge base of marketing tools, strategies, and best practices
- Industry-specific recommendations and budget allocation templates
- Content frameworks, growth hacks, and attribution models

### Key Features

**Multi-Source Data Integration**:
- Web scraping for competitor analysis
- Financial data from Yahoo Finance
- Social media sentiment analysis
- SEO and keyword research
- News and trend analysis

**Advanced Validation System**:
- Confidence scoring for all data points
- Cross-reference validation across multiple sources
- Statistical validation and historical pattern analysis
- Ensemble validation combining multiple methods

**Report Generation**:
- Comprehensive HTML reports with interactive elements
- Markdown summaries for easy reading
- Structured JSON data for programmatic access
- Time-stamped output in `strategy_reports/` directory

### Data Flow
1. User provides business information through interactive prompts
2. System collects real-time market data from multiple sources
3. Specialized OpenAI agents analyze different aspects (marketing, competition, consumers)
4. Master architect synthesizes findings into comprehensive strategy
5. Validator ensures quality and accuracy
6. **NEW: Claude 3.5 Sonnet Refiner transforms strategy into world-class Fortune 100 consulting standards**
7. Reports are generated in multiple formats and saved to timestamped directories

### Configuration Notes
- The system is designed to work with free APIs where possible
- Fallback mechanisms provide simulated data when APIs are unavailable
- Environment variables control API access and features
- WeasyPrint dependencies require special path configuration on macOS (handled by `run.sh`)

### Output Structure
Generated reports include:
- Executive summary with key recommendations
- Detailed market analysis and competitive intelligence
- Customer personas and journey mapping
- Marketing strategy frameworks and action plans
- Budget allocation and ROI projections
- Risk assessment and validation scores