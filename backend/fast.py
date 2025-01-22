from typing import Union
from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import helpSql
import exctract
app = FastAPI()


    


@app.post("/")
async def read_root(request:Request):
    data=await request.json()
    queryResult=data['queryResult']
    intent=data['queryResult']['intent']['displayName']
    parameters=data['queryResult']['parameters']
    name_context=queryResult['outputContexts'][0]['name']
    id_sission=exctract.extrack_session_id(name_context)
    intent_handler={
        'track-order-context':track_order,
        'order.add':add_order,
        'order.complete':compelete_order,
        'order.remove':remove_order
    }
    if intent=='order.add':
        return intent_handler[intent](queryResult)
    elif intent=='order.complete':
        return intent_handler[intent](id_sission)
    elif intent=='order.remove':
        return intent_handler[intent](parameters,id_sission)
    
    return intent_handler[intent](parameters)
    


total_order_over_ssio={}


def track_order(parameters:dict):
    order_id=int(parameters['number'])
    result=helpSql.order_track_satus(order_id)
    if result is None:
        return JSONResponse({
            'fulfillmentText':'sorry the id of order is not found'
        })
    return JSONResponse(content={
        'fulfillmentText':f'the order {result[0]} is {result[1]}'
    })
    
    
    
def compelete_order(id_session):
    if id_session not in total_order_over_ssio:
        return JSONResponse({
            'fulfillmentText':'I didn''t understand. You can say ''New Order'' or ''Track Order'' to ordrer. Also, in a new order, please mention only items from our available menu: Pav Bhaji, Chole Bhature, Pizza, Mango Lassi, Masala Dosa, Biryani, Vada Pav, Rava Dosa, and Samosa. Also specify a quantity for each item for example: '"One pizza and 2 chole bhature'"
        })
    else:
       order_id,sum_of_price= helpSql.save_order(total_order_over_ssio[id_session])
       return JSONResponse({
           'fulfillmentText':f'Awesome , your order is placed Here is your order id #{order_id} and Tota price {sum_of_price} Anything else?'
       })
    
        
    
    
     
def add_order(queryResult:dict):
    numbers=queryResult['parameters']['number']
    foods=queryResult['parameters']['food']
    name_context=queryResult['outputContexts'][0]['name']
    fulfillmentText='Don''t understand, try again please.'
    if len(numbers)!=len(foods):
        return JSONResponse({
            'fulfillmentText':fulfillmentText
        })
        
    id_sission=exctract.extrack_session_id(name_context)
    carrunt_order_s=dict(zip(foods,numbers))
    if id_sission in total_order_over_ssio:
        carrunt=total_order_over_ssio[id_sission]
        carrunt.update(carrunt_order_s)
        total_order_over_ssio[id_sission]=carrunt
    else:
        total_order_over_ssio[id_sission]=carrunt_order_s
    
    fulfillmentText=f'the {exctract.dict_to_string(total_order_over_ssio[id_sission])} is recieved Anything else?'
    
    return JSONResponse({
        'fulfillmentText':fulfillmentText
    })
    
    
    
def remove_order(parameters,id_session):
    list_remove=parameters['food']
    if id_session not in total_order_over_ssio:
        return JSONResponse({
            'fulfillmentText':'sorry can not remove order you can firsr write '"new order"' '
        })
    else:
        dic=total_order_over_ssio[id_session]
        
        for item in list_remove:
            if item in dic:
                dic.pop(item)
        str_removed=exctract.list_to_str(list_remove)
        return JSONResponse({
            'fulfillmentText':f'I remove {str_removed} from your order Anything else?'
        })
            
        
        
        
    
    
