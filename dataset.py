import kagglehub

# Download latest version
path = kagglehub.dataset_download("donovanbangs/call-centre-queue-simulation")

print("Path to dataset files:", path)