from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from database import Session, engine
from db_home.models import User, Order
from schemas import OrderModel
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']

)

session = Session(bind=engine)


@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    return {'message': 'Hello World'}


@order_router.post('/create', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity)

    new_order.user = user
    session.add(new_order)
    session.commit()
    response = {
        'id': new_order.id,
        'pizza_size': new_order.pizza_size,
        'quantity': new_order.quantity,
        'order_status': new_order.order_status
    }
    return jsonable_encoder(response)


@order_router.get('/get_list')
async def get_list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You are not a superuser')


@order_router.get('/get_info/{id}')
async def get_info(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='User not allowed to carry out request')


@order_router.get('/get_user_orders')
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('/get_info/{id}')
async def get_specific_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    orders = current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='No order with such id')


@order_router.put('/update/{id}')
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    data = session.query(Order).filter(Order.id == id).first()

    data.quantity = order.quantity
    data.pizza_size = order.pizza_size

    session.commit()

    return jsonable_encoder(data)


@order_router.put('/delete/{id}')
async def delete_order(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    data = session.query(Order).filter(Order.id == id).first()

    session.delete(data)
    session.commit()

    return data


