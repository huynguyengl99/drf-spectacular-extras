#!/usr/bin/env bash

if [ "$1" == "--fix" ]; then
  ruff check . --fix && black ./drf_spectacular_extras && toml-sort ./*.toml
else
  ruff check . && black ./drf_spectacular_extras --check && toml-sort ./*.toml --check
fi
