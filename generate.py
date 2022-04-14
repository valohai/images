import yaml


def compact(lst):
    return [x for x in lst if x]


TENSORFLOW_VERSIONS = [
    "1.13.1-py3",
    "2.2.0",
    "2.2.0-gpu",
    "2.6.0",
    "2.6.0-gpu",
    "2.7.0",
    "2.7.0-gpu",
]
DEEPO_VARIANTS = [
    ("CUDA 11.3 GPU", "all-py38-cu113"),
    ("CPU", "all-py38-cpu"),
]

PYTORCH_VERSIONS = [
    ("1.10.0 on CUDA 11.3", "1.10.0-cuda11.3-cudnn8-runtime"),
    ("1.11.0 on CUDA 11.3", "1.11.0-cuda11.3-cudnn8-runtime"),
    ("1.9.1 on CUDA 11.1", "1.9.1-cuda11.1-cudnn8-runtime"),
]


def generate():
    data = {}

    for version in TENSORFLOW_VERSIONS:
        tf_ver = version.split("-")[0]
        data[f"tensorflow/tensorflow:{version}"] = {
            "isRecommended": ("2.6" in version or "2.7" in version),
            "description": " ".join(
                [
                    f"TensorFlow {tf_ver} on Python 3",
                    "with GPU support" if "gpu" in version else "(CPU only)",
                ]
            ),
            "tags": compact(
                [
                    f"TensorFlow {tf_ver}",
                    "Python 3",
                    "GPU" if "gpu" in version else "",
                ]
            ),
        }

    for spec, variant in DEEPO_VARIANTS:
        data[f"ufoym/deepo:{variant}"] = {
            "isRecommended": True,
            "description": f"All-in-one Deep Learning image for {spec} on Python 3.8",
            "tags": compact(
                [
                    "Python 3",
                    "GPU" if "cu113" in spec else "",
                ]
            ),
        }

    for spec, variant in PYTORCH_VERSIONS:
        version = variant.split("-")[0]
        data[f"pytorch/pytorch:{variant}"] = {
            "isRecommended": True,
            "description": f"PyTorch {spec}",
            "tags": ["PyTorch", f"PyTorch {version}", "GPU"],
        }

    return data


def main():
    with open("images.v2.yaml", "w") as f:
        yaml.safe_dump(generate(), f, default_flow_style=False, sort_keys=True)


if __name__ == "__main__":
    main()
