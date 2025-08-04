# generate_report.py
# This is your RCM Benchmark Report Generator

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

print("Starting RCM Benchmark Report Generator...")

class RCMBenchmarkReportGenerator:
    def __init__(self):
        """Initialize the report generator"""
        print("Initializing report generator...")
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Create custom styles for better looking reports"""
        # Title style - big blue text
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),  # Dark blue
            spaceAfter=30,
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#374151'),  # Dark gray
            spaceBefore=20,
            spaceAfter=15,
        ))
        
        print("Custom styles created!")
    
    def calculate_metrics(self, hospital_beds, hospital_name):
        """Calculate all the important metrics for the hospital"""
        print(f"Calculating metrics for {hospital_name}...")
        
        # Constants based on industry research
        AVERAGE_RCM_STAFF_PER_BED = 0.025  # 2.5 staff per 100 beds
        AVERAGE_RCM_SALARY = 85000
        CURRENT_TURNOVER_RATE = 0.40  # 40%
        BEST_PRACTICE_TURNOVER = 0.15  # 15%
        REPLACEMENT_COST_MULTIPLIER = 2.0  # 200% of salary
        
        # Calculate staff size
        estimated_staff = int(hospital_beds * AVERAGE_RCM_STAFF_PER_BED)
        
        # Calculate current turnover cost
        staff_turning_over = estimated_staff * CURRENT_TURNOVER_RATE
        current_cost = staff_turning_over * AVERAGE_RCM_SALARY * REPLACEMENT_COST_MULTIPLIER
        
        # Calculate potential savings
        reduced_staff_turnover = estimated_staff * BEST_PRACTICE_TURNOVER
        reduced_cost = reduced_staff_turnover * AVERAGE_RCM_SALARY * REPLACEMENT_COST_MULTIPLIER
        potential_savings = current_cost - reduced_cost
        
        metrics = {
            'hospital_beds': hospital_beds,
            'estimated_rcm_staff': estimated_staff,
            'current_turnover_cost': int(current_cost),
            'potential_savings': int(potential_savings),
            'reduced_cost': int(reduced_cost),
            'staff_turning_over_now': int(staff_turning_over),
            'staff_turning_over_optimized': int(reduced_staff_turnover)
        }
        
        print(f"Metrics calculated: {estimated_staff} staff, ${potential_savings:,} potential savings")
        return metrics
    
    def generate_report(self, hospital_name, hospital_beds, recipient_name, recipient_email):
        """Generate the complete PDF report"""
        print(f"Generating report for {hospital_name}...")
        
        # Calculate metrics
        metrics = self.calculate_metrics(hospital_beds, hospital_name)
        
        # Create filename
        safe_hospital_name = hospital_name.replace(' ', '_').replace('/', '_')
        filename = f"RCM_Benchmark_{safe_hospital_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []  # This will hold all our content
        
        # Title Page
        story.append(Paragraph(
            "RCM Staffing Crisis Benchmark Report",
            self.styles['CustomTitle']
        ))
        
        story.append(Paragraph(
            f"Prepared for: {recipient_name}<br/>"
            f"{hospital_name}<br/>"
            f"{datetime.now().strftime('%B %d, %Y')}",
            self.styles['Normal']
        ))
        
        story.append(Spacer(1, 1*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['CustomSubtitle']))
        
        summary_text = f"""
        Our analysis reveals that {hospital_name}, with {hospital_beds} beds and an estimated 
        {metrics['estimated_rcm_staff']} RCM staff members, is currently experiencing approximately 
        ${metrics['current_turnover_cost']:,} in annual turnover costs.
        <br/><br/>
        By implementing strategic outsourcing of high-burnout functions and reducing turnover 
        from 40% to 15%, your organization could save ${metrics['potential_savings']:,} annually.
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(PageBreak())
        
        # Current State Analysis
        story.append(Paragraph("Current State Analysis", self.styles['CustomSubtitle']))
        
      # Create data table
        data = [
            ['Metric', 'Current State', 'Industry Best Practice', 'Your Opportunity'],
            ['RCM Staff Size', f"{metrics['estimated_rcm_staff']}", f"{metrics['estimated_rcm_staff']}", '-'],
            ['Annual Turnover Rate', '40%', '15%', '25% reduction'],
            ['Staff Leaving Annually', 
             f"{metrics['staff_turning_over_now']}", 
             f"{metrics['staff_turning_over_optimized']}", 
             f"{metrics['staff_turning_over_now'] - metrics['staff_turning_over_optimized']} fewer"],
            ['Annual Turnover Cost', 
             f"${metrics['current_turnover_cost']:,}", 
             f"${metrics['reduced_cost']:,}", 
             f"${metrics['potential_savings']:,} savings"]
        ]
        
        # Create and style the table
        table = Table(data)
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Last column (opportunity) in green
            ('BACKGROUND', (3, 1), (3, -1), colors.lightgreen),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*inch))
        
        # Strategic Recommendations
        story.append(PageBreak())
        story.append(Paragraph("Strategic Recommendations", self.styles['CustomSubtitle']))
        
        recommendations = """
        <b>1. Immediate Actions (Next 30 Days)</b><br/>
        • Identify your highest turnover RCM functions<br/>
        • Calculate department-specific turnover costs<br/>
        • Survey staff to understand burnout drivers<br/>
        <br/>
        <b>2. Outsourcing Evaluation (Days 30-60)</b><br/>
        • Focus on these high-burnout functions:<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;- Denial management and appeals (45% typical turnover)<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;- Insurance follow-up (42% typical turnover)<br/>
        &nbsp;&nbsp;&nbsp;&nbsp;- Aged accounts receivable (38% typical turnover)<br/>
        • Request proposals from specialized vendors<br/>
        • Compare costs vs. current turnover expense<br/>
        <br/>
        <b>3. Implementation (Days 60-90)</b><br/>
        • Select strategic partners for high-burnout functions<br/>
        • Reinvest 30% of savings into retained staff compensation<br/>
        • Establish clear performance metrics<br/>
        """
        
        story.append(Paragraph(recommendations, self.styles['Normal']))
        
        # ROI Timeline
        story.append(PageBreak())
        story.append(Paragraph("Return on Investment Timeline", self.styles['CustomSubtitle']))
        
        # Simple ROI table
        roi_data = [
            ['Timeline', 'Investment', 'Savings', 'Net Benefit'],
            ['Months 1-6', '$225,000', f"${int(metrics['potential_savings']/2):,}", f"${int(metrics['potential_savings']/2 - 225000):,}"],
            ['Months 7-12', '$225,000', f"${int(metrics['potential_savings']/2):,}", f"${int(metrics['potential_savings']/2 - 225000):,}"],
            ['Year 2', '$400,000', f"${metrics['potential_savings']:,}", f"${metrics['potential_savings'] - 400000:,}"],
            ['3-Year Total', '$1,050,000', f"${metrics['potential_savings'] * 3:,}", f"${metrics['potential_savings'] * 3 - 1050000:,}"]
        ]
        
        roi_table = Table(roi_data)
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            # Highlight the 3-year total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(roi_table)
        
        # Call to Action
        story.append(Spacer(1, 1*inch))
        cta_text = """
        <para alignment="center">
        <b>Ready to Transform Your RCM Staffing Challenges?</b><br/>
        <br/>
        This report demonstrates clear financial benefits from addressing your RCM staffing crisis.<br/>
        The next step is a confidential consultation to discuss your specific situation.<br/>
        <br/>
        <b>Contact us today:</b><br/>
        Email: solutions@frost-arnett.com | Phone: 1-800-FROST-RCM<br/>
        <br/>
        <i>Frost-Arnett Company - Healthcare RCM Excellence Since 1893</i>
        </para>
        """
        
        story.append(Paragraph(cta_text, self.styles['Normal']))
        
        # Build the PDF
        print(f"Building PDF: {filename}")
        doc.build(story)
        
        print(f"✅ Report generated successfully: {filename}")
        return filename


# Test function to make sure everything works
def test_report_generation():
    """Test the report generator with sample data"""
    print("\n🚀 Testing Report Generation...\n")
    
    generator = RCMBenchmarkReportGenerator()
    
    # Test data
    test_hospital = "St. Mary's Hospital"
    test_beds = 250
    test_recipient = "Sarah Johnson"
    test_email = "sarah.johnson@stmarys.com"
    
    # Generate report
    filename = generator.generate_report(
        hospital_name=test_hospital,
        hospital_beds=test_beds,
        recipient_name=test_recipient,
        recipient_email=test_email
    )
    
    print(f"\n✅ Test complete! Check your folder for: {filename}")
    

# Run the test when this file is executed
if __name__ == "__main__":
    test_report_generation()