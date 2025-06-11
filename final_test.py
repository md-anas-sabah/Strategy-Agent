#!/usr/bin/env python3

import os
from decouple import config
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

print("🧪 Final Working Test")
print("=" * 40)

# Use the exact same format that worked before
business_info = "E-commerce company selling sustainable home goods, 3 years old, 15 employees"
business_goals = "Increase annual revenue by 40% to reach $2.5M"

try:
    # Create simple agents like the working version
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    business_analyst = Agent(
        role="Business Intelligence Analyst",
        goal="Analyze business information and create customer personas",
        backstory="You are a business analyst expert",
        llm=llm,
        verbose=True
    )
    
    competitor_analyst = Agent(
        role="Competitive Intelligence Specialist", 
        goal="Research competitors and market opportunities",
        backstory="You are a market research expert",
        llm=llm,
        verbose=True
    )
    
    strategy_composer = Agent(
        role="Marketing Strategy Consultant",
        goal="Create comprehensive marketing strategies",
        backstory="You are a marketing strategy expert",
        llm=llm,
        verbose=True
    )
    
    # Create simple tasks
    business_task = Task(
        description=f"Analyze this business: {business_info}. Goals: {business_goals}. Create 2-3 customer personas and identify growth opportunities.",
        expected_output="A business analysis with customer personas and recommendations",
        agent=business_analyst
    )
    
    competitor_task = Task(
        description=f"Research competitors for: {business_info}. Identify 3-5 main competitors and market opportunities.",
        expected_output="A competitor analysis with insights and opportunities",
        agent=competitor_analyst
    )
    
    print("🚀 Running Business Analysis...")
    business_crew = Crew(
        agents=[business_analyst],
        tasks=[business_task],
        verbose=True
    )
    business_result = business_crew.kickoff()
    
    print("🚀 Running Competitor Analysis...")
    competitor_crew = Crew(
        agents=[competitor_analyst],
        tasks=[competitor_task], 
        verbose=True
    )
    competitor_result = competitor_crew.kickoff()
    
    print("🚀 Running Strategy Creation...")
    strategy_task = Task(
        description=f"Create a marketing strategy using: Business Analysis: {business_result}. Competitor Analysis: {competitor_result}. Include channel recommendations and budget allocation.",
        expected_output="A comprehensive marketing strategy with implementation plan",
        agent=strategy_composer
    )
    
    strategy_crew = Crew(
        agents=[strategy_composer],
        tasks=[strategy_task],
        verbose=True
    )
    strategy_result = strategy_crew.kickoff()
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Complete Strategy Generated")
    print("=" * 60)
    print(f"Strategy Preview: {str(strategy_result)[:300]}...")
    
    # Save results
    from datetime import datetime
    from pathlib import Path
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"strategy_reports/{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as markdown
    md_content = f"""# Marketing Strategy Report
Generated: {timestamp}

## Business Analysis
{business_result}

## Competitor Analysis  
{competitor_result}

## Marketing Strategy
{strategy_result}
"""
    
    with open(output_dir / "marketing_strategy.md", 'w') as f:
        f.write(md_content)
        
    print(f"📁 Strategy saved to: {output_dir}/marketing_strategy.md")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()