from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message":"palm mind backend"}

@app.get("/health")
def health():
    return {"status":"healthy"}