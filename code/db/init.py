import sqlite3

con = sqlite3.connect("code/db/noten.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Module(
    ModulID TEXT PRIMARY KEY NOT NULL,
    Modulname TEXT NOT NULL,
    ECTS INTEGER NOT NULL,
    Professor TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Pruefung(
    PruefungID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    PruefungsDatum TEXT NOT NULL,
    Noteneingabedatum TEXT NOT NULL,
    ModulID TEXT NOT NULL REFERENCES Module(ModulID) ON DELETE CASCADE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Noten(
    NotenID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Note REAL NOT NULL,
    Bestanden TEXT NOT NULL CHECK (Bestanden IN ('true', 'false')),
    isUser TEXT NOT NULL CHECK (isUser IN ('true', 'false')),
    PruefungID INTEGER NOT NULL REFERENCES Pruefung(PruefungID) ON DELETE CASCADE
)
""")

con.commit()
con.close()
