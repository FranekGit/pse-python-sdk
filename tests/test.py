from pse import PSEClient

client = PSEClient()

resp = client.get_cen(start="2026-03-01", end="2026-03-01", format="dataframe")

print(resp)
