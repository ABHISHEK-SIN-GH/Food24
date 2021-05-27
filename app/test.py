import razorpay
client = razorpay.Client(auth=('rzp_test_PlEYg3Ud7QmRGo','xELzeSakL6gWRrNM2Of1wTBl'))
data = {
    'amount': 100*100,
    'currency': 'INR',
    'receipt': "DroppersService",
    'notes': {'name':'abhi'},
    }
orders = client.order.create(data=data)
print(orders)
# {'id': 'order_HEbBNkYAFeNBjm', 'entity': 'order', 'amount': 10000, 'amount_paid': 0, 'amount_due': 10000, 'currency': 'INR', 'receipt': 'DroppersService', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': {'name': 'abhi'}, 'created_at': 1621852579}