from fastapi import FastAPI, Response, Body

app = FastAPI()


@app.get("/")
async def root():
    
    return {"message": "Hello World"}



@app.get("/xml", response_class=Response)
def get_xml():
    xml_content = """
    <note>
        <to>User</to>
        <from>FastAPI</from>
        <heading>Reminder</heading>
        <body>This is an XML response!</body>
    </note>
    """
    return Response(content=xml_content, media_type="application/xml")

@app.post("/post")
async def post_data(data: bytes = Body(...)):
    xml_content = data.decode("utf-8")
    print("Received XML:")
    print(xml_content)
    return {"message": "XML data received"}



