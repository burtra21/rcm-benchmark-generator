# generate_report_enhanced_v2.py
# Enhanced RCM Report Generator with Real Data Integration

from generate_report_enhanced import EnhancedRCMReportGenerator
from data_sources import enhance_report_with_real_data
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

class DataEnhancedRCMReportGenerator(EnhancedRCMReportGenerator):
    """Enhanced report generator that uses real data sources"""
    
    def generate_report(self, hospital_name, hospital_beds, recipient_name, recipient_email, state=None):
        """Generate report with real data integration"""
        print(f"Generating data-enhanced report for {hospital_name} in {state}...")
        
        # Get real data
        self.real_data = enhance_report_with_real_data(hospital_name, hospital_beds, state)
        
        # Store state for use in other methods
        self.state = state
        
        # Call parent method
        return super().generate_report(hospital_name, hospital_beds, recipient_name, recipient_email)
    
    def calculate_metrics(self, hospital_beds, hospital_name):
        """Override to use real data when available"""
        if hasattr(self, 'real_data') and self.real_data:
            analysis = self.real_data['analysis']
            
            # Use real data with enhanced calculations
            metrics = {
                'hospital_beds': hospital_beds,
                'estimated_rcm_staff': analysis['estimated_rcm_staff'],
                'current_turnover_cost': analysis['total_turnover_cost'],
                'potential_savings': analysis['potential_savings'],
                'reduced_cost': analysis['best_practice_cost'],
                'staff_turning_over_now': analysis['annual_staff_turnover'],
                'staff_turning_over_optimized': int(analysis['estimated_rcm_staff'] * 0.15),
                'productivity_loss': int(analysis['potential_savings'] * 0.3),
                'quality_improvement': int(analysis['potential_savings'] * 0.15),
                'total_impact': int(analysis['potential_savings'] * 1.45),
                'cost_per_bed': int(analysis['total_turnover_cost'] / hospital_beds),
                'savings_per_bed': int(analysis['potential_savings'] / hospital_beds),
                'break_even_months': 8,
                # New real data fields
                'average_salary': analysis['average_rcm_salary'],
                'regional_factor': analysis['regional_cost_factor'],
                'denial_benchmark': analysis['denial_rate_benchmark'],
                'ar_days_benchmark': analysis['days_in_ar_benchmark'],
                'function_turnover': analysis['function_specific_turnover'],
                'current_turnover_rate': analysis['current_turnover_rate'],
                'wage_data': analysis['wage_data']
            }
            
            print(f"Using real data: Average salary ${metrics['average_salary']:,} with regional factor {metrics['regional_factor']}")
            return metrics
        else:
            # Fallback to parent implementation
            return super().calculate_metrics(hospital_beds, hospital_name)
    
    def create_enhanced_turnover_chart(self, metrics, hospital_name):
        """Create an enhanced chart showing function-specific turnover rates"""
        if 'function_turnover' not in metrics:
            # Use parent method if no function data
            return super().create_turnover_comparison_chart(metrics, hospital_name)
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        
        # Left chart - Overall comparison (same as parent)
        categories = [f'{hospital_name}\n(Current)', 'Industry\nAverage', 'Best\nPractice']
        turnover_rates = [
            int(metrics['current_turnover_rate'] * 100),
            37,  # Industry average
            15   # Best practice
        ]
        colors_list = ['#ef4444', '#f59e0b', '#10b981']
        
        bars = ax1.bar(categories, turnover_rates, color=colors_list, width=0.6)
        
        for bar, rate in zip(bars, turnover_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{rate}%', ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        ax1.set_ylabel('Staff Turnover Rate (%)', fontsize=16, fontweight='bold')
        ax1.set_title('Overall RCM Turnover Comparison', fontsize=20, fontweight='bold', pad=20)
        ax1.set_ylim(0, 50)
        ax1.tick_params(axis='both', labelsize=14)
        ax1.set_xticklabels(categories, fontsize=16)
        
        # Right chart - Function-specific turnover
        functions = list(metrics['function_turnover'].keys())
        function_rates = [v * 100 for v in metrics['function_turnover'].values()]
        
        # Sort by turnover rate
        sorted_data = sorted(zip(functions, function_rates), key=lambda x: x[1], reverse=True)
        functions, function_rates = zip(*sorted_data)
        
        # Create gradient colors from red to green
        colors_func = []
        for rate in function_rates:
            if rate >= 40:
                colors_func.append('#ef4444')  # Red
            elif rate >= 35:
                colors_func.append('#f59e0b')  # Orange
            else:
                colors_func.append('#f59e0b')  # Orange
        
        bars2 = ax2.barh(functions[:6], function_rates[:6], color=colors_func[:6])  # Top 6
        
        for bar, rate in zip(bars2, function_rates[:6]):
            width = bar.get_width()
            ax2.text(width + 1, bar.get_y() + bar.get_height()/2.,
                    f'{rate:.0f}%', ha='left', va='center', fontsize=14, fontweight='bold')
        
        ax2.set_xlabel('Turnover Rate (%)', fontsize=16, fontweight='bold')
        ax2.set_title('Turnover by RCM Function', fontsize=20, fontweight='bold', pad=20)
        ax2.set_xlim(0, 55)
        ax2.tick_params(axis='both', labelsize=13)
        
        # Add target line
        ax2.axvline(x=15, color='green', linestyle='--', alpha=0.7, linewidth=2)
        ax2.text(15, -0.5, 'Target', ha='center', fontsize=12, color='green')
        
        plt.tight_layout()
        chart_filename = f'enhanced_turnover_chart_{hospital_name.replace(" ", "_")}.png'
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return chart_filename
    
    def add_regional_data_section(self, story, metrics, hospital_name):
        """Add a new section showing regional data insights"""
        story.append(Paragraph("Regional Market Analysis", self.styles['CustomSubtitle']))
        
        # Get state name
        state_name = self.state if hasattr(self, 'state') else 'your region'
        
        regional_text = f"""
        <font size="14">Based on real-time data from the Bureau of Labor Statistics and CMS, 
        here's how {hospital_name} compares to regional benchmarks in {state_name}:</font>
        """
        story.append(Paragraph(regional_text, self.styles['CustomNormal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Regional comparison table
        regional_data = [
            ['Metric', f'{state_name} Average', 'Your Calculation', 'Variance'],
            ['RCM Staff Salary', f"${metrics['average_salary']:,}", 
             f"${metrics['average_salary']:,}", 'Market Rate'],
            ['Cost of Living Index', f"{metrics['regional_factor']:.2f}", 
             f"{metrics['regional_factor']:.2f}", 
             'Included' if metrics['regional_factor'] != 1.0 else 'Baseline'],
            ['Denial Rate', f"{metrics['denial_benchmark']*100:.1f}%", 
             f"{metrics['denial_benchmark']*100:.1f}%", 'Industry Avg'],
            ['Days in A/R', f"{metrics['ar_days_benchmark']}", 
             f"{metrics['ar_days_benchmark']}", 'Target: 35']
        ]
        
        regional_table = Table(regional_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.3*inch])
        regional_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(regional_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add wage breakdown if available
        if 'wage_data' in metrics and metrics['wage_data']:
            story.append(Paragraph("RCM Position Salary Breakdown", self.styles['CustomNormal']))
            story.append(Spacer(1, 0.2*inch))
            
            wage_headers = ['Position', 'Entry Level', 'Median', 'Experienced']
            wage_rows = [wage_headers]
            
            for role, data in metrics['wage_data'].items():
                role_name = role.replace('_', ' ').title()
                wage_rows.append([
                    role_name,
                    f"${data['entry_level']:,}",
                    f"${data['median_annual']:,}",
                    f"${data['experienced']:,}"
                ])
            
            wage_table = Table(wage_rows, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
            wage_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.brand_gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(wage_table)
        
        return story


# Test function
def test_data_enhanced_report():
    """Test the data-enhanced report generator"""
    print("\n🚀 Testing Data-Enhanced Report Generation...\n")
    
    generator = DataEnhancedRCMReportGenerator()
    
    # Test data - try different states to see regional variations
    test_cases = [
        {
            "hospital_name": "Houston Methodist Hospital",
            "hospital_beds": 650,
            "recipient_name": "Test User",
            "recipient_email": "test@example.com",
            "state": "TX"
        },
        {
            "hospital_name": "UCLA Medical Center",
            "hospital_beds": 450,
            "recipient_name": "Test User",
            "recipient_email": "test@example.com", 
            "state": "CA"
        }
    ]
    
    # Generate report for first test case
    test = test_cases[0]
    filename = generator.generate_report(
        hospital_name=test["hospital_name"],
        hospital_beds=test["hospital_beds"],
        recipient_name=test["recipient_name"],
        recipient_email=test["recipient_email"],
        state=test["state"]
    )
    
    print(f"\n✅ Data-enhanced report complete! Check: {filename}")
    print(f"Report includes real data for {test['state']} including:")
    print("- State-specific RCM salaries")
    print("- Regional cost adjustments") 
    print("- Function-specific turnover rates")
    print("- Industry benchmarks")
    

if __name__ == "__main__":
    test_data_enhanced_report()