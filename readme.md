# Kubernetes Image Lister

`kubernetes-image-lister` is a simple Python script that lists container images used in Kubernetes manifest files. It can process `.yaml` and `.yml` files, and supports `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, and `CronJob` resources.

## Requirements

- Python 3.6 or higher

## Usage

1. Clone the repository or download the `list_images.py` script.
2. Navigate to the folder containing the script.
3. Run the script with the path to the folder containing the manifest files as an argument:

```bash
python list_images.py /path/to/your/manifest/folder
```

## Optional Flags
--show-filenames: Show filenames before listing images. If this flag is set, the script will print the filename before listing the images found in it.

```
python list_images.py /path/to/your/manifest/folder --show-filenames
```

## Output
The script will output the list of container images found in the manifest files. If the --show-filenames flag is set, the output will also include the file each image came from:

```
IMAGES FROM xyz.yml
Image: IMAGE_NAME
```

## Troubleshooting
If the script encounters any issues parsing a manifest file, it will print an error message with the file name and the error details:

```
Error parsing /path/to/your/manifest/folder/problematic_file.yaml: ...
```

Please ensure that your manifest files are valid YAML and follow the expected structure for Kubernetes resources.
