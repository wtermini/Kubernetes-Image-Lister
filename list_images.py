import os
import re
import yaml
import argparse
import tldextract


def find_images_in_manifest(file_path, registry_map, exclude_patterns, dry_run=False, replace=False):
    with open(file_path, 'r') as f:
        try:
            contents = yaml.load_all(f, Loader=yaml.FullLoader)
            all_images = []
            for content in contents:
                if not content or 'kind' not in content:
                    continue

                if content['kind'] in ['Deployment', 'StatefulSet', 'DaemonSet', 'Job', 'CronJob']:
                    if 'spec' in content and 'template' in content['spec'] and 'spec' in content['spec']['template']:
                        if 'containers' in content['spec']['template']['spec']:
                            containers = content['spec']['template']['spec']['containers']

                            if content['kind'] == 'CronJob':
                                if 'jobTemplate' in content['spec'] and 'spec' in content['spec']['jobTemplate'] and 'template' in content['spec']['jobTemplate']['spec'] and 'spec' in content['spec']['jobTemplate']['spec']['template']:
                                    containers = content['spec']['jobTemplate']['spec']['template']['spec']['containers']

                            for container in containers:
                                if 'image' in container:
                                    original_image = container['image']
                                    if any(re.search(pattern, original_image) for pattern in exclude_patterns):
                                        # Skip images that match the exclude patterns
                                        continue

                                    if dry_run or replace:
                                        new_image = replace_image_registry(original_image, registry_map)
                                        print(f"Original Image: {original_image}")
                                        print(f"New Image: {new_image}\n")
                                        container['image'] = new_image
                                        all_images.append(new_image)
                                        if not dry_run:
                                            # Replace the original image string with the new image string in the file
                                            with open(file_path, 'r') as f:
                                                file_content = f.read()
                                            file_content = file_content.replace(original_image, new_image)
                                            with open(file_path, 'w') as f:
                                                f.write(file_content)
                                    else:
                                        all_images.append(original_image)

            return all_images

        except yaml.YAMLError as e:
            pass
            #print(f"Error parsing {file_path}: {e}")
        return []



def replace_image_registry(image, registry_map):
    extracted = tldextract.extract(image)
    if not extracted.suffix:
        # No valid TLD found, assume it's a Docker Hub image
        internal = registry_map.get('docker_hub', {}).get('internal', '')
        return f"{internal}/{image}"

    for key, value in registry_map.items():
        external = value.get('external', '')
        internal = value.get('internal', '')

        if extracted.domain + '.' + extracted.suffix == external:
            return image.replace(external, internal)

    return image





def main():
    parser = argparse.ArgumentParser(description='List container images in Kubernetes manifest files and optionally replace them')
    parser.add_argument('folder', type=str, help='Path to the folder containing the manifest files')
    parser.add_argument('--config', type=str, help='Path to the config.yaml file')
    parser.add_argument('--dry-run', action='store_true', help='Preview the result without updating the images')
    parser.add_argument('--replace', action='store_true', help='Replace the images in the manifest files')
    args = parser.parse_args()

    registry_map = {}
    exclude_patterns = []

    if args.config:
        with open(args.config, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            registry_map = config.get('map', {})
            exclude_patterns = config.get('exclude', [])

    for root, _, files in os.walk(args.folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                images = find_images_in_manifest(file_path, registry_map, exclude_patterns, args.dry_run, args.replace)
                if not args.dry_run and not args.replace:
                    for image in images:
                        print(f"Image: {image}")



if __name__ == '__main__':
    main()