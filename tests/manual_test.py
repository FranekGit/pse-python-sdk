from pse_sdk import PSEClient

client = PSEClient()

resp = client.get_demand(start="2026-01-01", end="2026-01-02", format="dataframe")

print(resp)
