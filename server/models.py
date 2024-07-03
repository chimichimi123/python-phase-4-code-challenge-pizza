from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = relationship("RestaurantPizza", back_populates="restaurant", cascade="all, delete-orphan")
    pizzas = relationship("Pizza", secondary="restaurant_pizzas", back_populates="restaurants", overlaps="restaurant_pizzas")

    serialize_rules = ('-pizzas.restaurant_pizzas',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    restaurant_pizzas = relationship("RestaurantPizza", back_populates="pizza", cascade="all, delete-orphan")
    restaurants = relationship("Restaurant", secondary="restaurant_pizzas", back_populates="pizzas", overlaps="restaurant_pizzas")

    serialize_rules = ('-restaurants.restaurant_pizzas',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    pizza_id = db.Column(db.Integer, ForeignKey("pizzas.id", ondelete="CASCADE"), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    restaurant = relationship("Restaurant", back_populates="restaurant_pizzas", overlaps="pizzas")
    pizza = relationship("Pizza", back_populates="restaurant_pizzas", overlaps="restaurants,restaurant_pizzas")

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30.")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"