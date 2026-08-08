FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG TARGETARCH
ARG MUJOCO_VERSION=3.11.0
ARG CYCLONEDDS_VERSION=11.0.1
ARG CPP_TUI_VERSION=1.12.0

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
      build-essential \
      bison \
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
      python3-dev \
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

RUN set -eux; \
    cyclonedds_archive="cyclonedds-${CYCLONEDDS_VERSION}.tar.gz"; \
    cyclonedds_cxx_archive="cyclonedds-cxx-${CYCLONEDDS_VERSION}.tar.gz"; \
    curl --fail --location --retry 3 \
      --output "/tmp/${cyclonedds_archive}" \
      "https://github.com/eclipse-cyclonedds/cyclonedds/archive/refs/tags/${CYCLONEDDS_VERSION}.tar.gz"; \
    curl --fail --location --retry 3 \
      --output "/tmp/${cyclonedds_cxx_archive}" \
      "https://github.com/eclipse-cyclonedds/cyclonedds-cxx/archive/refs/tags/${CYCLONEDDS_VERSION}.tar.gz"; \
    echo "c25d46075ad6b5cee564bda9e5f49509e9a6dbb1a8b858e708eb360d335cf973  /tmp/${cyclonedds_archive}" \
      | sha256sum --check; \
    echo "f20d30610100329716b2bd810054741a6ce9be6a9eeefcf941def1e1b311ddb2  /tmp/${cyclonedds_cxx_archive}" \
      | sha256sum --check; \
    mkdir --parents /tmp/cyclonedds /tmp/cyclonedds-cxx; \
    tar --extract --gzip --file "/tmp/${cyclonedds_archive}" \
      --directory /tmp/cyclonedds --strip-components=1; \
    tar --extract --gzip --file "/tmp/${cyclonedds_cxx_archive}" \
      --directory /tmp/cyclonedds-cxx --strip-components=1; \
    cmake -S /tmp/cyclonedds -B /tmp/cyclonedds-build \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/opt/cyclonedds \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_TESTING=OFF; \
    cmake --build /tmp/cyclonedds-build --parallel; \
    cmake --install /tmp/cyclonedds-build; \
    cmake -S /tmp/cyclonedds-cxx -B /tmp/cyclonedds-cxx-build \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/opt/cyclonedds \
      -DCMAKE_PREFIX_PATH=/opt/cyclonedds \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_TESTING=OFF \
      -DENABLE_LEGACY=OFF; \
    cmake --build /tmp/cyclonedds-cxx-build --parallel; \
    cmake --install /tmp/cyclonedds-cxx-build; \
    rm --recursive --force \
      "/tmp/${cyclonedds_archive}" \
      "/tmp/${cyclonedds_cxx_archive}" \
      /tmp/cyclonedds \
      /tmp/cyclonedds-build \
      /tmp/cyclonedds-cxx \
      /tmp/cyclonedds-cxx-build

ENV CYCLONEDDS_HOME=/opt/cyclonedds

RUN set -eux; \
    cpp_tui_archive="cpp-tui-${CPP_TUI_VERSION}.tar.gz"; \
    curl --fail --location --retry 3 \
      --output "/tmp/${cpp_tui_archive}" \
      "https://github.com/jonoton/cpp-tui/archive/refs/tags/v${CPP_TUI_VERSION}.tar.gz"; \
    echo "192806f877c3c5e78445d760aad640d54b502ae7aeac34cf4a5d2d6977f8900c  /tmp/${cpp_tui_archive}" \
      | sha256sum --check; \
    mkdir --parents /opt/cpp-tui/include /tmp/cpp-tui; \
    tar --extract --gzip --file "/tmp/${cpp_tui_archive}" \
      --directory /tmp/cpp-tui --strip-components=1; \
    cp /tmp/cpp-tui/cpptui.hpp /opt/cpp-tui/include/; \
    cp /tmp/cpp-tui/LICENSE /opt/cpp-tui/; \
    rm --recursive --force "/tmp/${cpp_tui_archive}" /tmp/cpp-tui

RUN python3 -m venv /opt/robotics-lab/venv \
    && /opt/robotics-lab/venv/bin/pip install --no-cache-dir \
      --no-binary cyclonedds \
      "cyclonedds==${CYCLONEDDS_VERSION}" \
      "mujoco==${MUJOCO_VERSION}" \
    && test -f /opt/cyclonedds/include/dds/dds.h \
    && test -f /opt/cyclonedds/include/ddscxx/dds/dds.hpp \
    && test -f /opt/cyclonedds/lib/libddsc.so \
    && test -f /opt/cyclonedds/lib/libddscxx.so \
    && test -f /opt/cpp-tui/include/cpptui.hpp \
    && test -f /opt/mujoco/include/mujoco/mujoco.h \
    && test -f /opt/mujoco/lib/libmujoco.so \
    && /opt/robotics-lab/venv/bin/python -c \
      "import importlib.metadata, mujoco; assert importlib.metadata.version('cyclonedds') == '${CYCLONEDDS_VERSION}'; assert mujoco.__version__ == '${MUJOCO_VERSION}'; mujoco.MjModel.from_xml_string('<mujoco/>')"

ENV MUJOCO_HOME=/opt/mujoco
ENV CPP_TUI_HOME=/opt/cpp-tui
ENV CMAKE_PREFIX_PATH=/opt/cyclonedds
ENV LD_LIBRARY_PATH=/opt/mujoco/lib:/opt/cyclonedds/lib
ENV PATH=/opt/robotics-lab/venv/bin:/opt/mujoco/bin:/opt/cyclonedds/bin:${PATH}

WORKDIR /workspace/robotics-lab

CMD ["bash"]
