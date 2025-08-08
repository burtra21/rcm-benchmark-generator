# app.py
# Complete RCM Benchmark Report Generator Web Application with Clay Integration

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime
import os

# Import your enhanced report generator with data
from generate_report_enhanced_v2 import DataEnhancedRCMReportGenerator

# Create FastAPI app
app = FastAPI(title="RCM Benchmark Report Generator")

# HTML form for the web interface
@app.get("/", response_class=HTMLResponse)
async def show_form():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RCM Benchmark Report Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f0f0f0;
            }
            .container {
                background-color: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            h1 {
                color: #1e3a8a;
                text-align: center;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #6b7280;
                text-align: center;
                margin-bottom: 30px;
                font-size: 18px;
            }
            .feature-list {
                background-color: #f3f4f6;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
                font-size: 14px;
            }
            .feature-list h3 {
                color: #1e3a8a;
                margin-top: 0;
                font-size: 18px;
            }
            .feature-list ul {
                margin: 10px 0;
                padding-left: 25px;
                line-height: 1.8;
            }
            .feature-list li {
                margin-bottom: 5px;
            }
            .new-badge {
                background-color: #10b981;
                color: white;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                margin-left: 5px;
            }
            label {
                display: block;
                margin-top: 18px;
                font-weight: bold;
                color: #374151;
                font-size: 14px;
            }
            input, select {
                width: 100%;
                padding: 12px;
                margin-top: 6px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                box-sizing: border-box;
                font-size: 16px;
                background-color: white;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #3b82f6;
                background-color: #f9fafb;
            }
            select {
                cursor: pointer;
            }
            button {
                background-color: #1e3a8a;
                color: white;
                padding: 16px 30px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                margin-top: 30px;
                width: 100%;
                transition: all 0.3s;
            }
            button:hover {
                background-color: #1e3366;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
            }
            .footer {
                text-align: center;
                margin-top: 35px;
                color: #6b7280;
                font-size: 14px;
                line-height: 1.5;
            }
            .loading {
                display: none;
                text-align: center;
                margin-top: 25px;
                padding: 20px;
                background-color: #eff6ff;
                border-radius: 8px;
                color: #1e3a8a;
            }
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #e5e7eb;
                border-radius: 50%;
                border-top-color: #1e3a8a;
                animation: spin 1s ease-in-out infinite;
                margin-right: 10px;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            .row {
                display: flex;
                gap: 15px;
            }
            .col {
                flex: 1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>RCM Staffing Crisis Analyzer</h1>
            <p class="subtitle">Professional Benchmark Report Generator with Real Healthcare Data</p>
            
            <div class="feature-list">
                <h3>Your Data-Enhanced Report Includes:</h3>
                <ul>
                    <li>📊 Visual charts showing turnover comparison & cost savings</li>
                    <li>💰 ROI timeline with break-even analysis</li>
                    <li>📈 3-year financial projections</li>
                    <li>🏥 Hospital-specific calculations based on size & location</li>
                    <li>📍 Regional salary data from Bureau of Labor Statistics<span class="new-badge">NEW</span></li>
                    <li>🎯 Industry benchmarks from MGMA/HFMA reports<span class="new-badge">NEW</span></li>
                    <li>💡 Function-specific turnover rates (denial mgmt, coding, etc.)<span class="new-badge">NEW</span></li>
                    <li>📋 Custom implementation roadmap</li>
                </ul>
            </div>
            
            <form action="/generate" method="post" onsubmit="showLoading()">
                <label for="hospital_name">Hospital Name:</label>
                <input type="text" id="hospital_name" name="hospital_name" required 
                       placeholder="e.g., Regional Medical Center"
                       autocomplete="organization">
                
                <div class="row">
                    <div class="col">
                        <label for="hospital_beds">Number of Beds:</label>
                        <input type="number" id="hospital_beds" name="hospital_beds" required 
                               placeholder="e.g., 350" min="50" max="2000">
                    </div>
                    
                    <div class="col">
                        <label for="state">State:</label>
                        <select id="state" name="state" required>
                            <option value="">Select State</option>
                            <option value="AL">Alabama</option>
                            <option value="AK">Alaska</option>
                            <option value="AZ">Arizona</option>
                            <option value="AR">Arkansas</option>
                            <option value="CA">California</option>
                            <option value="CO">Colorado</option>
                            <option value="CT">Connecticut</option>
                            <option value="DE">Delaware</option>
                            <option value="FL">Florida</option>
                            <option value="GA">Georgia</option>
                            <option value="HI">Hawaii</option>
                            <option value="ID">Idaho</option>
                            <option value="IL">Illinois</option>
                            <option value="IN">Indiana</option>
                            <option value="IA">Iowa</option>
                            <option value="KS">Kansas</option>
                            <option value="KY">Kentucky</option>
                            <option value="LA">Louisiana</option>
                            <option value="ME">Maine</option>
                            <option value="MD">Maryland</option>
                            <option value="MA">Massachusetts</option>
                            <option value="MI">Michigan</option>
                            <option value="MN">Minnesota</option>
                            <option value="MS">Mississippi</option>
                            <option value="MO">Missouri</option>
                            <option value="MT">Montana</option>
                            <option value="NE">Nebraska</option>
                            <option value="NV">Nevada</option>
                            <option value="NH">New Hampshire</option>
                            <option value="NJ">New Jersey</option>
                            <option value="NM">New Mexico</option>
                            <option value="NY">New York</option>
                            <option value="NC">North Carolina</option>
                            <option value="ND">North Dakota</option>
                            <option value="OH">Ohio</option>
                            <option value="OK">Oklahoma</option>
                            <option value="OR">Oregon</option>
                            <option value="PA">Pennsylvania</option>
                            <option value="RI">Rhode Island</option>
                            <option value="SC">South Carolina</option>
                            <option value="SD">South Dakota</option>
                            <option value="TN">Tennessee</option>
                            <option value="TX">Texas</option>
                            <option value="UT">Utah</option>
                            <option value="VT">Vermont</option>
                            <option value="VA">Virginia</option>
                            <option value="WA">Washington</option>
                            <option value="WV">West Virginia</option>
                            <option value="WI">Wisconsin</option>
                            <option value="WY">Wyoming</option>
                        </select>
                    </div>
                </div>
                
                <label for="recipient_name">Recipient Name:</label>
                <input type="text" id="recipient_name" name="recipient_name" required 
                       placeholder="e.g., Sarah Johnson"
                       autocomplete="name">
                
                <label for="recipient_email">Recipient Email:</label>
                <input type="email" id="recipient_email" name="recipient_email" required 
                       placeholder="e.g., sarah.johnson@hospital.com"
                       autocomplete="email">
                
                <button type="submit">Generate Enhanced Report</button>
            </form>
            
            <div class="loading" id="loading">
                <div><span class="loading-spinner"></span>Generating your enhanced report with real data...</div>
                <p>This may take 15-20 seconds.</p>
            </div>
            
            <div class="footer">
                <p>Powered by Frost-Arnett Company | Healthcare Excellence Since 1893</p>
            </div>
        </div>
        
        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

# Handle form submission - using Enhanced generator with real data
@app.post("/generate")
async def generate_report(
    hospital_name: str = Form(...),
    hospital_beds: int = Form(...),
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    state: str = Form(...)
):
    try:
        # Create enhanced generator with data sources
        generator = DataEnhancedRCMReportGenerator()
        
        # Generate the enhanced report with real data
        filename = generator.generate_report(
            hospital_name=hospital_name,
            hospital_beds=hospital_beds,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            state=state
        )
        
        # Return the file for download
        return FileResponse(
            filename,
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Enhanced RCM Benchmark Report Generator", 
        "version": "3.0",
        "features": ["real_data", "charts", "roi_analysis", "clay_integration"]
    }

# API endpoint for N8N integration
@app.post("/api/generate")
async def api_generate_report(
    hospital_name: str = Form(...),
    hospital_beds: int = Form(...),
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    state: str = Form(...)
):
    """API endpoint for programmatic access (N8N, webhooks, etc.)"""
    try:
        generator = DataEnhancedRCMReportGenerator()
        filename = generator.generate_report(
            hospital_name=hospital_name,
            hospital_beds=hospital_beds,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            state=state
        )
        
        return {
            "status": "success",
            "filename": filename,
            "message": f"Enhanced report generated for {hospital_name}",
            "location": f"{hospital_name}, {state}",
            "features": ["real_wage_data", "regional_adjustments", "industry_benchmarks"]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Webhook endpoint for N8N integration with Clay
@app.post("/webhook/send-to-clay")
async def send_to_clay(request: Request):
    """Generate report and send all data to Clay for email delivery"""
    
    # Get form data
    form_data = await request.form()
    
    hospital_name = form_data.get("hospital_name")
    hospital_beds = int(form_data.get("hospital_beds"))
    recipient_name = form_data.get("recipient_name")
    recipient_email = form_data.get("recipient_email")
    state = form_data.get("state")
    original_subject = form_data.get("original_subject", f"{hospital_name} RCM Staffing Analysis")
    
    # Generate report
    generator = DataEnhancedRCMReportGenerator()
    filename = generator.generate_report(
        hospital_name=hospital_name,
        hospital_beds=hospital_beds,
        recipient_name=recipient_name,
        recipient_email=recipient_email,
        state=state
    )
    
    # Get metrics from the generator
    metrics = generator.calculate_metrics(hospital_beds, hospital_name)
    
    # Create download URL
    report_url = f"https://web-production-8b50.up.railway.app/reports/{filename}"
    
    # Format currency for email
    def format_currency(amount):
        return f"{int(amount):,}"
    
    # Generate email HTML (using Template 1 - Immediate Response)
    first_name = recipient_name.split(' ')[0]
    email_html = f"""
    <p>Hi {first_name},</p>
    
    <p>Wow, that was fast! I just finished analyzing {hospital_name}'s specific situation.</p>
    
    <p>The report shows you're likely spending <strong>${format_currency(metrics['current_turnover_cost'])}</strong> annually on RCM turnover costs alone.</p>
    
    <p>But here's the good news: By implementing the strategies in your report, {hospital_name} could save <strong>${format_currency(metrics['potential_savings'])}</strong> every year.</p>
    
    <p><a href="{report_url}" style="background-color: #1e3a8a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; font-weight: bold;">DOWNLOAD YOUR PERSONALIZED REPORT</a></p>
    
    <p>The report includes:<br>
    ✓ Your specific turnover cost analysis<br>
    ✓ ROI timeline showing {metrics['break_even_months']}-month payback<br>
    ✓ Implementation roadmap for your {hospital_beds}-bed facility<br>
    ✓ {state} market salary data</p>
    
    <p>Quick question - are you free for a 15-minute call tomorrow to discuss the fastest path to these savings?</p>
    
    <p>Best,<br>
    Mike Patterson<br>
    VP Healthcare Solutions<br>
    Frost-Arnett Company<br>
    📱 312-555-0100 (mobile)</p>
    """
    
    # Prepare Clay payload
    clay_payload = {
        "hospital_name": hospital_name,
        "hospital_beds": hospital_beds,
        "recipient_name": recipient_name,
        "recipient_email": recipient_email,
        "state": state,
        "original_subject": original_subject,
        "report_url": report_url,
        "potential_savings": metrics['potential_savings'],
        "current_turnover_cost": metrics['current_turnover_cost'],
        "break_even_months": metrics['break_even_months'],
        "savings_per_bed": metrics['savings_per_bed'],
        "report_generated_at": datetime.now().isoformat(),
        "email_html": email_html,
        "email_subject": f"Re: {original_subject} - Your RCM Benchmark Report is Ready",
        "estimated_rcm_staff": metrics['estimated_rcm_staff'],
        "staff_turning_over_now": metrics['staff_turning_over_now'],
        "cost_per_bed": metrics['cost_per_bed']
    }
    
    # Send to Clay webhook
    import requests
    clay_webhook_url = "https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-7c4d6c32-6127-42df-958a-bf6c54f13b71"
    
    try:
        response = requests.post(clay_webhook_url, json=clay_payload, timeout=10)
        clay_status = "success" if response.status_code == 200 else f"error: {response.status_code}"
    except Exception as e:
        clay_status = f"error: {str(e)}"
    
    return {
        "status": "success",
        "report_generated": filename,
        "report_url": report_url,
        "clay_webhook_status": clay_status,
        "metrics": metrics
    }

# Original webhook endpoint (keeping for compatibility)
@app.post("/webhook/staffing-reply")
async def handle_staffing_reply(
    hospital_name: str = Form(...),
    hospital_beds: int = Form(...),
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    state: str = Form(...),
    original_subject: str = Form(...)
):
    """Handle STAFFING replies from N8N webhook"""
    try:
        # Generate report
        generator = DataEnhancedRCMReportGenerator()
        filename = generator.generate_report(
            hospital_name=hospital_name,
            hospital_beds=hospital_beds,
            recipient_name=recipient_name,
            recipient_email=recipient_email,
            state=state
        )
        
        return {
            "status": "success",
            "message": "Report generated and ready for delivery",
            "filename": filename,
            "recipient": recipient_email
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Serve generated PDF reports
@app.get("/reports/{filename}")
async def download_report(filename: str):
    """Serve generated PDF reports"""
    # Security check - only allow PDF files
    if not filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Check if file exists
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        filename,
        media_type='application/pdf',
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Check available data sources
@app.get("/api/data-sources")
async def get_data_sources():
    """Show what data sources are integrated"""
    return {
        "integrated_sources": {
            "cms": {
                "name": "CMS Hospital Compare",
                "data": ["hospital_info", "quality_ratings", "general_information"],
                "status": "active"
            },
            "bls": {
                "name": "Bureau of Labor Statistics",
                "data": ["healthcare_wages", "regional_adjustments", "occupation_data"],
                "status": "active"
            },
            "benchmarks": {
                "name": "Industry Benchmarks",
                "sources": ["MGMA", "HFMA", "ACHE"],
                "data": ["turnover_rates", "denial_benchmarks", "staffing_ratios"],
                "status": "active"
            },
            "regional": {
                "name": "Regional Cost Factors",
                "data": ["cost_of_living", "wage_adjustments"],
                "status": "active"
            }
        }
    }