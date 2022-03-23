#!/bin/bash
pipenv run db upgrade
pipenv run server -h 0.0.0.0