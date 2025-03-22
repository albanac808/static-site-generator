import time

props = {f"key{i}": f"value{i}" for i in range(100000)}

# Using +=
start = time.time()
html = ""
for key, value in props.items():
    html += f' {key}="{value}"'
end = time.time()
print(f"Using +=: {end - start} seconds")

# Using join
start = time.time()
html = " ".join(f'{key}="{value}"' for key, value in props.items())
end = time.time()
print(f"Using join: {end - start} seconds")