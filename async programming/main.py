async def fetch_user(user_id:int):
    result=await database.get_user(user_id)
    return result
# here we have used await that will instruct the event loop that this task will take time so till it is waiting to be completed do some other work.
# the os instructs when the task is done and then the pause is resumed.



import time 

@app.get("/bad-example")
async def bad_example():
    time.sleep(5)
    return {"message":"done"}

# here we have declared the function as async but didnt use the await making the time.sleep() function force the async function to be an synchronus . 
# once this function is ran no other request can be processed by the worker for 5 sec.


import asyncio

@app.get("/bad-example")
async def bad_example():
    await asyncio.sleep(5)
    return {"message":"done"}

# this is the correct way for the above example 


# Async gather 

import asyncio

async def fetch_a():
    await asyncio.sleep(2)
    return "a"

async def fetch_b():
    await asyncio.sleep(2)
    return "b"

async def main():
    result_a, result_b= await asyncio.gather(fetch_a(),fetch_b())
    return result_a,result_b


