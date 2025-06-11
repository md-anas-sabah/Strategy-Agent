from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


class CustomAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    def business_analyst_agent(self):
        return Agent(
            role="Business Intelligence Analyst",
            goal="Gather comprehensive business intelligence and analyze market opportunities",
            backstory=dedent("""
                You are a senior business analyst with 12+ years of experience in business intelligence 
                and strategic planning. You specialize in extracting structured business information, 
                understanding complex business models, and identifying growth opportunities.
            """),
            llm=self.OpenAIGPT4,
            verbose=True
        )

    def competitor_analyst_agent(self):
        return Agent(
            role="Competitive Intelligence Specialist",
            goal="Conduct comprehensive competitor analysis and market research",
            backstory=dedent("""
                You are a competitive intelligence expert with 10+ years of experience in market research 
                and competitor analysis. You specialize in uncovering competitor strategies, pricing models, 
                and market positioning through advanced research techniques.
            """),
            llm=self.OpenAIGPT35,
            verbose=True
        )

    def marketing_evaluator_agent(self):
        return Agent(
            role="Marketing Performance Analyst",
            goal="Analyze and evaluate marketing efforts to identify improvement opportunities",
            backstory=dedent("""
                You are a marketing analytics expert with 8+ years of experience in performance 
                measurement and optimization. You specialize in analyzing existing marketing efforts, 
                identifying performance gaps, and recommending improvements.
            """),
            llm=self.OpenAIGPT35,
            verbose=True
        )

    def strategy_composer_agent(self):
        return Agent(
            role="Senior Marketing Strategy Consultant",
            goal="Synthesize all research into a comprehensive marketing strategy",
            backstory=dedent("""
                You are an expert marketing strategist with over 15 years of experience helping 
                businesses develop comprehensive marketing strategies. You excel at synthesizing 
                complex information into cohesive, actionable marketing strategies.
            """),
            llm=self.OpenAIGPT4,
            verbose=True
        )

    def qa_supervisor_agent(self):
        return Agent(
            role="Quality Assurance Supervisor",
            goal="Ensure the final marketing strategy meets the highest quality standards",
            backstory=dedent("""
                You are a senior quality assurance manager with 15+ years of experience in 
                strategic consulting and quality control. You specialize in reviewing complex 
                deliverables, ensuring completeness, and maintaining high standards.
            """),
            llm=self.OpenAIGPT4,
            verbose=True
        )