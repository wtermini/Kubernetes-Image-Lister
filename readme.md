# Kubernetes Image Lister
This Python script is designed to help list container images in Kubernetes manifest files and optionally replace them.

Prerequisites
Python 3.x
PyYAML module (pip install pyyaml)
tldextract module (pip install tldextract)
Usage  
`python k8s-image-finder.py <folder> [--config <config>] [--dry-run] [--replace]`

Arguments
- folder: Path to the folder containing the Kubernetes manifest files.
- --config: (Optional) Path to the config.yaml file that defines a mapping of external to internal registries and a list of exclude patterns for images.
- --dry-run: (Optional) Preview the result without updating the images.
- --replace: (Optional) Replace the images in the manifest files.
Example
List all container images in Kubernetes manifest files in the ./manifests directory:

```python k8s-image-finder.py ./manifests```

Replace all container images in Kubernetes manifest files in the ./manifests directory:

```python k8s-image-finder.py ./manifests --config config.yaml --replace```