from flask import Flask, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

async def fetch(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def get_response(urls, data):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, url, data)) for url in urls]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            return await task

@app.route('/', methods=['POST'])
async def forward_request():
    data = request.json
    print(data)
    urls = [
        'http://localhost:3001/',
        # 'http://localhost:3005/',
        'http://localhost:3006/',
    ]
    response = await get_response(urls, data)
    return jsonify({'response': response})

if __name__ == "__main__":
    # app.run(host="localhost",port=5010, debug=True )
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:5010"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
