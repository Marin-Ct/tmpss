"""The 'before' version: one class that breaks S, O and D at once.
Kept only for comparison, it is not used by the final project."""
import json


class OrderProcessor:
    def process(self, order, kind):
        total = sum(i.price * i.quantity for i in order.items)

        if kind == "regular":          # new discount -> edit this method (OCP)
            final = total
        elif kind == "promo":
            final = total * 0.8
        elif kind == "bulk":
            final = total * 0.9
        else:
            raise ValueError(kind)

        with open("orders.json", "w") as f:   # storage hard-wired (DIP)
            json.dump({"id": order.order_id, "price": final}, f)

        print(f"mail to {order.customer}: {final}")  # notification hard-wired (DIP)
        return final                           # pricing + storage + mail (SRP)
