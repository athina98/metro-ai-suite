# System Requirements

This section provides the hardware, software, and platform requirements to set up and
run the application.

## Supported Platforms

**Operating Systems**

- Ubuntu 24.04 LTS

## Minimum Requirements

| **Component**       | **Minimum Requirement** |
|---------------------|-------------------------|
| **Processor**       | Intel® Core™ Ultra Processors Series 1 and above |
| **GPU/Accelerator** | Integrated GPU (recommended; CPU fallback supported) |

## Hardware Requirements

- Intel® GPU recommended; CPU fallback supported
- For Panther Lake `xe` GPU telemetry, install `xpu-smi` on the host before running
  `./setup.sh`
- Host install example on Ubuntu OS version 24.04 when the Intel graphics repository
  or PPA is already configured:
  `sudo apt install xpu-smi`
- If the GPU name still appears as a raw Peripheral Component Interconnect (PCI) ID
  after host package install, refresh the host PCI ID database with:
  `sudo update-pciids`

## Software Requirements

- Docker Engine
- Docker Compose tool
- Python 3 programming language
- OpenSSL toolkit
- jq tool
- Install the Git Large File Storage (LFS) extension **before** cloning, for video file storage:

  ```bash
  # Ubuntu/Debian
  sudo apt install git-lfs
  git lfs install
  ```
