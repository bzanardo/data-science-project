import json

data_1 = []

with open("training_data.json", "w") as output:
	for i in range(1, 101):
		file = "random" + str(i) + ".json"
		with open(file, "rb") as infile:
			file_data = json.load(infile)
			data_1 += file_data

	print(len(data_1))
	json.dump(data_1, output)



data_2 = []
with open("testing_data.json", "w") as output:
	for i in range(1, 24):
		file = "new" + str(i) + ".json"
		with open(file, "rb") as infile:
			file_data = json.load(infile)
			data_2 += file_data

	print(len(data_2))
	json.dump(data_2, output)


data_3 = []
with open("total_data.json", "w") as output:
	for i in range(1, 101):
		file = "random" + str(i) + ".json"
		with open(file, "rb") as infile:
			file_data = json.load(infile)
			data_3 += file_data

	for i in range(1, 24):
		file = "new" + str(i) + ".json"
		with open(file, "rb") as infile:
			file_data = json.load(infile)
			data_3 += file_data

	print(len(data_3))
	json.dump(data_3, output)