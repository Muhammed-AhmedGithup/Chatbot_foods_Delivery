def remove_order(id_session):
    if id_session not in total_order_over_ssio:
        return JSONResponse({
            'fulfillmentText':'sorry can not remove order you can firsr write '"new order"' '
        })
    else:
        dic=total_order_over_ssio[id_sission]