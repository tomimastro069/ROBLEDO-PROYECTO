from typing import Optional, List
from sqlmodel import Session, select
from .models import Order, OrderItem

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, order: Order, items: List[OrderItem]):
        self.session.add(order)
        self.session.flush()
        for item in items:
            item.order_id = order.id
            self.session.add(item)
        self.session.commit()
        order.items = items
        return order

    def get(self, order_id: int) -> Optional[Order]:
        statement = select(Order).where(Order.id == order_id)
        result = self.session.exec(statement).one_or_none()
        if result:
            result.items = self.get_items(result.id)
        return result

    def list_by_user(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Order]:
        statement = select(Order).where(Order.user_id == user_id).offset(skip).limit(limit)
        results = self.session.exec(statement).all()
        for result in results:
            result.items = self.get_items(result.id)
        return results
    
    def list_all(self, skip: int = 0, limit: int = 20) -> List[Order]:
        statement = select(Order).offset(skip).limit(limit)
        results = self.session.exec(statement).all()
        for result in results:
            result.items = self.get_items(result.id)
        return results

    def update(self, order: Order, **kwargs):
        for key, value in kwargs.items():
            setattr(order, key, value)
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def delete(self, order: Order):
        self.session.delete(order)
        self.session.commit()

    def add_items(self, order: Order, items: List[OrderItem]):
        for item in items:
            item.order_id = order.id
            self.session.add(item)
        self.session.commit()
        self.session.refresh(order)
        return order

    def get_items(self, order_id: int) -> List[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        results = self.session.exec(statement).all()
        return results
