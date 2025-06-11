#!/usr/bin/env python3

import os
from decouple import config

# Test the exact inputs you provided
business_info = "We are a mid-sized e-commerce company specializing in sustainable home goods. We sell eco-friendly products like bamboo kitchenware, organic cotton bedding, and natural cleaning supplies. We've been in business for 3 years, operate primarily online through our website and Amazon marketplace, and have a team of 15 employees. Our business model is B2C with some wholesale partnerships with eco-friendly retailers."

business_goals = "- Increase annual revenue by 40% to reach $2.5M"

budget_info = ""  # Empty budget info as provided

current_marketing = "1 part-time SEO consultant"

print("🔧 Testing with your exact inputs...")
print("=" * 60)

from main import StrategyAgentSystem

# Set environment
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

try:
    # Initialize system with your inputs
    strategy_system = StrategyAgentSystem(
        business_info=business_info,
        business_goals=business_goals,
        budget_info=budget_info,
        current_marketing=current_marketing
    )
    
    print("✅ System initialized successfully")
    print("🚀 Starting strategy generation...")
    
    # Execute strategy generation
    final_strategy, output_dir = strategy_system.run()
    
    if final_strategy and output_dir:
        print(f"\n🎉 SUCCESS! Strategy generated!")
        print(f"📁 Reports saved to: {output_dir}")
    else:
        print("\n❌ Strategy generation failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()