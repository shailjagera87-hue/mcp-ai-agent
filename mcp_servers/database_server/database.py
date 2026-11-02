from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mcp_servers.database_server.models import Base


DATABASE_URL = "sqlite:///./customers.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def initialize_database():

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        existing = session.query(
            __import__(
                "mcp_servers.database_server.models",
                fromlist=["Customer"]
            ).Customer
        ).first()

        if existing:
            return

        from mcp_servers.database_server.models import Customer

        sample_customers = [
            Customer(
                name="Rahul Sharma",
                email="rahul@example.com",
                city="Ludhiana",
                phone="9876543210"
            ),
            Customer(
                name="Priya Verma",
                email="priya@example.com",
                city="Delhi",
                phone="9876543211"
            ),
            Customer(
                name="Amit Kumar",
                email="amit@example.com",
                city="Mumbai",
                phone="9876543212"
            ),
            Customer(
                name="Neha Singh",
                email="neha@example.com",
                city="Chandigarh",
                phone="9876543213"
            )
        ]

        session.add_all(sample_customers)
        session.commit()

    finally:
        session.close()