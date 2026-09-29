from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    phone: Mapped[str] = mapped_column(String(40), default="")
    email: Mapped[str] = mapped_column(String(160), default="")
    address: Mapped[str] = mapped_column(Text, default="")
    customer_type: Mapped[str] = mapped_column(String(40), default="Lainnya")
    notes: Mapped[str] = mapped_column(Text, default="")
    survey_description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    quotations: Mapped[list["Quotation"]] = relationship(back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    type: Mapped[str] = mapped_column(String(20), default="product")
    category: Mapped[str] = mapped_column(String(80), default="Umum")
    unit: Mapped[str] = mapped_column(String(20), default="pcs")
    cost_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    stock: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    supplier: Mapped[str] = mapped_column(String(160), default="")
    is_active: Mapped[bool] = mapped_column(default=True)

class Quotation(Base):
    __tablename__ = "quotations"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(40), unique=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String(30), default="Draft")
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    tax: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    customer: Mapped[Customer] = relationship(back_populates="quotations")
    items: Mapped[list["QuotationItem"]] = relationship(back_populates="quotation", cascade="all, delete-orphan")

class QuotationItem(Base):
    __tablename__ = "quotation_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    quotation_id: Mapped[int] = mapped_column(ForeignKey("quotations.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=1)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    quotation: Mapped[Quotation] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    quotation_id: Mapped[int] = mapped_column(ForeignKey("quotations.id"), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    location: Mapped[str] = mapped_column(String(240), default="")
    status: Mapped[str] = mapped_column(String(30), default="Planning")
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    notes: Mapped[str] = mapped_column(Text, default="")

class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    invoice_number: Mapped[str] = mapped_column(String(40), unique=True)
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="Issued")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    payment_date: Mapped[date] = mapped_column(Date, default=date.today)
    payment_method: Mapped[str] = mapped_column(String(30), default="Transfer")

class Expense(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    category: Mapped[str] = mapped_column(String(80))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    expense_date: Mapped[date] = mapped_column(Date, default=date.today)
    description: Mapped[str] = mapped_column(String(240), default="")
