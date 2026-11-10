"""
Retention Agent

Purpose
-------
Transforms churn intelligence into
business retention actions.

Input:
    Risk Level
    Customer Segment

Output:
    Offer
    Channel
    Priority
    Expected Retention Lift
    Justification
"""


class RetentionAgent:

    def __init__(self):

        self.rules = {

            ("High", "At Risk"): {
                "offer": "20% Cashback",
                "channel": "Phone Call + Email",
                "priority": "Critical",
                "expected_lift": "18-22%",
                "justification":
                    "High churn risk customers "
                    "require aggressive retention."
            },

            ("High", "Price Sensitive"): {
                "offer": "15% Discount Upgrade",
                "channel": "Email + SMS",
                "priority": "High",
                "expected_lift": "15-18%",
                "justification":
                    "Pricing concerns are driving churn."
            },

            ("High", "Champions"): {
                "offer": "Premium Loyalty Reward",
                "channel": "Relationship Manager",
                "priority": "Critical",
                "expected_lift": "20-25%",
                "justification":
                    "Protect high-value customers."
            },

            ("Medium", "At Risk"): {
                "offer": "10% Cashback",
                "channel": "Email",
                "priority": "Medium",
                "expected_lift": "12-15%",
                "justification":
                    "Early intervention recommended."
            },

            ("Medium", "Loyal Customers"): {
                "offer": "Reward Points Bonus",
                "channel": "Email",
                "priority": "Medium",
                "expected_lift": "10-14%",
                "justification":
                    "Maintain loyalty and engagement."
            },

            ("Low", "Champions"): {
                "offer": "VIP Benefits Package",
                "channel": "Email",
                "priority": "Low",
                "expected_lift": "8-10%",
                "justification":
                    "Maintain premium relationship."
            },

            ("Low", "Loyal Customers"): {
                "offer": "Loyalty Rewards Program",
                "channel": "Email",
                "priority": "Low",
                "expected_lift": "6-8%",
                "justification":
                    "Encourage continued engagement."
            },

            ("Low", "New Customers"): {
                "offer": "Reward Point Bonus",
                "channel": "Email + App Notification",
                "priority": "Medium",
                "expected_lift": "8-12%",
                "justification":
                    "Support onboarding and engagement."
            }
        }

    def generate_retention_strategy(

        self,

        risk_level,

        segment

    ):

        strategy = self.rules.get(

            (risk_level, segment),

            {
                "offer": "Standard Retention Offer",
                "channel": "Email",

                "priority": "Medium",

                "expected_lift": "5-10%",

                "justification":
                    "General retention strategy."
            }
        )

        return {

            "risk_level": risk_level,

            "segment": segment,

            **strategy
        }


if __name__ == "__main__":

    agent = RetentionAgent()

    result = (
        agent.generate_retention_strategy(
            risk_level="High",
            segment="At Risk"
        )
    )

    print("\n")
    print("=" * 60)
    print("RETENTION STRATEGY")
    print("=" * 60)

    for key, value in result.items():

        print(f"{key}: {value}")