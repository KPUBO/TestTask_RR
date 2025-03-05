from sqlalchemy.orm import Session

from core.models import PriceItem

priceitems = [
    PriceItem(vendor="Bosch",
              search_number="123ABC",
              search_vendor="bosch",
              number="123abc",
              description="Brake Pad",
              price=45.99,
              count=10),

    PriceItem(vendor="Valeo",
              search_number="456DEF",
              search_vendor="valeo",
              number="456def",
              description="Clutch Kit",
              price=120.50,
              count=5),

    PriceItem(vendor="SKF",
              search_number="789GHI",
              search_vendor="skf",
              number="789ghi",
              description="Wheel Bearing",
              price=35.75,
              count=8),

    PriceItem(vendor="LUK",
              search_number="101JKL",
              search_vendor="luk",
              number="101jkl",
              description="Flywheel",
              price=250.00,
              count=2),

    PriceItem(vendor="Mann",
              search_number="202MNO",
              search_vendor="mann",
              number="202mno",
              description="Oil Filter",
              price=12.99,
              count=15),

    PriceItem(vendor="NGK",
              search_number="303PQR",
              search_vendor="ngk",
              number="303pqr",
              description="Spark Plug",
              price=8.50,
              count=20),

    PriceItem(vendor="Denso",
              search_number="404STU",
              search_vendor="denso",
              number="404stu",
              description="Ignition Coil",
              price=55.30,
              count=7),

    PriceItem(vendor="Continental",
              search_number="505VWX",
              search_vendor="continental",
              number="505vwx",
              description="Timing Belt",
              price=90.00,
              count=3),

    PriceItem(vendor="Bosch",
              search_number="606YZA",
              search_vendor="bosch",
              number="606yza",
              description="Fuel Pump",
              price=140.75,
              count=4),

    PriceItem(vendor="Febi",
              search_number="707BCD",
              search_vendor="febi",
              number="707bcd",
              description="Control Arm",
              price=65.40,
              count=6)

]


def organizations_insert(session: Session):
    session.add_all(priceitems)
    session.commit()

