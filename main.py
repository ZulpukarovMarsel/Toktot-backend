import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "8xp6kbwftk4fftbm",
    "client_secret": "ffbaea21014a0ada2293c01047335706"
})


payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"
    },
    "transactions": [{
        "amount": {
            "total": "10.00",
            "currency": "USD"
        },
        "description": "Test payment"
    }],
    "redirect_urls": {
        "return_url": "https://www.youtube.com/",
        "cancel_url": "https://chatgpt.com/?model=gpt-4o"
    }
})


if payment.create():
    print("Payment created successfully")
else:
    print(payment.error)
