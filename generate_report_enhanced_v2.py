# generate_report_enhanced_v2.py
# This is a shortened version that imports and uses the real data

from generate_report_enhanced import EnhancedRCMReportGenerator
from data_sources import enhance_report_with_real_data
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import Paragraph, Spacer

class DataEnhancedRCMReportGenerator(EnhancedRCMReportGenerator):
    """Enhanced report generator that uses real data sources"""
    
    def generate_report(self, hospital_name, hospital_beds, recipient_name, recipient_email, state=None):
        """Generate report with real data integration"""
        print(f"Generating data-enhanced report for {hospital_name}...")
        
        # Get real data
        real_data = enhance_report_with_real_data(hospital_name, hospital_beds, state)
        
        # Use real data in calculations
        self.real_data = real_data
        
        # Call parent method
        return super().generate_report(hospital_name, hospital_beds, recipient_name, recipient_email)
    
    def calculate_metrics(self, hospital_beds, hospital_name):
        """Override to use real data when available"""
        if hasattr(self, 'real_data') and self.real_data:
            analysis = self.real_data['analysis']
            
            # Use real data with fallback to estimates
            return {
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
                'function_turnover': analysis['function_specific_turnover']
            }
        else:
            # Fallback to parent implementation
            return super().calculate_metrics(hospital_beds, hospital_name)


# Test it
if __name__ == "__main__":
    generator = DataEnhancedRCMReportGenerator()
    
    filename = generator.generate_report(
        hospital_name="Houston Methodist Hospital",
        hospital_beds=650,
        recipient_name="Test User",
        recipient_email="test@example.com",
        state="TX"
    )
    
    print(f"Enhanced report with real data: {filename}")