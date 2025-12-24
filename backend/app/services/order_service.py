"""
주문 서비스

결제 완료 후 카페24에 주문을 생성합니다.
"""
from typing import Optional
from app.daos.cafe24_dao import cafe24_dao
from app.services.cart_service import cart_service
from app.services.payment_service import payment_service
from app.models.order import Order, OrderItem, CreateOrderRequest, ShippingAddress
from app.models.product import ProductPrice
from app.commons.utils import generate_uuid, get_timestamp
from app.commons.exceptions import CartNotFoundException, OrderNotFoundException


class OrderService:
    """주문 관련 비즈니스 로직"""

    def __init__(self):
        self.cafe24 = cafe24_dao
        # 메모리 기반 주문 저장소 (실제로는 DB 사용 권장)
        self._orders: dict[str, Order] = {}

    def _transform_to_cafe24_order(self, order: Order) -> dict:
        """
        내부 주문 데이터를 카페24 형식으로 변환

        카페24 주문 생성 API 형식에 맞게 변환합니다.
        """
        items = []
        for item in order.items:
            items.append({
                "product_no": int(item.product_id),
                "quantity": item.quantity,
                "product_price": int(item.price.amount),
            })

        return {
            "order": {
                "order_id": order.id,
                "payment_method": "etc",  # 외부 결제
                "paid": "T",  # 결제 완료 상태
                "items": items,
                "receiver_name": order.shipping_address.name if order.shipping_address else "",
                "receiver_phone": order.shipping_address.phone if order.shipping_address else "",
                "receiver_zipcode": order.shipping_address.zip_code if order.shipping_address else "",
                "receiver_address1": order.shipping_address.address1 if order.shipping_address else "",
                "receiver_address2": order.shipping_address.address2 if order.shipping_address else "",
            }
        }

    async def create_order(self, request: CreateOrderRequest, payment_key: str) -> Order:
        """
        주문 생성

        1. 장바구니 정보로 주문 생성
        2. 카페24에 주문 등록
        """
        # 장바구니 조회
        cart = cart_service.get_cart(request.cart_id)
        if not cart or not cart.items:
            raise CartNotFoundException("장바구니가 비어있습니다.")

        # 주문 아이템 생성
        order_items = []
        for cart_item in cart.items:
            order_items.append(
                OrderItem(
                    id=generate_uuid(),
                    product_id=cart_item.product_id,
                    variant_id=cart_item.variant_id,
                    title=cart_item.title,
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                )
            )

        # 내부 주문 생성
        now = get_timestamp()
        order = Order(
            id=generate_uuid(),
            status="paid",
            items=order_items,
            shipping_address=request.shipping_address,
            total_price=cart.total_price,
            payment_id=payment_key,
            created_at=now,
            updated_at=now,
        )

        # 카페24에 주문 생성
        try:
            cafe24_order_data = self._transform_to_cafe24_order(order)
            cafe24_response = await self.cafe24.create_order(cafe24_order_data)
            order.cafe24_order_id = cafe24_response.get("order", {}).get("order_id")
        except Exception as e:
            # 카페24 주문 생성 실패해도 내부 주문은 저장
            print(f"카페24 주문 생성 실패: {e}")

        # 내부 저장
        self._orders[order.id] = order

        # 장바구니 비우기
        cart_service.clear_cart(request.cart_id)

        return order

    def get_order(self, order_id: str) -> Order:
        """주문 조회"""
        order = self._orders.get(order_id)
        if not order:
            raise OrderNotFoundException()
        return order

    def get_orders(self, page: int = 1, limit: int = 10) -> list[Order]:
        """주문 목록 조회"""
        orders = list(self._orders.values())
        # 최신순 정렬
        orders.sort(key=lambda x: x.created_at, reverse=True)

        start = (page - 1) * limit
        end = start + limit
        return orders[start:end]

    async def sync_order_status(self, order_id: str) -> Order:
        """카페24 주문 상태 동기화"""
        order = self.get_order(order_id)

        if order.cafe24_order_id:
            try:
                cafe24_order = await self.cafe24.get_order(order.cafe24_order_id)
                # 상태 매핑 (카페24 상태 → 내부 상태)
                status_map = {
                    "N00": "pending",
                    "N10": "paid",
                    "N20": "shipped",
                    "N30": "delivered",
                    "C00": "cancelled",
                }
                cafe24_status = cafe24_order.get("order", {}).get("order_status")
                if cafe24_status in status_map:
                    order.status = status_map[cafe24_status]
                    order.updated_at = get_timestamp()
            except Exception as e:
                print(f"주문 상태 동기화 실패: {e}")

        return order


# 싱글톤 인스턴스
order_service = OrderService()
