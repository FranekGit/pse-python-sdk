from pse_sdk import PSEClient

client = PSEClient()

resp = client.fetch(
    "his-wlk-cal",
    start="2026-01-01",
    end="2026-01-02",
    columns=["demand", "pv"],
    format="dataframe",
)

print(resp)
