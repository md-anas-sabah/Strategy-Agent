import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from decouple import config
import markdown
from weasyprint import HTML, CSS

from textwrap import dedent
from agents import CustomAgents
from tasks import CustomTasks

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")

class SharedMemory:
    """Shared memory system for agent communication"""
    def __init__(self):
        self.data = {
            "business_info": {},
            "competitor_data": {},
            "marketing_gaps": {},
            "strategy_components": {},
            "qa_feedback": {}
        }
    
    def store(self, key, value):
        """Store data in shared memory"""
        self.data[key] = value
    
    def retrieve(self, key):
        """Retrieve data from shared memory"""
        return self.data.get(key, {})
    
    def get_all(self):
        """Get all data from shared memory"""
        return self.data

class StrategyAgentSystem:
    """Multi-agent system for comprehensive marketing strategy generation"""
    
    def __init__(self, business_info, business_goals, budget_info, current_marketing):
        self.business_info = business_info
        self.business_goals = business_goals
        self.budget_info = budget_info
        self.current_marketing = current_marketing
        self.shared_memory = SharedMemory()
        self.agents = CustomAgents()
        self.tasks = CustomTasks()
    
    def create_output_directory(self):
        """Create output directory for reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"strategy_reports/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def save_to_markdown(self, content, filename, output_dir):
        """Save content to markdown file"""
        filepath = output_dir / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def convert_to_pdf(self, markdown_file, output_dir):
        """Convert markdown to PDF"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # Add professional styling
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Marketing Strategy Report</title>
                <style>
                    body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 40px; }}
                    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                    h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
                    h3 {{ color: #2c3e50; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #f8f9fa; font-weight: bold; }}
                    .executive-summary {{ background-color: #f8f9fa; padding: 20px; border-left: 4px solid #3498db; margin: 20px 0; }}
                    ul, ol {{ margin: 10px 0; padding-left: 30px; }}
                    .page-break {{ page-break-before: always; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            pdf_file = output_dir / "marketing_strategy_report.pdf"
            HTML(string=styled_html).write_pdf(pdf_file)
            return pdf_file
        except Exception as e:
            print(f"PDF conversion failed: {e}")
            return None
    
    def run_parallel_analysis(self):
        """Run the first 3 agents in parallel for data gathering"""
        print("\n🔄 Phase 1: Parallel Intelligence Gathering")
        print("=" * 50)
        
        # Create agents
        business_analyst = self.agents.business_analyst_agent()
        competitor_analyst = self.agents.competitor_analyst_agent()
        marketing_evaluator = self.agents.marketing_evaluator_agent()
        
        # Create tasks
        business_task = self.tasks.business_analysis_task(
            business_analyst, self.business_info, self.business_goals, 
            self.budget_info, self.current_marketing
        )
        
        competitor_task = self.tasks.competitor_analysis_task(
            competitor_analyst, self.business_info, self.business_goals
        )
        
        evaluation_task = self.tasks.marketing_evaluation_task(
            marketing_evaluator, self.current_marketing, 
            self.business_goals, self.budget_info
        )
        
        # Run parallel crew
        parallel_crew = Crew(
            agents=[business_analyst, competitor_analyst, marketing_evaluator],
            tasks=[business_task, competitor_task, evaluation_task],
            process=Process.hierarchical,
            manager_llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),
            verbose=True,
            memory=True
        )
        
        results = parallel_crew.kickoff()
        
        # Store results in shared memory
        self.shared_memory.store("business_analysis", results)
        self.shared_memory.store("competitor_analysis", results)
        self.shared_memory.store("marketing_evaluation", results)
        
        return results
    
    def run_strategy_composition(self, analysis_results):
        """Run strategy composition agent"""
        print("\n🧠 Phase 2: Strategy Composition")
        print("=" * 50)
        
        strategy_composer = self.agents.strategy_composer_agent()
        
        composition_task = self.tasks.strategy_composition_task(
            strategy_composer,
            self.shared_memory.retrieve("business_analysis"),
            self.shared_memory.retrieve("competitor_analysis"),
            self.shared_memory.retrieve("marketing_evaluation")
        )
        
        composition_crew = Crew(
            agents=[strategy_composer],
            tasks=[composition_task],
            verbose=True,
            memory=True
        )
        
        strategy_result = composition_crew.kickoff()
        self.shared_memory.store("strategy_composition", strategy_result)
        
        return strategy_result
    
    def run_qa_supervision(self, strategy_result):
        """Run QA supervision for final quality check"""
        print("\n✅ Phase 3: Quality Assurance & Finalization")
        print("=" * 50)
        
        qa_supervisor = self.agents.qa_supervisor_agent()
        
        qa_task = self.tasks.qa_supervision_task(
            qa_supervisor,
            self.shared_memory.retrieve("business_analysis"),
            self.shared_memory.retrieve("competitor_analysis"),
            self.shared_memory.retrieve("marketing_evaluation"),
            strategy_result
        )
        
        qa_crew = Crew(
            agents=[qa_supervisor],
            tasks=[qa_task],
            verbose=True,
            memory=True
        )
        
        final_result = qa_crew.kickoff()
        self.shared_memory.store("final_strategy", final_result)
        
        return final_result
    
    def generate_strategy_report(self):
        """Generate and export the final strategy report"""
        output_dir = self.create_output_directory()
        
        print("\n📊 Generating Final Report...")
        
        # Get final strategy from memory
        final_strategy = self.shared_memory.retrieve("final_strategy")
        
        # Save as markdown
        md_file = self.save_to_markdown(str(final_strategy), "marketing_strategy_report", output_dir)
        print(f"✅ Markdown report saved: {md_file}")
        
        # Convert to PDF
        pdf_file = self.convert_to_pdf(md_file, output_dir)
        if pdf_file:
            print(f"✅ PDF report saved: {pdf_file}")
        
        # Save raw data as JSON
        json_file = output_dir / "strategy_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.shared_memory.get_all(), f, indent=2, default=str)
        print(f"✅ Raw data saved: {json_file}")
        
        return output_dir, final_strategy
    
    def run(self):
        """Execute the complete strategy generation process"""
        print("\n🚀 STRATEGY AGENT SYSTEM INITIALIZED")
        print("=" * 60)
        print("Deploying 5 specialized AI agents for comprehensive analysis...")
        
        try:
            # Phase 1: Parallel intelligence gathering
            analysis_results = self.run_parallel_analysis()
            
            # Phase 2: Strategy composition
            strategy_result = self.run_strategy_composition(analysis_results)
            
            # Phase 3: QA supervision
            final_result = self.run_qa_supervision(strategy_result)
            
            # Phase 4: Report generation
            output_dir, final_strategy = self.generate_strategy_report()
            
            print("\n" + "=" * 60)
            print("🎉 STRATEGY GENERATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📁 Reports saved to: {output_dir}")
            print("\n📋 EXECUTIVE SUMMARY:")
            print("-" * 30)
            
            # Display key highlights
            return final_strategy, output_dir
            
        except Exception as e:
            print(f"\n❌ Error during strategy generation: {e}")
            return None, None

def collect_business_information():
    """Enhanced CLI for structured data collection"""
    print("\n" + "=" * 80)
    print("🏢 STRATEGY AGENT - COMPREHENSIVE MARKETING STRATEGY GENERATOR")
    print("=" * 80)
    print("This AI system deploys 5 specialized agents to create your marketing strategy:")
    print("\n🧩 Agents:")
    print("  🧾 Business Analyst - Gathers structured business intelligence")
    print("  🕵️ Competitor Analyst - Performs comprehensive market research")
    print("  📊 Marketing Evaluator - Analyzes current marketing performance")
    print("  🧠 Strategy Composer - Creates integrated marketing strategy")
    print("  ✅ QA Supervisor - Ensures quality and completeness")
    print("\n⚡ Features: Parallel processing, shared memory, PDF export")
    print("\n" + "=" * 80)
    
    # Business Information
    print("\n📊 SECTION 1: BUSINESS INFORMATION")
    print("-" * 40)
    business_info = input(dedent("""
    📝 Describe your business (industry, products/services, business model, stage):
    >>> """)).strip()
    
    # Goals and Objectives
    print("\n🎯 SECTION 2: GOALS & OBJECTIVES")
    print("-" * 40)
    business_goals = input(dedent("""
    🎯 What are your key business goals? (revenue targets, growth metrics, market expansion):
    >>> """)).strip()
    
    # Budget Information
    print("\n💰 SECTION 3: BUDGET & RESOURCES")
    print("-" * 40)
    budget_info = input(dedent("""
    💰 What's your marketing budget and team resources? (monthly/annual budget, team size):
    >>> """)).strip()
    
    # Current Marketing Efforts
    print("\n📈 SECTION 4: CURRENT MARKETING")
    print("-" * 40)
    current_marketing = input(dedent("""
    📈 Describe your current marketing efforts (channels, campaigns, performance, challenges):
    >>> """)).strip()
    
    return business_info, business_goals, budget_info, current_marketing

if __name__ == "__main__":
    try:
        # Collect business information via enhanced CLI
        business_info, business_goals, budget_info, current_marketing = collect_business_information()
        
        # Initialize and run the strategy system
        strategy_system = StrategyAgentSystem(
            business_info=business_info,
            business_goals=business_goals,
            budget_info=budget_info,
            current_marketing=current_marketing
        )
        
        # Execute strategy generation
        final_strategy, output_dir = strategy_system.run()
        
        if final_strategy and output_dir:
            print("\n🎊 SUCCESS! Your comprehensive marketing strategy is ready.")
            print(f"📁 Find your reports in: {output_dir}")
            print("\n📄 Files generated:")
            print("  • marketing_strategy_report.md (Markdown)")
            print("  • marketing_strategy_report.pdf (PDF)")
            print("  • strategy_data.json (Raw data)")
        else:
            print("\n❌ Strategy generation failed. Please check the logs above.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Process interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")