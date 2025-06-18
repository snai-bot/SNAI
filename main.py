from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("schemes.json", "r", encoding="utf-8") as f:
    all_schemes = json.load(f)

@app.post("/check-eligibility")
async def check_eligibility(user: dict):
    matched = []
    for scheme in all_schemes:
        try:
            eligible = True
            if scheme.get("Income Limit (आय सीमा)"):
                income_limit = int("".join(filter(str.isdigit, scheme["Income Limit (आय सीमा)"])))
                if user["income"] > income_limit:
                    eligible = False
            if scheme.get("Farmer-specific (किसान-विशेष)") == "Yes" and not user["is_farmer"]:
                eligible = False
            if scheme.get("Specific Category (विशिष्ट श्रेणी)"):
                if user["caste"].lower() not in scheme["Specific Category (विशिष्ट श्रेणी)"].lower():
                    eligible = False
            if scheme.get("Asset Disqualification (संपत्ति अयोग्यता)") == "No car" and user["asset_car"]:
                eligible = False
            if eligible:
                matched.append({
                    "scheme": scheme["Scheme Name (योजना का नाम)"],
                    "documents": scheme["Documents (दस्तावेज़)"],
                    "link": scheme["Official Link"]
                })
        except:
            continue
    return {"matched_schemes": matched}