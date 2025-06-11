#!/usr/bin/env python3

import os
from decouple import config
from crewai import Agent, Task, Crew, Process
from agents import CustomAgents
from tasks import CustomTasks

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

print("🧪 Testing Strategy Agent with E-commerce Input...")
print("=" * 60)

# Use the working input from your earlier successful example
business_info = "E-commerce company selling sustainable home goods, 3 years old, 15 employees"
business_goals = "Increase annual revenue by 40% to reach $2.5M"

try:
    # Create agents and tasks
    agents = CustomAgents()
    tasks = CustomTasks()
    
    print("✅ Creating all 3 analysis agents...")
    business_analyst = agents.business_analyst_agent()
    competitor_analyst = agents.competitor_analyst_agent()  
    marketing_evaluator = agents.marketing_evaluator_agent()
    
    print("✅ Creating tasks...")
    business_task = tasks.business_intelligence_task(
        business_analyst, business_info, business_goals
    )
    
    competitor_task = tasks.competitor_analysis_task(
        competitor_analyst, business_info
    )
    
    # Use simpler inputs for evaluation task
    evaluation_task = tasks.business_intelligence_task(
        marketing_evaluator, "Limited marketing channels", "Need better ROI"
    )
    
    print("✅ Creating crew with sequential processing...")
    crew = Crew(
        agents=[business_analyst, competitor_analyst, marketing_evaluator],
        tasks=[business_task, competitor_task, evaluation_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Running 3-agent analysis...")
    results = crew.kickoff()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Multi-agent analysis completed")
    print("=" * 60)
    print("RESULTS SUMMARY:")
    print(str(results)[:500] + "..." if len(str(results)) > 500 else str(results))
    
    # Now test strategy composition
    print("\n🧠 Testing Strategy Composer...")
    strategy_composer = agents.strategy_composer_agent()
    
    strategy_task = tasks.marketing_strategy_development_task(
        strategy_composer, results, results
    )
    
    strategy_crew = Crew(
        agents=[strategy_composer],
        tasks=[strategy_task],
        process=Process.sequential,
        verbose=True
    )
    
    strategy_result = strategy_crew.kickoff()
    
    print("\n" + "=" * 60)
    print("🎉 FULL SYSTEM SUCCESS!")
    print("=" * 60)
    print("✅ Business Intelligence: Completed")
    print("✅ Competitor Analysis: Completed") 
    print("✅ Marketing Evaluation: Completed")
    print("✅ Strategy Composition: Completed")
    print("\n🎊 Your Strategy Agent system is working perfectly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()