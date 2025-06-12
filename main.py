import os
import json
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from decouple import config
import markdown

from textwrap import dedent

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
# Remove organization header to avoid conflicts
if "OPENAI_ORGANIZATION" in os.environ:
    del os.environ["OPENAI_ORGANIZATION"]

# Optional PDF generation - only import if available
try:
    from weasyprint import HTML, CSS
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  WeasyPrint not available - PDF generation disabled. Only Markdown reports will be generated.")

class StrategyAgentSystem:
    """Multi-agent system for comprehensive marketing strategy generation"""
    
    def __init__(self, business_info, business_goals, budget_info, current_marketing):
        self.business_info = business_info
        self.business_goals = business_goals
        self.budget_info = budget_info
        self.current_marketing = current_marketing
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    def create_output_directory(self):
        """Create output directory for reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"strategy_reports/{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def save_to_html(self, markdown_file, output_dir):
        """Convert markdown to styled HTML as PDF alternative"""
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
                    body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 40px; max-width: 1200px; }}
                    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                    h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
                    h3 {{ color: #2c3e50; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                    th {{ background-color: #f8f9fa; font-weight: bold; }}
                    .executive-summary {{ background-color: #f8f9fa; padding: 20px; border-left: 4px solid #3498db; margin: 20px 0; }}
                    ul, ol {{ margin: 10px 0; padding-left: 30px; }}
                    .print-button {{ position: fixed; top: 20px; right: 20px; background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
                </style>
                <script>
                    function printReport() {{
                        window.print();
                    }}
                </script>
            </head>
            <body>
                <button class="print-button" onclick="printReport()">🖨️ Print Report</button>
                {html_content}
            </body>
            </html>
            """
            
            html_file = output_dir / "marketing_strategy_report.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(styled_html)
            return html_file
        except Exception as e:
            print(f"HTML conversion failed: {e}")
            return None
    
    def run(self):
        """Execute the complete strategy generation process using the proven working approach"""
        print("\n🚀 STRATEGY AGENT SYSTEM INITIALIZED")
        print("=" * 60)
        print("Deploying 3 specialized AI agents for comprehensive analysis...")
        
        try:
            # Create simple, proven working agents
            business_analyst = Agent(
                role="Business Intelligence Analyst",
                goal="Analyze business information and create customer personas",
                backstory="You are a business analyst expert with deep knowledge of market analysis and customer segmentation.",
                llm=self.llm,
                verbose=True
            )
            
            competitor_analyst = Agent(
                role="Competitive Intelligence Specialist", 
                goal="Research competitors and identify market opportunities",
                backstory="You are a market research expert specializing in competitive analysis and industry insights with extensive knowledge of the EdTech industry.",
                llm=self.llm,
                verbose=True
            )
            
            strategy_composer = Agent(
                role="Marketing Strategy Consultant",
                goal="Create comprehensive marketing strategies with budget allocations",
                backstory="You are a senior marketing strategist with expertise in digital marketing and growth strategies.",
                llm=self.llm,
                verbose=True
            )
            
            # Phase 1: Business Analysis
            print("\n🔄 Phase 1: Business Intelligence Analysis")
            print("=" * 50)
            
            business_task = Task(
                description=f"""Conduct comprehensive business intelligence analysis for:
                
                Business: {self.business_info}
                Goals: {self.business_goals}
                Budget: {self.budget_info}
                Current Marketing: {self.current_marketing}
                
                Provide:
                1. Company Overview (extract business name, industry, core offering, business model)
                2. Mission, Vision, Values (create professional statements)
                3. Market & Industry Analysis (market size, trends, regulations, barriers)
                4. SWOT Analysis (detailed strengths, weaknesses, opportunities, threats)
                5. Strategic Goals (convert goals into SMART objectives)
                6. Target Customer Personas (3-4 detailed personas with demographics, behaviors, pain points)
                7. Resource Assessment (team, budget allocation, infrastructure needs)
                8. Financial Projections (revenue, CAC, LTV, burn rate projections)""",
                expected_output="Comprehensive business intelligence report with company overview, market analysis, SWOT, strategic goals, personas, and financial projections.",
                agent=business_analyst
            )
            
            business_crew = Crew(
                agents=[business_analyst],
                tasks=[business_task],
                verbose=True
            )
            business_result = business_crew.kickoff()
            print("✅ Business analysis completed!")
            
            # Phase 2: Competitor Analysis
            print("\n🕵️ Phase 2: Competitive Intelligence Gathering")
            print("=" * 50)
            
            competitor_task = Task(
                description=f"""Conduct detailed competitive intelligence analysis for: {self.business_info}
                
                Use your knowledge of the EdTech industry to identify REAL competitors and create comprehensive competitor analysis including:
                
                1. **Top Competitors Comparison Table** with:
                   - Competitor name, founding year, core product, business model
                   - Total funding, key investors, market presence
                   - Key strengths and weaknesses
                   - Pricing strategies and marketing approaches
                   
                2. **Digital Presence Analysis**:
                   - SEO and content marketing strategies
                   - Social media presence and engagement
                   - Partnership and collaboration strategies
                   
                3. **Market Positioning Analysis**:
                   - Competitive advantages and differentiators
                   - Market share insights and positioning gaps
                   - Opportunities for differentiation
                   
                4. **Industry Insights**:
                   - Funding trends and investment patterns
                   - Technology trends and innovation areas
                   - Regulatory landscape and compliance requirements
                   
                Provide specific, actionable insights for competitive positioning and market entry strategies.""",
                expected_output="Comprehensive competitor analysis with comparison table, digital presence analysis, positioning insights, and strategic recommendations.",
                agent=competitor_analyst
            )
            
            competitor_crew = Crew(
                agents=[competitor_analyst],
                tasks=[competitor_task], 
                verbose=True
            )
            competitor_result = competitor_crew.kickoff()
            print("✅ Competitor analysis completed!")
            
            # Phase 3: Strategy Creation
            print("\n🧠 Phase 3: Marketing Strategy Composition")
            print("=" * 50)
            
            strategy_task = Task(
                description=f"""Create a comprehensive business and marketing strategy document using:
                
                Business Analysis: {business_result}
                Competitor Analysis: {competitor_result}
                Budget Available: {self.budget_info}
                Current Marketing: {self.current_marketing}
                Goals: {self.business_goals}
                
                Create a detailed strategy document with these sections:
                
                **1. Executive Summary**
                - Strategic priorities and key recommendations
                - Expected outcomes and ROI projections
                - Critical success factors
                
                **2. Action Plan & Initiatives Table**
                - Specific initiatives with owners, timelines, and milestones
                - Implementation roadmap with quarterly breakdown
                
                **3. Resource Allocation Strategy**
                - Team structure and hiring plans
                - Budget allocation across functions
                - Technology and infrastructure requirements
                
                **4. Financial Projections Table**
                - Revenue targets (ARR, MRR growth)
                - Cost structure (CAC, LTV, burn rate)
                - Profitability timeline and key metrics
                
                **5. Marketing Channel Strategy**
                - Digital marketing (SEO, content, social media, paid ads)
                - Traditional marketing (conferences, partnerships, PR)
                - Channel-specific budget allocation and expected ROI
                - Customer acquisition and retention strategies
                
                **6. Risk Assessment & Mitigation**
                - Market risks, competitive threats, operational risks
                - Probability assessment and mitigation strategies
                
                **7. Monitoring & KPI Framework**
                - Success metrics for each strategic goal
                - Review cycles and optimization processes
                - Dashboard and tracking recommendations
                
                Ensure all recommendations are specific, measurable, and aligned with achieving: {self.business_goals}""",
                expected_output="Comprehensive business strategy document with executive summary, action plans, resource allocation, financial projections, marketing strategy, risk assessment, and KPI framework.",
                agent=strategy_composer
            )
            
            strategy_crew = Crew(
                agents=[strategy_composer],
                tasks=[strategy_task],
                verbose=True
            )
            strategy_result = strategy_crew.kickoff()
            print("✅ Marketing strategy completed!")
            
            # Phase 4: Report Generation
            print("\n📊 Phase 4: Report Generation")
            print("=" * 50)
            
            output_dir = self.create_output_directory()
            
            # Create comprehensive markdown report in the format you requested
            md_content = f"""# Comprehensive Business Strategy Report
**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## Executive Summary
This comprehensive strategy document outlines a growth-focused roadmap to achieve the strategic objectives: {self.business_goals}

---

## Business Intelligence Analysis
{business_result}

---

## Competitive Intelligence & Market Analysis  
{competitor_result}

---

## Strategic Business Plan & Marketing Strategy
{strategy_result}

---

## Implementation Roadmap
### Phase 1: Foundation (Month 1-2)
- Set up tracking and analytics systems
- Implement core marketing infrastructure
- Launch priority customer acquisition channels

### Phase 2: Optimization (Month 3-4)  
- Optimize based on initial performance data
- Scale successful channels and campaigns
- Refine customer targeting and messaging

### Phase 3: Growth (Month 5-6)
- Scale successful channels and test new opportunities
- Expand into new market segments
- Implement retention and upselling strategies

### Phase 4: Review & Scale (Quarterly)
- Comprehensive strategy review and adjustments
- Performance analysis against KPIs
- Strategic pivots based on market feedback

---

## Conclusion
This strategic framework provides a clear path to achieving sustainable growth and market leadership. Success will depend on disciplined execution, continuous optimization, and maintaining focus on key performance indicators while adapting to market dynamics.

---

**Report Prepared By:** Strategy Agent AI System   
**Date:** {datetime.now().strftime("%B %d, %Y")}
"""
            
            # Save markdown file
            md_file = output_dir / "marketing_strategy_report.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"✅ Markdown report saved: {md_file}")
            
            # Create HTML version
            html_file = self.save_to_html(md_file, output_dir)
            if html_file:
                print(f"✅ HTML report saved: {html_file}")
                print("   💡 Open the HTML file in your browser and use Ctrl+P to print as PDF")
            
            # Save raw data as JSON
            json_file = output_dir / "strategy_data.json"
            strategy_data = {
                "business_info": self.business_info,
                "business_goals": self.business_goals,
                "budget_info": self.budget_info,
                "current_marketing": self.current_marketing,
                "business_analysis": str(business_result),
                "competitor_analysis": str(competitor_result),
                "marketing_strategy": str(strategy_result),
                "generated_at": datetime.now().isoformat()
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(strategy_data, f, indent=2, default=str)
            print(f"✅ Raw data saved: {json_file}")
            
            print("\n" + "=" * 60)
            print("🎉 STRATEGY GENERATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📁 Reports saved to: {output_dir}")
            print("\n📋 EXECUTIVE SUMMARY:")
            print("-" * 30)
            
            return strategy_result, output_dir
            
        except Exception as e:
            print(f"\n❌ Error during strategy generation: {e}")
            import traceback
            traceback.print_exc()
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
    business_name = input(dedent("""
    🏢 What is your business name?
    >>> """)).strip()
    
    business_info = input(dedent("""
    📝 Describe your business (industry, products/services, business model, stage):
    >>> """)).strip()
    
    # Combine business name with description
    business_info = f"Business Name: {business_name}. {business_info}"
    
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
            print("  • marketing_strategy_report.html (HTML - can be printed as PDF)")
            print("  • strategy_data.json (Raw data)")
        else:
            print("\n❌ Strategy generation failed. Please check the logs above.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Process interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")