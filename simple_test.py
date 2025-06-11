#!/usr/bin/env python3

import os
from decouple import config
from crewai import Agent, Task, Crew, Process
from agents import CustomAgents
from tasks import CustomTasks

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

print("🧪 Testing Simple Strategy Agent...")
print("=" * 50)

# Test inputs
business_info = "E-commerce company selling sustainable home goods, 3 years old, 15 employees"
business_goals = "Increase annual revenue by 40% to reach $2.5M"

try:
    # Create agents and tasks
    agents = CustomAgents()
    tasks = CustomTasks()
    
    print("✅ Creating business analyst...")
    business_analyst = agents.business_analyst_agent()
    
    print("✅ Creating business intelligence task...")
    business_task = tasks.business_intelligence_task(
        business_analyst, business_info, business_goals
    )
    
    print("✅ Creating simple crew...")
    crew = Crew(
        agents=[business_analyst],
        tasks=[business_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Running single agent test...")
    result = crew.kickoff()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Single agent working properly")
    print("=" * 60)
    print("RESULT:")
    print(result)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()