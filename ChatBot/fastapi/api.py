from fastapi import FastAPI
#import logging

app = FastAPI()

@app.get("/home")
async def root():
    #logging.info("Hello World!")
    return {"message" : "BoB13기 문경태입니다"}