<h1 align="center"> 📺 MKVrestyle </h1>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/mkvrestyle?label=Release&sort=semver" alt="Current bundle version" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/codestyle.yml?branch=main&label=Black" alt="Black">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/codequality.yml?branch=main&label=Ruff" alt="Ruff">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/statictyping.yml?branch=main&label=Mypy" alt="Mypy">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/security.yml?branch=main&label=Security%20check" alt="Security check" />
v
</div>

## 📝 Quickstart

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest -h
```

## 📜 Documentation

The documentation is available at [https://toshy.github.io/mkvrestyle](https://toshy.github.io/mkvrestyle).

## 🛠️ Contribute

### Requirements

* ☑️ [Pre-commit](https://pre-commit.com/#installation).
* 🐋 [Docker Compose V2](https://docs.docker.com/compose/install/)
* 📋 [Task 3.37+](https://taskfile.dev/installation/)

## ❕ License

This repository comes with a [MIT license](./LICENSE).
