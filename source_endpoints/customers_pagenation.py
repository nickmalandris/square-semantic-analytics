from authenticate import get_square_client

client = get_square_client()

# customers = client.customers.list(
#     # limit=10,
#     sort_field="DEFAULT",
#     sort_order="DESC"
# )
orders = client.orders.search(
    location_ids=["LNTHXYC3W0E87", "LC3E6FJECFBW5"],
    query={
        "sort": {"sort_field": "CREATED_AT", "sort_order": "ASC"},
        "filter": {
            "date_time_filter": {"created_at": {"start_at": "2022-08-26T06:05:58.259Z"}}
        },
    },
    return_entries=False,
    limit=1000,
)
count = 0
for order in orders:
    count += 1
    print(count)
# for customer in customers:
#     print(
#       f"Customer: ID: {customer.id}, "
#       f"Version: {customer.version}, "
#       f"Given name: {customer.given_name}, "
#       f"Family name: {customer.family_name}"
#   )
