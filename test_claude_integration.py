#!/usr/bin/env python3
"""
Test script to verify Claude 3.5 Sonnet integration
"""
import os
from decouple import config
from langchain_anthropic import ChatAnthropic

def test_claude_integration():
    """Test Claude 3.5 Sonnet API connection"""
    print("🔬 Testing Claude 3.5 Sonnet Integration...")
    
    try:
        # Load API key
        api_key = config("ANTHROPIC_API_KEY", default="")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in .env file")
            print("💡 Please add ANTHROPIC_API_KEY=your_key_here to your .env file")
            return False
        
        # Set environment variable
        os.environ["ANTHROPIC_API_KEY"] = api_key
        
        # Initialize Claude
        claude = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.1)
        
        # Test simple message
        test_message = "Hello Claude! Can you confirm you're ready to enhance marketing strategies?"
        response = claude.invoke(test_message)
        
        print("✅ Claude 3.5 Sonnet connection successful!")
        print(f"🤖 Claude Response: {response.content}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Package import error: {e}")
        print("💡 Run: pip install langchain-anthropic")
        return False
        
    except Exception as e:
        print(f"❌ Claude integration test failed: {e}")
        print("💡 Check your ANTHROPIC_API_KEY and internet connection")
        return False

def test_agent_creation():
    """Test Claude Refiner Agent creation"""
    print("\n🚀 Testing Claude Refiner Agent Creation...")
    
    try:
        from agents import WorldClassAgents
        
        # Create agents instance
        agents = WorldClassAgents()
        
        # Test Claude Refiner Agent creation
        claude_refiner = agents.world_class_claude_refiner_agent()
        
        print("✅ Claude Refiner Agent created successfully!")
        print(f"🎯 Agent Role: {claude_refiner.role}")
        print(f"🤖 Agent LLM: {type(claude_refiner.llm).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 CLAUDE 3.5 SONNET INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: API Connection
    api_test = test_claude_integration()
    
    # Test 2: Agent Creation
    agent_test = test_agent_creation()
    
    # Summary
    print("\n📊 TEST RESULTS:")
    print("=" * 30)
    print(f"✅ Claude API Connection: {'PASS' if api_test else 'FAIL'}")
    print(f"✅ Agent Creation: {'PASS' if agent_test else 'FAIL'}")
    
    if api_test and agent_test:
        print("\n🎉 All tests passed! Your system is ready for world-class marketing strategy generation!")
        print("🚀 Run 'python3 main.py' to start generating Fortune 100-level strategies!")
    else:
        print("\n⚠️  Some tests failed. Please resolve the issues above before running the main system.")