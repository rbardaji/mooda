from mooda import WaterFrame

directory_path = r"PATH"
file_path = r"FILE"

path = directory_path + file_path

print("Loading WaterFrame")
wf = WaterFrame(path)
print("Done")

save_path = "{}csv".format(path[:-2])
print("Saving to CSV")
wf.to_csv(save_path)
print("Done")
