from agents.executive_agent import (
    ExecutiveAgent
)

from agents.executive_report_agent import (
    ExecutiveReportAgent
)

import pandas as pd


df = pd.read_csv(
    "data/customer_segments.csv"
)

customer_id = (
    df.iloc[0]["customerID"]
)

executive_agent = ExecutiveAgent()

result = executive_agent.run(
    customer_id
)

report_agent = (
    ExecutiveReportAgent()
)

report_path = (
    report_agent.generate_report(
        result
    )
)

print(
    f"Report Created: {report_path}"
)