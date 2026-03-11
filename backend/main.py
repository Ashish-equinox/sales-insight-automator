from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from backend.services.ai import generate_summary
from backend.services.emailer import send_email

app = FastAPI(title="Sales Insight Automator")

# allow frontend (React) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/analyze")
async def analyze_sales(file: UploadFile = File(...), email: str = Form(...)):

    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX allowed")

    # read uploaded file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    else:
        df = pd.read_excel(file.file)

    # compute insights
    total_revenue = df["Revenue"].sum()
    best_region = df.groupby("Region")["Revenue"].sum().idxmax()
    best_category = df.groupby("Product_Category")["Revenue"].sum().idxmax()

    structured_data = f"""
Total Revenue: {total_revenue}
Best Region: {best_region}
Best Category: {best_category}
"""

    # generate AI summary
    summary = generate_summary(structured_data)

    # send email
    send_email(email, summary)

    return {
        "status": "success",
        "message": "Summary generated and email sent"
    }