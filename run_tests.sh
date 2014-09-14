#!/usr/bin/env bash

coverage run --branch --source=vcii --omit='*__*' -m unittest
echo
coverage report
