#!/usr/bin/env python3

import os
from decouple import config
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

print("🔍 Debug Test - Step by Step")
print("=" * 40)

try:
    # Test 1: Basic LLM Connection
    print("1. Testing OpenAI connection...")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    print("✅ LLM created successfully")
    
    # Test 2: Simple Agent Creation
    print("2. Testing basic agent creation...")
    agent = Agent(
        role="Business Analyst",
        goal="Analyze business information",
        backstory="You are a business analyst",
        llm=llm,
        verbose=True
    )
    print("✅ Agent created successfully")
    
    # Test 3: Simple Task Creation
    print("3. Testing basic task creation...")
    task = Task(
        description="Analyze this business: E-commerce company selling sustainable goods. Goal: Increase revenue by 40%.",
        expected_output="A simple business analysis report",
        agent=agent
    )
    print("✅ Task created successfully")
    
    # Test 4: Simple Crew Execution
    print("4. Testing basic crew execution...")
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    print("✅ Crew created successfully")
    
    print("5. Executing simple task...")
    result = crew.kickoff()
    
    print("✅ SUCCESS! Basic execution works")
    print("Result preview:", str(result)[:200] + "...")
    
except Exception as e:
    print(f"❌ Error at step: {e}")
    import traceback
    traceback.print_exc()