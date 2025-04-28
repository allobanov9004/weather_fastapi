from fastapi import FastAPI
import httpx
from pydantic import BaseModel
import uvicorn
from config import API_KEY

app = FastAPI()


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str


api_key = API_KEY
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "ru"}
        response = await client.get(BASE_URL, params=params)
        
        if response.status_code != 200:
            return {"error": "Город не найден или ошибка API"}
        
        data = response.json()
        return WeatherResponse(
            city=city,
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"]
        )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)