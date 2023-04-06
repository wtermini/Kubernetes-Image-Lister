import os
import yaml
import argparse

def find_images_in_manifest(file_path):
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

                            images = []
                            for container in containers:
                                if 'image' in container:
                                    images.append(container['image'])
                            all_images.extend(images)
            return all_images

        except yaml.YAMLError as e:
            print(f"Error parsing {file_path}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='List container images in Kubernetes manifest files')
    parser.add_argument('folder', type=str, help='Path to the folder containing the manifest files')
    parser.add_argument('--show-filenames', action='store_true', help='Show filenames before listing images')
    args = parser.parse_args()

    for root, _, files in os.walk(args.folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                images = find_images_in_manifest(file_path)
                if images and args.show_filenames:
                    print(f"IMAGES FROM {file}:")
                for image in images:
                    print(f"Image: {image}")

if __name__ == '__main__':
    main()
