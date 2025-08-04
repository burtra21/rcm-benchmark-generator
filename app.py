# app.py
# Web interface for enhanced RCM benchmark report generator with real data integration

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os
from generate_report_enhanced_v2 import DataEnhancedRCMReportGenerator

# Create the web application
app = FastAPI()

# Create enhanced HTML form with state selection
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

# Handle form submission - now using Enhanced generator with real data
@app.post("/generate")
async def generate_report(
    hospital_name: str = Form(...),
    hospital_beds: int = Form(...),
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    state: str = Form(...)  # Added state parameter
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
            state=state  # Pass state to generator
        )
        
        # Return the file for download
        return FileResponse(
            filename,
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Enhanced RCM Benchmark Report Generator", 
        "version": "3.0",
        "features": ["real_data", "charts", "roi_analysis"]
    }

# Add a simple API endpoint for N8N integration
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

# Webhook endpoint for N8N integration
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
        
        # In production, you'd email this report
        # For now, just return success
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

# Endpoint to check available data sources
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