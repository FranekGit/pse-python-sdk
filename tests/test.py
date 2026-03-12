from pse import PSE

client = PSE()

resp = client.get_cen(start="2026-03-01", end="2026-03-01", format="dataframe")

print(resp)
