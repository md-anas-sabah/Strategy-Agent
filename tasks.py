from crewai import Task
from textwrap import dedent


class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def business_intelligence_task(self, agent, business_info, business_goals):
        return Task(
            description=dedent(
                f"""
            Conduct comprehensive business intelligence gathering and current state assessment for:
            
            Business Information: {business_info}
            Business Goals: {business_goals}
            
            Your task is to:
            1. Create a detailed questionnaire system to capture:
               - Business model and revenue streams
               - Target audience demographics and psychographics
               - Current marketing efforts and performance
               - Available budget and resources
               - Short-term and long-term objectives
               
            2. Assess the current marketing state by analyzing:
               - Existing marketing channels and their performance
               - Brand positioning and messaging
               - Marketing gaps and opportunities
               - Resource allocation effectiveness
               
            3. Develop comprehensive customer personas including:
               - Demographics, interests, and behaviors
               - Pain points and motivations
               - Preferred communication channels
               - Purchase decision factors
            
            {self.__tip_section()}
            
            Make sure to gather the most current and relevant data available.
        """
            ),
            expected_output="""A comprehensive business intelligence report containing:
            - Detailed business assessment questionnaire with responses
            - Current marketing state analysis with identified gaps
            - 3-5 detailed customer personas with complete profiles
            - Business model and revenue stream analysis
            - Resource and budget assessment summary""",
            agent=agent,
        )

    def competitor_analysis_task(self, agent, business_info):
        return Task(
            description=dedent(
                f"""
            Conduct thorough competitor analysis and market research for the business:
            {business_info}
            
            Your comprehensive research should include:
            
            1. Identify Direct and Indirect Competitors:
               - Find 5-10 direct competitors in the same market
               - Identify 3-5 indirect competitors solving similar problems
               - Analyze market leaders and emerging players
               
            2. Competitive Intelligence Gathering:
               - Pricing strategies and models
               - Marketing messages and value propositions
               - Channel strategies (organic and paid)
               - Content marketing approaches
               - Social media presence and engagement
               - SEO and keyword strategies
               - Advertising spend and creative approaches
               
            3. Market Positioning Analysis:
               - Competitive advantages and differentiators
               - Market share and positioning
               - Strengths and weaknesses assessment
               - Opportunities for differentiation
               
            4. Industry Trends and Benchmarks:
               - Market size and growth trends
               - Industry best practices
               - Emerging opportunities and threats
               - Technology and innovation trends
            
            {self.__tip_section()}
            
            Use the most recent data and ensure comprehensive coverage of the competitive landscape.
        """
            ),
            expected_output="""A detailed competitor analysis report including:
            - Complete competitor profiles (5-10 direct, 3-5 indirect)
            - Competitive positioning matrix and analysis
            - Pricing comparison and strategy insights
            - Marketing channel and messaging analysis
            - Industry benchmarks and best practices
            - Market opportunities and differentiation strategies
            - Competitive threats and mitigation recommendations""",
            agent=agent,
        )

    def marketing_strategy_development_task(self, agent, business_intelligence, competitor_analysis):
        return Task(
            description=dedent(
                f"""
            Using the business intelligence and competitor analysis, create a comprehensive 
            marketing strategy document that will serve as the foundation for all marketing efforts.
            
            Based on:
            - Business Intelligence: {business_intelligence}
            - Competitor Analysis: {competitor_analysis}
            
            Develop a complete marketing strategy including:
            
            1. Executive Summary with Key Recommendations
               - Top 3-5 strategic priorities
               - Expected outcomes and ROI projections
               - Critical success factors
               
            2. Target Audience Strategy
               - Primary and secondary audience segments
               - Detailed persona-based messaging
               - Customer journey mapping
               
            3. Competitive Positioning and Differentiation
               - Unique value proposition
               - Brand positioning statement
               - Differentiation strategy
               
            4. Marketing Channel Strategy
               - Organic channel recommendations (SEO, content, social)
               - Paid channel recommendations (PPC, social ads, display)
               - Channel prioritization based on audience and budget
               - Cross-channel integration approach
               
            5. Budget Allocation and Resource Planning
               - Channel-specific budget recommendations
               - Resource requirements (team, tools, external support)
               - ROI expectations by channel
               
            6. 12-Month Implementation Roadmap
               - Quarterly milestones and objectives
               - Month-by-month tactical execution plan
               - Key initiatives and campaign schedules
               - Dependencies and critical path items
               
            7. Success Metrics and KPIs
               - Channel-specific KPIs and benchmarks
               - Overall business impact metrics
               - Reporting and optimization framework
               
            8. Content Strategy and Messaging Framework
               - Content pillars and themes
               - Messaging hierarchy by audience
               - Content calendar and production plan
            
            {self.__tip_section()}
            
            Ensure all recommendations are tailored to the business stage, industry, and available resources.
            Provide specific, actionable recommendations with clear rationale.
        """
            ),
            expected_output="""A comprehensive marketing strategy document (15-25 pages) containing:
            - Executive summary with top strategic recommendations
            - Complete target audience analysis and persona-based strategies  
            - Competitive positioning and differentiation strategy
            - Detailed channel strategy with budget allocation recommendations
            - 12-month implementation roadmap with quarterly milestones
            - Success metrics framework with KPIs for each channel
            - Content strategy and messaging framework
            - Resource requirements and investment recommendations
            - Risk assessment and mitigation strategies
            - Next steps and immediate action items""",
            agent=agent,
        )
