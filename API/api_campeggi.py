from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import sqlite3

# Connessione con il db
conn = sqlite3.connect('../db_turismo_test.db')


app = FastAPI()

# Creazione del modello CampeggioCreate
class CampeggioCreate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# Creazione del modello CampeggioUpdate
class CampeggioUpdate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# API Post - Crea un nuovo campeggio
@app.post("/crea_campeggi/")
async def crea_campeggio(campeggio: CampeggioCreate):
    query = "INSERT INTO Campeggi (Regione, Anno, Arrivi, Presenze) VALUES (?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (campeggio.Regione, campeggio.Anno, campeggio.Arrivi, campeggio.Presenze))
    conn.commit()
    return {"message": "Campeggio creato con successo"}


# API Put - Aggiorna un campeggio esistente
@app.put("/aggiorna_campeggi/")
async def aggiorna_campeggio(campeggio: CampeggioUpdate):
    query = "UPDATE Campeggi SET Anno = ?, Arrivi = ?, Presenze = ? WHERE Regione = ?"
    cursor = conn.cursor()
    cursor.execute(query, (campeggio.Anno, campeggio.Arrivi, campeggio.Presenze, campeggio.Regione))
    conn.commit()
    return {"message": f"Dati dei Campeggi e Villaggi con Regione {campeggio.Regione} aggiornati con successo"}


# API Get - Ottiene le informazioni relative agli 'Arrivi' dei Campeggi
@app.get("/arrivi_campeggi/")
async def get_items():
    cursor = conn.cursor()
    cursor.execute("SELECT arrivi FROM Campeggi")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Arrivi Campeggi e Villaggi": result}


# API Get - Ottiene informazioni relative agli 'Arrivi' dei campeggi in base alle regioni
@app.get("/arrivi_campeggi_per_regione/{regione}")
async def get_arrivi_per_regione(regione: str):
    cursor = conn.cursor()
    query = "SELECT Regione, Anno, Arrivi FROM Campeggi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# Api Get - Ottiene informazioni relative agli Arrivi dei Campeggi in base all'anno
@app.get("/arrivi_campeggi_per_anno/{anno}")
async def get_arrivi_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Arrivi FROM Campeggi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Get - Ottiene informazioni relative alle Presenze dei Campeggi
@app.get("/presenze_alberghi/")
async def get_presenze_alberghi():
    cursor = conn.cursor()
    cursor.execute("SELECT presenze FROM Campeggi")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Presenze": result}


# API Get - Ottiene informazioni relative alle Presenze dei Campeggi in base alle Regioni
@app.get("/presenze_campeggi_per_regione/{regione}")
async def get_presenze_per_regione(regione: str):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Campeggi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# API Get - Ottiene informazioni relative alle Presenze dei Campeggi in base all'Anno
@app.get("/presenze_campeggi_per_anno/{anno}")
async def get_presenze_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Campeggi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Delete - Eliminazione di un campeggio (inserendo la regione e l'anno)
@app.delete("/elimina_campeggi/{regione}/{anno}")
async def elimina_alberghi(regione: str, anno: int):
    query = "DELETE FROM Campeggi WHERE Regione = ? AND Anno = ?"
    cursor = conn.cursor()
    cursor.execute(query, (regione, anno))
    conn.commit()
    return {"message": f"Dati dei Campeggi con Regione {regione} e Anno {anno} eliminati con successo"}