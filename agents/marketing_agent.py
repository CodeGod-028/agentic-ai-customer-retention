"""
Marketing Agent

Purpose
-------
Generate personalized customer
retention campaigns.

Current Version:
    Rule-Based

Future Version:
    Gemini Powered
"""

from datetime import datetime


class MarketingAgent:

    def __init__(self):

        self.brand_name = "TeleConnect"

    def generate_campaign(

        self,

        customer_id,

        segment,

        offer,

        channel,

        priority

    ):

        subject = self.create_subject(
            segment,
            offer
        )

        campaign_text = self.create_campaign_body(
            customer_id=customer_id,
            segment=segment,
            offer=offer,
            channel=channel,
            priority=priority
        )

        return {

            "subject": subject,

            "campaign_text": campaign_text,

            "recommended_channel": channel,

            "priority": priority,

            "generated_timestamp":
                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }

    def create_subject(
        self,
        segment,
        offer
    ):

        if segment == "Champions":

            return (
                f"Exclusive Reward Just for You - {offer}"
            )

        elif segment == "At Risk":

            return (
                f"Special Offer to Keep You Connected - {offer}"
            )

        elif segment == "New Customers":

            return (
                f"Welcome! Unlock Your New Benefits"
            )

        elif segment == "Price Sensitive":

            return (
                f"Save More with Our Latest Offer"
            )

        return (
            f"Exclusive Customer Offer - {offer}"
        )

    def create_campaign_body(

        self,

        customer_id,

        segment,

        offer,

        channel,

        priority

    ):

        greeting = (
            f"Dear Valued Customer ({customer_id}),"
        )

        if segment == "Champions":

            message = f"""
Thank you for being one of our most valued customers.

As a token of appreciation, we are delighted to offer:

✅ {offer}

Your loyalty and long-term engagement have made you an important member of our customer community.

We look forward to continuing to serve you with premium experiences and rewards.
"""

        elif segment == "At Risk":

            message = f"""
We noticed that your engagement with our services may be changing.

To ensure you continue enjoying the best experience, we would like to offer:

✅ {offer}

This exclusive retention offer has been selected specifically to provide more value and savings.

We would love the opportunity to keep serving you.
"""

        elif segment == "Price Sensitive":

            message = f"""
We understand that getting the best value matters.

That's why we are excited to provide:

✅ {offer}

Designed to help maximize benefits while reducing costs.

Take advantage of this opportunity today.
"""

        elif segment == "New Customers":

            message = f"""
Welcome to {self.brand_name}.

To help you get started, we are pleased to offer:

✅ {offer}

Explore our services and discover the value our platform delivers every day.
"""

        else:

            message = f"""
We are pleased to offer:

✅ {offer}

Thank you for being a valued customer.
"""

        closing = f"""

Recommended Channel:
{channel}

Priority:
{priority}

Best Regards,
Customer Success Team
{self.brand_name}
"""

        return greeting + "\n\n" + message + closing


if __name__ == "__main__":

    agent = MarketingAgent()

    result = agent.generate_campaign(
        customer_id="7590-VHVEG",
        segment="At Risk",
        offer="20% Cashback",
        channel="Phone Call + Email",
        priority="Critical"
    )

    print("\n")
    print("=" * 70)
    print("MARKETING CAMPAIGN")
    print("=" * 70)

    print(
        f"Subject:\n{result['subject']}"
    )

    print("\n")

    print(
        result["campaign_text"]
    )