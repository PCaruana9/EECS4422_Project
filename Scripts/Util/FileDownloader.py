import requests
from tqdm import tqdm

urlBase = "http://www02.smt.ufrj.br/~fusion/Database/Registered/Camouflage/take_"
nameBase = "Camouflage_"


for i in range(1,8):
	url = urlBase + str(i) + ".tar.gz"
	filename = nameBase + url.split("/")[-1]
	# Streaming, so we can iterate over the response.
	r = requests.get(url, stream=True)
	# Total size in bytes.
	total_size = int(r.headers.get('content-length', 0))
	block_size = 1024 #1 Kibibyte
	t=tqdm(total=total_size, unit='iB', unit_scale=True)

	print("\n >>Downloading " + filename + "...")
	with open(filename, 'wb') as f:
		for data in r.iter_content(block_size):
			t.update(len(data))
			f.write(data)
	t.close()
	if total_size != 0 and t.n != total_size:
		print("ERROR, something went wrong")

print("--Finished!")

    



