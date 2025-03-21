import json
from datetime import datetime
from producer import KafkaProducer
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
kafka_producer = KafkaProducer()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# routes
@app.get("/")
async def read_root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

@app.get("/enter_data", response_class=HTMLResponse)
def get_data(request: Request):
    try:
        return templates.TemplateResponse("form.html", {"request": request})
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

@app.post("/submit")
def submit_form(
    request: Request,
    transaction_id: int = Form(...),
    user_id: int = Form(...),
    transaction_amount: float = Form(...),
    merchant_id: int = Form(...),
    previous_transactions: int = Form(...),
    failed_transactions: int = Form(...),
    account_age_days: int = Form(...),
    user_credit_score: int = Form(...),
    is_foreign_transaction: int = Form(...),
    is_high_risk_country: int = Form(...),
    is_vpn_used: int = Form(...),
    user_income: float = Form(...),
    is_account_compromised: int = Form(...),
    transaction_location: str = Form(...),
    device_type: str = Form(...),
    merchant_category: str = Form(...),
    transaction_channel: str = Form(...),
    user_location: str = Form(...)
):
    try:
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "transaction_amount": transaction_amount,
            "merchant_id": merchant_id,
            "previous_transactions": previous_transactions,
            "failed_transactions": failed_transactions,
            "account_age_days": account_age_days,
            "user_credit_score": user_credit_score,
            "is_foreign_transaction": is_foreign_transaction,
            "is_high_risk_country": is_high_risk_country,
            "is_vpn_used": is_vpn_used,
            "user_income": user_income,
            "is_account_compromised": is_account_compromised,
            "transaction_location": transaction_location,
            "device_type": device_type,
            "merchant_category": merchant_category,
            "transaction_channel": transaction_channel,
            "user_location": user_location,
            "transaction_time": transaction_time,
        }
        print(data)

        # Producing Kafka message
        try:
            kafka_producer.produce(**data)
        except Exception as kafka_error:
            return HTMLResponse(content=f"Kafka Error: {str(kafka_error)}", status_code=500)

        pretty_json = json.dumps(data, indent=4)
        return templates.TemplateResponse("result.html", {"request": request, "data": pretty_json})

    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
