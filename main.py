from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI(title="Car Data Web Service")

def get_db_connection():
    conn = sqlite3.connect("carsweb.db")
    conn.row_factory = sqlite3.Row
    return conn

class CarBase(BaseModel):
    merk: str
    model: str
    tahun: int
    harga: float

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

@app.post("/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cars (merk, model, tahun, harga) VALUES (?, ?, ?, ?)",
            (car.merk, car.model, car.tahun, car.harga)
        )
        conn.commit()
        return {**car.model_dump(), "id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/cars", response_model=List[CarResponse])
def get_all_cars():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/cars/{car_id}", response_model=CarResponse)
def get_car_by_id(car_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Mobil tidak ditemukan")
    return dict(row)

@app.put("/cars/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car_update: CarCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cars WHERE id = ?", (car_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Mobil tidak ditemukan")
    try:
        cursor.execute(
            "UPDATE cars SET merk = ?, model = ?, tahun = ?, harga = ? WHERE id = ?",
            (car_update.merk, car_update.model, car_update.tahun, car_update.harga, car_id)
        )
        conn.commit()
        return {**car_update.model_dump(), "id": car_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cars WHERE id = ?", (car_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Mobil tidak ditemukan")
    try:
        cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
        return None
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
