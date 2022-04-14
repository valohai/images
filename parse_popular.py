import argparse
import sys
import json

safe_prefixes = {
    'floydhub/',
    'pytorch/',
    'tensorflow/',
    'ufoym/',
    'valohai/',
}


def clean_image_names(image_count_pairs):
    return [
        (image.replace('gcr.io/', ''), count)
        for (image, count)
        in image_count_pairs
    ]


def filter_images(image_count_pairs):
    valid = []
    invalid = []
    for pair in image_count_pairs:
        image = pair[0]
        (valid if any(image.startswith(safe_prefix) for safe_prefix in safe_prefixes) else invalid).append(pair)
    return (valid, invalid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', default=sys.stdin, type=argparse.FileType('r'))
    ap.add_argument('--threshold', default=.02, type=float)
    args = ap.parse_args()
    data = json.load(args.input)
    image_count_pairs = list(data['images'].items())
    image_count_pairs = clean_image_names(image_count_pairs)
    valid, invalid = filter_images(image_count_pairs)
    total_valid_count = sum(p[1] for p in valid)

    for image, count in sorted(valid, key=lambda p: p[1], reverse=True):
        if count > args.threshold * total_valid_count:
            print(f'{image}: {count}')


if __name__ == '__main__':
    main()
