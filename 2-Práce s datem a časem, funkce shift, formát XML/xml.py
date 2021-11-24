import pandas
import requests

r = requests.get("https://raw.githubusercontent.com/pesikj/progr2-python/master/data/invoices.xml")
open("invoices.xml", "wb").write(r.content)

publications = pandas.read_xml("invoices.xml")

print(publications.head())

publications.to_xml("invoices_export.xml", index=False, root_name="invoices", row_name="invoice")