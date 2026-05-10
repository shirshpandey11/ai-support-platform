from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

import models
import database
import ai_pipeline

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="AI Customer Support Insights")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home route
@app.get("/")
def home():
    return {
        "message": "Backend running successfully"
    }


# Upload tickets API
@app.post("/upload/")
async def upload_tickets(file: UploadFile):

    # Read uploaded CSV
    df = pd.read_csv(file.file)

    db = database.SessionLocal()

    for _, row in df.iterrows():

        message = str(row.get("message", ""))

        # AI sentiment analysis
        sentiment = ai_pipeline.classify_sentiment(message)

        # AI category detection
        category = ai_pipeline.detect_category(message)

        # AI suggested response
        reply = ai_pipeline.suggest_reply(message)

        # Create DB object
        ticket = models.Ticket(
            customer_id=str(row.get("customer_id", "")),
            message=message,
            product=str(row.get("product", "")),
            sentiment=sentiment,
            category=category,
            suggested_reply=reply,
            order_value=float(row.get("order_value", 0))
        )

        db.add(ticket)

    db.commit()
    db.close()

    return {
        "status": "uploaded successfully",
        "rows_processed": len(df)
    }


# Insights API
@app.get("/insights/")
def get_insights():

    tickets = pd.read_sql_table(
        "tickets",
        con=database.engine
    )

    if tickets.empty:
        return {
            "top_issues": {},
            "sentiment_trend": {},
            "avg_order_value": 0,
            "ticket_count": 0,
            "recent_tickets": []
        }

    top_issues = (
        tickets["category"]
        .fillna("Unknown")
        .value_counts()
        .head(5)
        .to_dict()
    )

    sentiment_trend = (
        tickets["sentiment"]
        .fillna("Unknown")
        .value_counts()
        .to_dict()
    )

    avg_order_value = float(
        tickets["order_value"]
        .fillna(0)
        .mean()
    )

    recent_tickets = tickets[[
        "message",
        "category",
        "sentiment",
        "suggested_reply"
    ]].tail(5).to_dict(orient="records")

    return {
        "top_issues": top_issues,
        "sentiment_trend": sentiment_trend,
        "avg_order_value": avg_order_value,
        "ticket_count": len(tickets),
        "recent_tickets": recent_tickets
    }

@app.delete("/reset/")
def reset_database():

    db = database.SessionLocal()

    db.query(models.Ticket).delete()

    db.commit()

    db.close()

    return {"message": "Database reset successful"}