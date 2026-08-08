FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG TARGETARCH
ARG MUJOCO_VERSION=3.11.0

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
      build-essential \
      ca-certificates \
      cmake \
      curl \
      git \
      libgl1 \
      libx11-6 \
      libxcursor1 \
      libxi6 \
      libxinerama1 \
      libxrandr2 \
      ninja-build \
      python3 \
      python3-pip \
      python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    case "${TARGETARCH}" in \
      amd64) \
        mujoco_arch="x86_64"; \
        mujoco_sha256="681a9353b296a06682e9e757d6d21ab7a0a5a5bdb218a1c05cb9a38536817c79" \
        ;; \
      arm64) \
        mujoco_arch="aarch64"; \
        mujoco_sha256="572616d27117a9739fcc6affb8d21ff24a6b4d376a8dc4756f1602beb82f4e83" \
        ;; \
      *) \
        echo "Unsupported architecture: ${TARGETARCH}" >&2; \
        exit 1 \
        ;; \
    esac; \
    archive="mujoco-${MUJOCO_VERSION}-linux-${mujoco_arch}.tar.gz"; \
    curl --fail --location --retry 3 \
      --output "/tmp/${archive}" \
      "https://github.com/google-deepmind/mujoco/releases/download/${MUJOCO_VERSION}/${archive}"; \
    echo "${mujoco_sha256}  /tmp/${archive}" | sha256sum --check; \
    mkdir --parents /opt/mujoco; \
    tar --extract --gzip --file "/tmp/${archive}" \
      --directory /opt/mujoco --strip-components=1; \
    rm "/tmp/${archive}"

RUN python3 -m venv /opt/robotics-lab/venv \
    && /opt/robotics-lab/venv/bin/pip install --no-cache-dir \
      "mujoco==${MUJOCO_VERSION}" \
    && test -f /opt/mujoco/include/mujoco/mujoco.h \
    && test -f /opt/mujoco/lib/libmujoco.so \
    && /opt/robotics-lab/venv/bin/python -c \
      "import mujoco; assert mujoco.__version__ == '${MUJOCO_VERSION}'; mujoco.MjModel.from_xml_string('<mujoco/>')"

ENV MUJOCO_HOME=/opt/mujoco
ENV LD_LIBRARY_PATH=/opt/mujoco/lib
ENV PATH=/opt/robotics-lab/venv/bin:/opt/mujoco/bin:${PATH}

WORKDIR /workspace/robotics-lab

CMD ["bash"]
