# README

```bash
docker run -it --name cve-2025-9809 -v "$(pwd):/app" cve-docker /bin/bash
```

```bash
make exploit
make run
# Removes the exploit
make clean
```