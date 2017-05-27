from decimal import Decimal

from django.conf import settings

import gocardless

PAYMENT_TYPES = (
    ('subscription', 'Monthly donation'),
    ('bill', 'Single donation'),
)

PAYMENT_UNITS = (
    (3, '£3'),
    (10, '£10'),
    (25, '£25'),
    (50, '£50'),
)


class GoCardlessHelper(object):
    def __init__(self):
        self.gocardless = gocardless
        if getattr(settings, 'GOCARDLESS_USE_SANDBOX', False):
            self.gocardless.environment = "sandbox"
        self.gocardless.set_details(
            app_id=settings.GOCARDLESS_APP_ID,
            app_secret=settings.GOCARDLESS_APP_SECRET,
            access_token=settings.GOCARDLESS_ACCESS_TOKEN,
            merchant_id=settings.GOCARDLESS_MERCHANT_ID,
        )

    def get_payment_url(self, amount, payment_type="bill",
        interval_length=None, interval_unit=None, name=None, description=None):
        """
        A bill is one off, a subscription is repeating
        """

        assert payment_type in [i[0] for i in PAYMENT_TYPES]
        amount = Decimal(amount)

        if not name:
            name = settings.GO_CARDLESS_PAYMENT_NAME
        if not description:
            description = settings.GO_CARDLESS_PAYMENT_DESCRIPTION

        if payment_type == "bill":
            return gocardless.client.new_bill_url(amount, name=name)

        return gocardless.client.new_subscription_url(
            amount=amount,
            interval_length=1,
            interval_unit="month",
            name=name,
            description=description)




# # client.new_subscription_url(
# amount=10,
# interval_length=1,
# interval_unit="month",
# name="Premium Subscription",
# description="A premium subscription for my site",)
