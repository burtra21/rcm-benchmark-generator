# generate_report_enhanced.py
# Enhanced RCM Benchmark Report Generator with Charts and Branding
# Updated with larger fonts and better page utilization

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas

# For charts
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

print("Starting Enhanced RCM Benchmark Report Generator...")

class EnhancedRCMReportGenerator:
    def __init__(self):
        """Initialize the enhanced report generator"""
        print("Initializing enhanced report generator...")
        self.styles = getSampleStyleSheet()
        self._setup_colors()
        self._setup_custom_styles()
        
    def _setup_colors(self):
        """Define brand colors"""
        self.brand_blue = colors.HexColor('#1e3a8a')
        self.brand_light_blue = colors.HexColor('#3b82f6')
        self.brand_green = colors.HexColor('#10b981')
        self.brand_red = colors.HexColor('#ef4444')
        self.brand_orange = colors.HexColor('#f59e0b')
        self.brand_gray = colors.HexColor('#6b7280')
        
    def _setup_custom_styles(self):
        """Create custom styles with better branding and larger fonts"""
        # Title style - BIGGER
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=36,  # Increased from 28
            textColor=self.brand_blue,
            spaceAfter=36,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=42  # Line height
        ))
        
        # Subtitle style - BIGGER
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=24,  # Increased from 18
            textColor=self.brand_blue,
            spaceBefore=24,
            spaceAfter=18,
            fontName='Helvetica-Bold',
            leading=28
        ))
        
        # Normal text - BIGGER
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=13,  # Increased from default 10
            leading=18,   # Better line spacing
            spaceBefore=6,
            spaceAfter=6
        ))
        
        # Highlight style for important numbers - BIGGER
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=18,  # Increased from 14
            textColor=self.brand_green,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=22
        ))
        
        # Large number style for key metrics
        self.styles.add(ParagraphStyle(
            name='BigNumber',
            parent=self.styles['Normal'],
            fontSize=48,  # Very large for impact
            textColor=self.brand_green,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=52
        ))
        
        # Medium number style
        self.styles.add(ParagraphStyle(
            name='MediumNumber',
            parent=self.styles['Normal'],
            fontSize=28,
            textColor=self.brand_blue,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=32
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=10,  # Keep footer smaller
            textColor=self.brand_gray,
            alignment=TA_CENTER
        ))
        
        # Bullet style
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=13,
            leading=20,
            leftIndent=20,
            bulletIndent=10
        ))
    
    def create_turnover_comparison_chart(self, metrics, hospital_name):
        """Create a visual turnover comparison chart"""
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))  # Bigger chart
        
        # Data
        categories = [f'{hospital_name}\n(Current)', 'Industry\nAverage', 'Best\nPractice']
        turnover_rates = [40, 35, 15]
        colors_list = ['#ef4444', '#f59e0b', '#10b981']
        
        # Create bars
        bars = ax.bar(categories, turnover_rates, color=colors_list, width=0.6)
        
        # Add value labels on bars - BIGGER FONT
        for bar, rate in zip(bars, turnover_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{rate}%', ha='center', va='bottom', fontsize=20, fontweight='bold')
        
        # Customize chart - BIGGER FONTS
        ax.set_ylabel('Staff Turnover Rate (%)', fontsize=16, fontweight='bold')
        ax.set_title('RCM Staff Turnover Rate Comparison', fontsize=22, fontweight='bold', pad=25)
        ax.set_ylim(0, 50)
        ax.grid(axis='y', alpha=0.3)
        ax.tick_params(axis='both', labelsize=14)
        
        # Set x-axis label font size
        ax.set_xticklabels(categories, fontsize=16)
        
        # Add a reference line for target
        ax.axhline(y=15, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Target Rate')
        ax.legend(fontsize=14)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        chart_filename = f'turnover_chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return chart_filename
    
    def create_cost_savings_chart(self, metrics):
        """Create a cost savings visualization"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # Bigger chart
        
        # Pie chart for cost breakdown
        current_cost = metrics['current_turnover_cost']
        saved_cost = metrics['potential_savings']
        remaining_cost = metrics['reduced_cost']
        
        # Donut chart
        sizes = [remaining_cost, saved_cost]
        colors_pie = ['#6b7280', '#10b981']
        explode = (0, 0.1)
        
        wedges, texts, autotexts = ax1.pie(sizes, labels=['Optimized Cost', 'Savings'], 
                                            colors=colors_pie, autopct='%1.0f%%',
                                            startangle=90, explode=explode,
                                            wedgeprops=dict(width=0.5),
                                            textprops={'fontsize': 16})  # Bigger font
        
        # Add center text - BIGGER
        ax1.text(0, 0, f'Total Current:\n${current_cost:,}', 
                ha='center', va='center', fontsize=18, fontweight='bold')
        
        ax1.set_title('Cost Optimization Potential', fontsize=18, fontweight='bold', pad=20)
        
        # Bar chart for 3-year projection
        years = ['Year 1', 'Year 2', 'Year 3']
        savings = [
            metrics['potential_savings'],
            metrics['potential_savings'],
            metrics['potential_savings']
        ]
        cumulative = np.cumsum(savings)
        
        bars = ax2.bar(years, cumulative, color='#10b981', alpha=0.7)
        
        # Add value labels - BIGGER
        for bar, cum in zip(bars, cumulative):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 50000,
                    f'${cum:,.0f}', ha='center', va='bottom', fontsize=16, fontweight='bold')
        
        ax2.set_ylabel('Cumulative Savings ($)', fontsize=16, fontweight='bold')
        ax2.set_title('3-Year Savings Projection', fontsize=18, fontweight='bold', pad=20)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        ax2.tick_params(axis='both', labelsize=14)
        ax2.grid(axis='y', alpha=0.3)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        chart_filename = f'savings_chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return chart_filename
    
    def create_roi_timeline_chart(self, metrics):
        """Create ROI timeline visualization"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))  # Bigger chart
        
        # Data
        months = np.arange(0, 37, 3)  # 0 to 36 months, every 3 months
        investment = []
        returns = []
        net_benefit = []
        
        for month in months:
            if month == 0:
                inv = 0
                ret = 0
            elif month <= 12:
                inv = (month/12) * 450000
                ret = (month/12) * metrics['potential_savings']
            elif month <= 24:
                inv = 450000 + ((month-12)/12) * 400000
                ret = metrics['potential_savings'] + ((month-12)/12) * metrics['potential_savings']
            else:
                inv = 450000 + 400000 + ((month-24)/12) * 400000
                ret = 2 * metrics['potential_savings'] + ((month-24)/12) * metrics['potential_savings']
            
            investment.append(inv)
            returns.append(ret)
            net_benefit.append(ret - inv)
        
        # Plot lines with bigger markers
        ax.plot(months, investment, 'o-', color='#ef4444', linewidth=3, markersize=10, label='Cumulative Investment')
        ax.plot(months, returns, 's-', color='#10b981', linewidth=3, markersize=10, label='Cumulative Savings')
        ax.fill_between(months, investment, returns, where=(np.array(returns) >= np.array(investment)), 
                        color='#10b981', alpha=0.3, label='Net Positive ROI')
        
        # Find break-even point
        for i, (inv, ret) in enumerate(zip(investment, returns)):
            if ret >= inv and i > 0:
                break_even_month = months[i]
                ax.plot(break_even_month, ret, 'o', color='#f59e0b', markersize=20, zorder=5)
                ax.annotate(f'Break-even\n({break_even_month} months)', 
                           xy=(break_even_month, ret), xytext=(break_even_month+3, ret+200000),
                           arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=3),
                           fontsize=16, fontweight='bold', color='#f59e0b')
                break
        
        # Customize chart - BIGGER FONTS
        ax.set_xlabel('Months', fontsize=18, fontweight='bold')
        ax.set_ylabel('Amount ($)', fontsize=18, fontweight='bold')
        ax.set_title('ROI Timeline Analysis', fontsize=22, fontweight='bold', pad=25)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        ax.tick_params(axis='both', labelsize=14)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=14)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        chart_filename = f'roi_timeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return chart_filename
    
    def calculate_metrics(self, hospital_beds, hospital_name):
        """Calculate all metrics with enhanced detail"""
        print(f"Calculating enhanced metrics for {hospital_name}...")
        
        # Base calculations (same as before)
        AVERAGE_RCM_STAFF_PER_BED = 0.025
        AVERAGE_RCM_SALARY = 85000
        CURRENT_TURNOVER_RATE = 0.40
        BEST_PRACTICE_TURNOVER = 0.15
        REPLACEMENT_COST_MULTIPLIER = 2.0
        
        estimated_staff = int(hospital_beds * AVERAGE_RCM_STAFF_PER_BED)
        staff_turning_over = estimated_staff * CURRENT_TURNOVER_RATE
        current_cost = staff_turning_over * AVERAGE_RCM_SALARY * REPLACEMENT_COST_MULTIPLIER
        reduced_staff_turnover = estimated_staff * BEST_PRACTICE_TURNOVER
        reduced_cost = reduced_staff_turnover * AVERAGE_RCM_SALARY * REPLACEMENT_COST_MULTIPLIER
        potential_savings = current_cost - reduced_cost
        
        # Enhanced metrics
        metrics = {
            'hospital_beds': hospital_beds,
            'estimated_rcm_staff': estimated_staff,
            'current_turnover_cost': int(current_cost),
            'potential_savings': int(potential_savings),
            'reduced_cost': int(reduced_cost),
            'staff_turning_over_now': int(staff_turning_over),
            'staff_turning_over_optimized': int(reduced_staff_turnover),
            # New metrics
            'productivity_loss': int(potential_savings * 0.3),  # 30% additional impact
            'quality_improvement': int(potential_savings * 0.15),  # 15% from better quality
            'total_impact': int(potential_savings * 1.45),  # Total including indirect benefits
            'cost_per_bed': int(current_cost / hospital_beds),
            'savings_per_bed': int(potential_savings / hospital_beds),
            'break_even_months': int(450000 / (potential_savings / 12)) if potential_savings > 0 else 999
        }
        
        return metrics
    
    def add_header_footer(self, canvas_obj, doc):
        """Add professional header and footer to each page"""
        canvas_obj.saveState()
        
        # Header
        canvas_obj.setFillColor(self.brand_blue)
        canvas_obj.setFont('Helvetica-Bold', 12)
        canvas_obj.drawString(0.75*inch, letter[1] - 0.5*inch, "CONFIDENTIAL - RCM Benchmark Analysis")
        canvas_obj.drawRightString(letter[0] - 0.75*inch, letter[1] - 0.5*inch, 
                                  datetime.now().strftime("%B %Y"))
        
        # Header line
        canvas_obj.setStrokeColor(self.brand_blue)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(0.75*inch, letter[1] - 0.6*inch, letter[0] - 0.75*inch, letter[1] - 0.6*inch)
        
        # Footer
        canvas_obj.setFont('Helvetica', 10)
        canvas_obj.setFillColor(self.brand_gray)
        canvas_obj.drawString(0.75*inch, 0.5*inch, 
                             "Frost-Arnett Company | Healthcare Revenue Excellence Since 1893")
        canvas_obj.drawRightString(letter[0] - 0.75*inch, 0.5*inch, 
                                  f"Page {canvas_obj.getPageNumber()}")
        
        # Footer line
        canvas_obj.setLineWidth(1)
        canvas_obj.line(0.75*inch, 0.65*inch, letter[0] - 0.75*inch, 0.65*inch)
        
        canvas_obj.restoreState()
    
    def generate_report(self, hospital_name, hospital_beds, recipient_name, recipient_email):
        """Generate the enhanced PDF report"""
        print(f"Generating enhanced report for {hospital_name}...")
        
        # Calculate metrics
        metrics = self.calculate_metrics(hospital_beds, hospital_name)
        
        # Generate charts
        turnover_chart = self.create_turnover_comparison_chart(metrics, hospital_name)
        savings_chart = self.create_cost_savings_chart(metrics)
        roi_chart = self.create_roi_timeline_chart(metrics)
        
        # Create filename
        safe_hospital_name = hospital_name.replace(' ', '_').replace('/', '_')
        filename = f"Enhanced_RCM_Benchmark_{safe_hospital_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Create PDF with smaller margins for more content space
        doc = SimpleDocTemplate(
            filename, 
            pagesize=letter,
            topMargin=0.75*inch,      # Reduced from 1 inch
            bottomMargin=0.75*inch,   # Reduced from 1 inch
            leftMargin=0.75*inch,     # Reduced from default
            rightMargin=0.75*inch     # Reduced from default
        )
        
        story = []
        
        # Cover Page
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph(
            "RCM Staffing Crisis<br/>Benchmark Analysis",
            self.styles['CustomTitle']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Client info box - BIGGER
        client_info = f"""
        <para alignment="center">
        <font size="16"><b>Prepared For:</b></font><br/>
        <font size="18">{recipient_name}</font><br/>
        <font size="18">{hospital_name}</font><br/>
        <br/>
        <font size="16"><b>Analysis Date:</b></font><br/>
        <font size="16">{datetime.now().strftime('%B %d, %Y')}</font><br/>
        <br/>
        <font size="16"><b>Facility Size:</b></font><br/>
        <font size="18">{hospital_beds} Beds</font>
        </para>
        """
        story.append(Paragraph(client_info, self.styles['CustomNormal']))
        
        story.append(Spacer(1, 1.5*inch))
        
        # Key finding highlight - MUCH BIGGER
        story.append(Paragraph(
            "Potential Annual Savings Identified:",
            self.styles['Highlight']
        ))
        story.append(Paragraph(
            f"${metrics['potential_savings']:,}",
            self.styles['BigNumber']
        ))
        
        story.append(PageBreak())
        
        # Executive Dashboard
        story.append(Paragraph("Executive Dashboard", self.styles['CustomSubtitle']))
        
        # Key metrics table - BIGGER FONTS
        dashboard_data = [
            ['Key Performance Indicators', 'Current State', 'Target State', 'Impact'],
            ['Staff Turnover Rate', '40%', '15%', '↓ 62.5%'],
            ['Annual Turnover Cost', f"${metrics['current_turnover_cost']:,}", 
             f"${metrics['reduced_cost']:,}", f"Save ${metrics['potential_savings']:,}"],
            ['Cost Per Bed', f"${metrics['cost_per_bed']:,}", 
             f"${int(metrics['cost_per_bed'] * 0.375):,}", f"↓ ${metrics['savings_per_bed']:,}"],
            ['Staff Departures/Year', f"{metrics['staff_turning_over_now']}", 
             f"{metrics['staff_turning_over_optimized']}", 
             f"↓ {metrics['staff_turning_over_now'] - metrics['staff_turning_over_optimized']}"],
            ['Break-Even Timeline', '-', f"{metrics['break_even_months']} months", 'Quick ROI']
        ]
        
        dashboard_table = Table(dashboard_data, colWidths=[2.5*inch, 1.5*inch, 1.7*inch, 1.7*inch])
        dashboard_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 13),  # Bigger header
            ('FONTSIZE', (0, 1), (-1, -1), 12),  # Bigger body
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            # Data rows
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Impact column
            ('BACKGROUND', (3, 1), (3, -1), self.brand_green),
            ('TEXTCOLOR', (3, 1), (3, -1), colors.whitesmoke),
            ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(dashboard_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Add turnover comparison chart - BIGGER
        story.append(Image(turnover_chart, width=6.5*inch, height=4.3*inch))
        
        story.append(PageBreak())
        
        # Financial Impact Analysis
        story.append(Paragraph("Financial Impact Analysis", self.styles['CustomSubtitle']))
        
        impact_text = f"""
        <font size="14">Our comprehensive analysis reveals significant financial opportunities through strategic 
        RCM workforce optimization at {hospital_name}:</font>
        <br/><br/>
        <font size="14"><b>Direct Cost Savings:</b> ${metrics['potential_savings']:,} annually<br/>
        <b>Productivity Recovery:</b> ${metrics['productivity_loss']:,} annually<br/>
        <b>Quality Improvements:</b> ${metrics['quality_improvement']:,} annually<br/>
        <b>Total Potential Impact:</b> ${metrics['total_impact']:,} annually</font>
        """
        
        story.append(Paragraph(impact_text, self.styles['CustomNormal']))
        story.append(Spacer(1, 0.4*inch))
        
        # Add savings charts - BIGGER
        story.append(Image(savings_chart, width=7*inch, height=3*inch))
        
        story.append(PageBreak())
        
        # ROI Analysis
        story.append(Paragraph("Return on Investment Analysis", self.styles['CustomSubtitle']))
        
        story.append(Paragraph(
            "<font size='14'>The following analysis demonstrates the compelling ROI timeline for implementing "
            "strategic RCM outsourcing initiatives:</font>",
            self.styles['CustomNormal']
        ))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Image(roi_chart, width=6.5*inch, height=4.3*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # ROI Summary Table - BIGGER
        roi_summary = [
            ['Investment Period', 'Investment', 'Savings', 'Net Benefit', 'ROI %'],
            ['Year 1', '$450,000', f"${metrics['potential_savings']:,}", 
             f"${metrics['potential_savings'] - 450000:,}", 
             f"{((metrics['potential_savings'] - 450000) / 450000 * 100):.0f}%"],
            ['Year 2', '$400,000', f"${metrics['potential_savings']:,}", 
             f"${metrics['potential_savings'] - 400000:,}",
             f"{((metrics['potential_savings'] - 400000) / 400000 * 100):.0f}%"],
            ['Year 3', '$400,000', f"${metrics['potential_savings']:,}", 
             f"${metrics['potential_savings'] - 400000:,}",
             f"{((metrics['potential_savings'] - 400000) / 400000 * 100):.0f}%"],
            ['3-Year Total', '$1,250,000', f"${metrics['potential_savings'] * 3:,}", 
             f"${(metrics['potential_savings'] * 3) - 1250000:,}",
             f"{(((metrics['potential_savings'] * 3) - 1250000) / 1250000 * 100):.0f}%"]
        ]
        
        roi_table = Table(roi_summary, colWidths=[1.6*inch, 1.4*inch, 1.4*inch, 1.5*inch, .9*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Bigger
            ('FONTSIZE', (0, 1), (-1, -1), 11),  # Bigger
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), self.brand_green),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(roi_table)
        
        # Implementation Roadmap
        story.append(PageBreak())
        story.append(Paragraph("Implementation Roadmap", self.styles['CustomSubtitle']))
        
        # Timeline visualization - BIGGER
        timeline_data = [
            ['Phase', 'Timeline', 'Key Activities', 'Expected Outcomes'],
            ['Discovery & Assessment', 'Days 1-30', 
             '• Detailed turnover analysis\n• Function-specific assessment\n• Vendor evaluation', 
             'Clear action plan'],
            ['Pilot Implementation', 'Days 31-90', 
             '• Select high-impact function\n• Partner selection\n• Process documentation', 
             '25% turnover reduction'],
            ['Scale & Optimize', 'Days 91-180', 
             '• Expand to additional functions\n• Technology integration\n• Staff development', 
             '50% turnover reduction'],
            ['Full Transformation', 'Days 181-365', 
             '• Complete implementation\n• Continuous improvement\n• Performance monitoring', 
             'Achieve 15% turnover rate']
        ]
        
        timeline_table = Table(timeline_data, colWidths=[2.0*inch, 1.1*inch, 2.5*inch, 1.8*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Bigger
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Bigger
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(timeline_table)
        
        # Next Steps
        story.append(PageBreak())
        story.append(Paragraph("Your Next Steps", self.styles['CustomSubtitle']))
        
        next_steps_text = """
        <font size="14"><b>1. Schedule Your Strategy Session (This Week)</b><br/>
        Our RCM transformation experts will conduct a confidential review of your specific 
        challenges and opportunities. This 60-minute session includes:<br/>
        • Detailed analysis of your RCM department structure<br/>
        • Identification of highest-impact outsourcing opportunities<br/>
        • Customized implementation timeline<br/>
        • ROI projections based on your actual data<br/>
        <br/>
        
        <b>2. Receive Your Custom Transformation Plan (Within 5 Days)</b><br/>
        Following our strategy session, you'll receive:<br/>
        • Function-by-function outsourcing recommendations<br/>
        • Vendor evaluation criteria specific to your needs<br/>
        • Risk mitigation strategies<br/>
        • Month-by-month implementation roadmap<br/>
        <br/>
        
        <b>3. Begin Your Pilot Program (Within 30 Days)</b><br/>
        Start with your highest-turnover function to:<br/>
        • Prove the ROI model with minimal risk<br/>
        • Build internal confidence in the approach<br/>
        • Refine processes before full-scale implementation<br/>
        • Generate quick wins to fund expansion</font>
        """
        
        story.append(Paragraph(next_steps_text, self.styles['CustomNormal']))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Call to action box - BIGGER
        cta_text = """
        <para alignment="center">
        <font size="20"><b>Ready to Transform Your RCM Workforce Challenges?</b></font><br/>
        <br/>
        <font size="18">Schedule Your Confidential Strategy Session Today</font><br/>
        <br/>
        <font size="16"><b>Call: 1-800-FROST-RCM</b><br/>
        <b>Email: solutions@frost-arnett.com</b><br/>
        <b>Web: www.frost-arnett.com/rcm-transformation</b></font><br/>
        <br/>
        <font size="14"><i>Mention reference code: STAFF-{} for priority scheduling</i></font>
        </para>
        """.format(datetime.now().strftime('%Y%m'))
        
        story.append(Paragraph(cta_text, self.styles['CustomNormal']))
        
        # Build PDF with header/footer
        doc.build(story, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        
        # Clean up chart files
        for chart in [turnover_chart, savings_chart, roi_chart]:
            if os.path.exists(chart):
                os.remove(chart)
        
        print(f"✅ Enhanced report generated successfully: {filename}")
        return filename


# Test function
def test_enhanced_report():
    """Test the enhanced report generator"""
    print("\n🚀 Testing Enhanced Report Generation...\n")
    
    generator = EnhancedRCMReportGenerator()
    
    # Test data
    filename = generator.generate_report(
        hospital_name="Regional Medical Center",
        hospital_beds=350,
        recipient_name="Sarah Johnson",
        recipient_email="sarah.johnson@rmc.com"
    )
    
    print(f"\n✅ Enhanced report complete! Check: {filename}")
    

if __name__ == "__main__":
    test_enhanced_report()