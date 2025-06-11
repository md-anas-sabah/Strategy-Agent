from crewai import Task
from textwrap import dedent


class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def business_intelligence_task(self, agent, business_info, business_goals):
        return Task(
            description=f"Analyze this business and provide strategic insights: {business_info}. Goals: {business_goals}. Create customer personas and identify growth opportunities.",
            expected_output="A business analysis report with customer personas and strategic recommendations.",
            agent=agent
        )

    def competitor_analysis_task(self, agent, business_info):
        return Task(
            description=f"Research and analyze competitors for this business: {business_info}. Identify key competitors, their strategies, and market opportunities.",
            expected_output="A competitor analysis report with competitive insights and recommendations.",
            agent=agent
        )

    def marketing_strategy_development_task(self, agent, business_intelligence, competitor_analysis):
        return Task(
            description=f"Create a comprehensive marketing strategy based on this research: {business_intelligence}. Include channel strategy, budget recommendations, and implementation roadmap.",
            expected_output="A complete marketing strategy document with actionable recommendations and implementation plan.",
            agent=agent
        )