#!/usr/bin/env python3

import os
from decouple import config
from main import StrategyAgentSystem

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

# Test inputs from the user
business_info = "We are a B2B SaaS startup developing AI-powered project management software. We're 2 years old, have 8 employees, and our platform helps teams automate task management and resource allocation. We operate on a subscription-based model with monthly and annual plans."

business_goals = "Our goals for the next year are: Increase monthly recurring revenue by 50%, - Expand to 3 new cities"

budget_info = "Monthly marketing budget: $15,000"

current_marketing = "LinkedIn (5K followers, 2% engagement), High customer acquisition cost, Industry-specific content series"

print("🚀 Testing Strategy Agent System with real inputs...")
print("=" * 60)

# Initialize system
strategy_system = StrategyAgentSystem(
    business_info=business_info,
    business_goals=business_goals,
    budget_info=budget_info,
    current_marketing=current_marketing
)

# Execute strategy generation
final_strategy, output_dir = strategy_system.run()

if final_strategy and output_dir:
    print(f"\n✅ SUCCESS! Strategy generated and saved to: {output_dir}")
else:
    print("\n❌ Strategy generation failed")