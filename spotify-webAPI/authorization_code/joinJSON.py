import json

data = []

with open("testing_data.json", "w") as output:
	with open("top50.json", "rb") as top50file:
		file_data = json.load(top50file)
		data += file_data

	for i in range(1, 21):
		file = "random" + str(i) + ".json"
		with open(file, "rb") as infile:
			file_data = json.load(infile)
			data += file_data

	print(len(data))
	json.dump(data, output)
