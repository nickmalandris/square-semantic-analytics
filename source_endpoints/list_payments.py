from sqlmodel import Session
from models.payments import BasePaymentModel, Payments
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError, IntegrityError
import pendulum


def get_payments(
    client,
    session: Session,
    sort_field: str = "CREATED_AT",
    sort_order: str = "DESC",
    begin_time: str | None = None,
    limit: int = 100,
    **kwargs,
):
    with session:
        try:
            incremental_begin_time = session.exec(
                text("""select max(created_at) from payment""")
            ).scalar()
        except ProgrammingError:
            print("Table does not exist, doing a full load...")
            incremental_begin_time = None

    if incremental_begin_time:
        begin_time = incremental_begin_time

    payments = client.payments.list(
        sort_field=sort_field,
        sort_order=sort_order,
        begin_time=pendulum.instance(begin_time, tz="UTC"),
        limit=limit,
        **kwargs,
    )

    for payment in payments:
        validate_payment_model = BasePaymentModel(**payment.model_dump())
        sql_model = Payments(
            **validate_payment_model.model_dump(
                exclude={
                    "amount_money",
                    "device_details",
                    "processing_feecard_payment_timeline",
                }
            )
        )

        with session:
            try:
                session.add(sql_model)
                session.commit()
                session.close()
            except IntegrityError:
                print(f"Skipping duplicate record for payment id: {sql_model.id}")
                continue
