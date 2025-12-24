"""
장바구니 서비스

세션 기반 장바구니를 관리합니다.
(카페24에 장바구니가 없으므로 자체 관리)
"""
from typing import Optional
from app.models.cart import Cart, CartItem, AddToCartRequest
from app.models.product import ProductPrice, ProductImage
from app.services.product_service import product_service
from app.commons.utils import generate_uuid
from app.commons.exceptions import CartNotFoundException, ProductNotFoundException


class CartService:
    """장바구니 관련 비즈니스 로직"""

    def __init__(self):
        # 메모리 기반 장바구니 저장소 (실제로는 Redis 등 사용 권장)
        self._carts: dict[str, Cart] = {}

    def _calculate_totals(self, cart: Cart) -> Cart:
        """장바구니 총계 계산"""
        total_quantity = sum(item.quantity for item in cart.items)
        total_amount = sum(
            int(item.price.amount) * item.quantity for item in cart.items
        )

        cart.total_quantity = total_quantity
        cart.total_price = ProductPrice(
            amount=str(total_amount),
            currency_code="KRW",
        )
        return cart

    def create_cart(self) -> Cart:
        """새 장바구니 생성"""
        cart_id = generate_uuid()
        cart = Cart(id=cart_id)
        self._carts[cart_id] = cart
        return cart

    def get_cart(self, cart_id: str) -> Optional[Cart]:
        """장바구니 조회"""
        return self._carts.get(cart_id)

    def get_or_create_cart(self, cart_id: Optional[str] = None) -> Cart:
        """장바구니 조회 또는 생성"""
        if cart_id and cart_id in self._carts:
            return self._carts[cart_id]
        return self.create_cart()

    async def add_item(self, cart_id: str, request: AddToCartRequest) -> Cart:
        """장바구니에 상품 추가"""
        cart = self.get_cart(cart_id)
        if not cart:
            raise CartNotFoundException()

        # 상품 정보 조회
        try:
            product = await product_service.get_product(request.product_id)
        except Exception:
            raise ProductNotFoundException()

        # 이미 담긴 상품인지 확인
        existing_item = None
        for item in cart.items:
            if item.product_id == request.product_id and item.variant_id == request.variant_id:
                existing_item = item
                break

        if existing_item:
            # 수량 증가
            existing_item.quantity += request.quantity
        else:
            # 새 아이템 추가
            new_item = CartItem(
                id=generate_uuid(),
                product_id=request.product_id,
                variant_id=request.variant_id,
                title=product.title,
                quantity=request.quantity,
                price=product.price,
                image=product.featured_image,
            )
            cart.items.append(new_item)

        # 총계 재계산
        self._calculate_totals(cart)
        return cart

    def update_item(self, cart_id: str, item_id: str, quantity: int) -> Cart:
        """장바구니 아이템 수량 변경"""
        cart = self.get_cart(cart_id)
        if not cart:
            raise CartNotFoundException()

        for item in cart.items:
            if item.id == item_id:
                if quantity <= 0:
                    cart.items.remove(item)
                else:
                    item.quantity = quantity
                break

        self._calculate_totals(cart)
        return cart

    def remove_item(self, cart_id: str, item_id: str) -> Cart:
        """장바구니에서 상품 삭제"""
        cart = self.get_cart(cart_id)
        if not cart:
            raise CartNotFoundException()

        cart.items = [item for item in cart.items if item.id != item_id]
        self._calculate_totals(cart)
        return cart

    def clear_cart(self, cart_id: str) -> Cart:
        """장바구니 비우기"""
        cart = self.get_cart(cart_id)
        if not cart:
            raise CartNotFoundException()

        cart.items = []
        self._calculate_totals(cart)
        return cart


# 싱글톤 인스턴스
cart_service = CartService()
