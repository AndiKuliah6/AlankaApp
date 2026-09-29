import hashlib
import hmac
import os
from datetime import date
from decimal import Decimal
from pathlib import Path
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from starlette.middleware.sessions import SessionMiddleware
from .database import Base, engine, get_db
from .models import Customer, Expense, Invoice, Payment, Product, Project, Quotation, QuotationItem
from .services.calculation_service import calculate_catalog_selling_price, calculate_item, calculate_quotation
from .services.pdf_service import quotation_pdf

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Alanka Management System")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "local-development-secret"))
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_authenticated(request: Request) -> bool:
    return bool(request.session.get("user"))


def render(request: Request, template: str, **context):
    context["request"] = request
    context["current_user"] = request.session.get("user")
    return templates.TemplateResponse(template, context)


def money(value):
    return f"Rp {Decimal(str(value or 0)):,.0f}".replace(",", ".")

templates.env.filters["money"] = money

templates.env.globals["today"] = date.today

@app.on_event("startup")
def startup():
    if os.getenv("AUTO_CREATE_SCHEMA", "true").lower() == "true":
        Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        if not db.scalar(select(Customer)):
            db.add_all([
                Customer(name="PT Contoh Teknologi", phone="08123456789", email="admin@contoh.id", address="Denpasar", customer_type="Perusahaan"),
                Customer(name="Villa Alanka", phone="08129876543", address="Bali", customer_type="Villa"),
            ])
        if not db.scalar(select(Product)):
            db.add_all([
                Product(code="CCTV-H6C", name="CCTV EZVIZ H6C Pro 3MP", category="CCTV", unit="pcs", cost_price=450000, selling_price=650000, stock=10),
                Product(code="UTP-CAT6", name="Kabel UTP Cat6", category="Jaringan", unit="meter", cost_price=5500, selling_price=8500, stock=300),
                Product(code="JASA-INST", name="Jasa Instalasi CCTV", type="service", category="Jasa", unit="titik", cost_price=100000, selling_price=250000),
            ])
        db.commit()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse("/dashboard" if is_authenticated(request) else "/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return render(request, "login.html", error=None)

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    expected_user = os.getenv("ADMIN_USERNAME", "admin")
    expected_password = os.getenv("ADMIN_PASSWORD", "admin123")
    if hmac.compare_digest(username, expected_user) and hmac.compare_digest(hash_password(password), hash_password(expected_password)):
        request.session["user"] = username
        return RedirectResponse("/dashboard", status_code=303)
    return render(request, "login.html", error="Username atau password tidak sesuai")

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    quotations = db.scalars(select(Quotation)).all()
    projects = db.scalars(select(Project)).all()
    revenue = sum((Decimal(str(i.total or 0)) for i in db.scalars(select(Invoice)).all()), Decimal(0))
    expenses = sum((Decimal(str(i.amount or 0)) for i in db.scalars(select(Expense)).all()), Decimal(0))
    receivable = Decimal(0)
    for invoice in db.scalars(select(Invoice)).all():
        paid = sum((Decimal(str(p.amount or 0)) for p in db.scalars(select(Payment).where(Payment.invoice_id == invoice.id)).all()), Decimal(0))
        receivable += Decimal(str(invoice.total or 0)) - paid
    return render(request, "dashboard.html", stats={"quotations": len(quotations), "active_quotations": sum(q.status in ("Sent", "Negotiation") for q in quotations), "projects": sum(p.status != "Completed" for p in projects), "completed_projects": sum(p.status == "Completed" for p in projects), "revenue": revenue, "expenses": expenses, "profit": revenue - expenses, "receivable": receivable}, quotations=quotations[-5:], projects=projects[-5:])

@app.get("/customers", response_class=HTMLResponse)
def customers(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    return render(request, "customers.html", customers=db.scalars(select(Customer).order_by(Customer.id.desc())).all(), editing_customer=None)

@app.post("/customers")
def add_customer(request: Request, name: str = Form(...), phone: str = Form(""), email: str = Form(""), address: str = Form(""), customer_type: str = Form("Lainnya"), survey_description: str = Form(""), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    db.add(Customer(name=name, phone=phone, email=email, address=address, customer_type=customer_type, survey_description=survey_description)); db.commit()
    return RedirectResponse("/customers", status_code=303)

@app.get("/customers/{customer_id}/edit", response_class=HTMLResponse)
def edit_customer_page(request: Request, customer_id: int, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    customer = db.get(Customer, customer_id)
    if not customer: return RedirectResponse("/customers", status_code=303)
    return render(request, "customers.html", customers=db.scalars(select(Customer).order_by(Customer.id.desc())).all(), editing_customer=customer)

@app.post("/customers/{customer_id}/edit")
def update_customer(request: Request, customer_id: int, name: str = Form(...), phone: str = Form(""), email: str = Form(""), address: str = Form(""), customer_type: str = Form("Lainnya"), survey_description: str = Form(""), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    customer = db.get(Customer, customer_id)
    if customer:
        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.address = address
        customer.customer_type = customer_type
        customer.survey_description = survey_description
        db.commit()
    return RedirectResponse("/customers", status_code=303)

@app.get("/products", response_class=HTMLResponse)
def products(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    return render(request, "products.html", products=db.scalars(select(Product).order_by(Product.id.desc())).all(), editing_product=None)

@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_page(request: Request, product_id: int, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    product = db.get(Product, product_id)
    if not product: return RedirectResponse("/products", status_code=303)
    return render(request, "products.html", products=db.scalars(select(Product).order_by(Product.id.desc())).all(), editing_product=product)

@app.post("/products")
def add_product(request: Request, code: str = Form(...), name: str = Form(...), type: str = Form("product"), category: str = Form("Umum"), unit: str = Form("pcs"), cost_price: Decimal = Form(...), selling_price: Decimal = Form(0), stock: Decimal = Form(0), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    selling_price = calculate_catalog_selling_price(cost_price)
    db.add(Product(code=code, name=name, type=type, category=category, unit=unit, cost_price=cost_price, selling_price=selling_price, stock=stock)); db.commit()
    return RedirectResponse("/products", status_code=303)

@app.post("/products/{product_id}/edit")
def update_product(request: Request, product_id: int, code: str = Form(...), name: str = Form(...), type: str = Form("product"), category: str = Form("Umum"), unit: str = Form("pcs"), cost_price: Decimal = Form(...), selling_price: Decimal = Form(...), stock: Decimal = Form(0), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    product = db.get(Product, product_id)
    if product:
        product.code = code
        product.name = name
        product.type = type
        product.category = category
        product.unit = unit
        product.cost_price = cost_price
        product.selling_price = calculate_catalog_selling_price(cost_price)
        product.stock = stock
        db.commit()
    return RedirectResponse("/products", status_code=303)

@app.get("/quotations", response_class=HTMLResponse)
def quotations(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    rows = db.scalars(select(Quotation).options(joinedload(Quotation.customer)).order_by(Quotation.id.desc())).all()
    return render(request, "quotations.html", quotations=rows)

@app.get("/quotations/new", response_class=HTMLResponse)
def new_quotation(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    return render(request, "quotation_form.html", customers=db.scalars(select(Customer).order_by(Customer.name)).all(), products=db.scalars(select(Product).where(Product.is_active == True).order_by(Product.name)).all())

@app.post("/quotations")
def create_quotation(request: Request, customer_id: int = Form(...), product_id: list[str] = Form(...), quantity: list[Decimal] = Form(...), discount: Decimal = Form(0), tax: Decimal = Form(0), notes: str = Form(""), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    number = f"Q-{date.today():%Y%m%d}-{(db.scalar(select(func.count(Quotation.id))) or 0) + 1:03d}"
    quotation = Quotation(number=number, customer_id=customer_id, discount=discount, tax=tax, notes=notes)
    db.add(quotation); db.flush()
    for pid, qty in zip(product_id, quantity):
        if not pid:
            continue
        product = db.get(Product, int(pid))
        if product and qty > 0:
            db.add(QuotationItem(quotation_id=quotation.id, product_id=pid, quantity=qty, cost_price=product.cost_price, selling_price=product.selling_price))
    db.commit()
    return RedirectResponse(f"/quotations/{quotation.id}", status_code=303)

@app.get("/quotations/{quotation_id}", response_class=HTMLResponse)
def quotation_detail(request: Request, quotation_id: int, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    quotation = db.scalar(select(Quotation).options(joinedload(Quotation.customer), joinedload(Quotation.items).joinedload(QuotationItem.product)).where(Quotation.id == quotation_id))
    if not quotation: return RedirectResponse("/quotations", status_code=303)
    totals = calculate_quotation([calculate_item(i.quantity, i.cost_price, i.selling_price, i.discount) for i in quotation.items], quotation.discount, quotation.tax)
    return render(request, "quotation_detail.html", quotation=quotation, totals=totals)

@app.post("/quotations/{quotation_id}/status")
def update_quotation_status(request: Request, quotation_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    quotation = db.get(Quotation, quotation_id)
    if quotation: quotation.status = status; db.commit()
    return RedirectResponse(f"/quotations/{quotation_id}", status_code=303)

@app.get("/quotations/{quotation_id}/pdf")
def quotation_pdf_download(request: Request, quotation_id: int, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    quotation = db.scalar(select(Quotation).options(joinedload(Quotation.customer), joinedload(Quotation.items).joinedload(QuotationItem.product)).where(Quotation.id == quotation_id))
    totals = calculate_quotation([calculate_item(i.quantity, i.cost_price, i.selling_price, i.discount) for i in quotation.items], quotation.discount, quotation.tax)
    return StreamingResponse(quotation_pdf(quotation, totals), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={quotation.number}.pdf"})

@app.post("/quotations/{quotation_id}/project")
def create_project(request: Request, quotation_id: int, name: str = Form(...), location: str = Form(""), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    quotation = db.get(Quotation, quotation_id)
    if quotation and quotation.status == "Approved" and not db.scalar(select(Project).where(Project.quotation_id == quotation_id)):
        items = db.scalars(select(QuotationItem).where(QuotationItem.quotation_id == quotation_id)).all()
        total = calculate_quotation([calculate_item(i.quantity, i.cost_price, i.selling_price, i.discount) for i in items], quotation.discount, quotation.tax)["total"]
        db.add(Project(customer_id=quotation.customer_id, quotation_id=quotation.id, name=name, location=location, total_value=total)); db.commit()
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/finance", response_class=HTMLResponse)
def finance(request: Request, db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    return render(request, "finance.html", customers=db.scalars(select(Customer).order_by(Customer.name)).all(), invoices=db.scalars(select(Invoice).order_by(Invoice.id.desc())).all(), projects=db.scalars(select(Project).order_by(Project.id.desc())).all())

@app.post("/finance/invoices")
def add_invoice(request: Request, customer_id: int = Form(...), project_id: str = Form(""), total: Decimal = Form(...), due_date: date | None = Form(None), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    number = f"INV-{date.today():%Y%m%d}-{(db.scalar(select(func.count(Invoice.id))) or 0) + 1:03d}"
    project_id_value = int(project_id) if project_id else None
    db.add(Invoice(customer_id=customer_id, project_id=project_id_value, invoice_number=number, total=total, due_date=due_date)); db.commit()
    return RedirectResponse("/finance", status_code=303)

@app.post("/finance/payments")
def add_payment(request: Request, invoice_id: int = Form(...), amount: Decimal = Form(...), payment_method: str = Form("Transfer"), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    invoice = db.get(Invoice, invoice_id)
    if invoice:
        db.add(Payment(invoice_id=invoice_id, amount=amount, payment_method=payment_method))
        paid = sum((Decimal(str(p.amount or 0)) for p in db.scalars(select(Payment).where(Payment.invoice_id == invoice_id)).all()), Decimal(0)) + amount
        invoice.status = "Paid" if paid >= invoice.total else "Partially Paid"
        db.commit()
    return RedirectResponse("/finance", status_code=303)

@app.post("/finance/expenses")
def add_expense(request: Request, category: str = Form(...), amount: Decimal = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    if not is_authenticated(request): return RedirectResponse("/login", status_code=303)
    db.add(Expense(category=category, amount=amount, description=description)); db.commit()
    return RedirectResponse("/finance", status_code=303)
