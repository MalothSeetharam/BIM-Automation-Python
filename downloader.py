import urllib.request

url = "https://raw.githubusercontent.com/BuildingSMART/Sample-Test-Files/master/IFC%202x3/Duplex%20Apartment/Design/Duplex_A_20110907.ifc"
print("⏳ Downloading your sample IFC file directly... Please wait.")
urllib.request.urlretrieve(url, "sample_model.ifc")
print("✅ Done! 'sample_model.ifc' has been successfully downloaded into your folder.")