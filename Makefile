# style the code according to accepted standards for the repo
.PHONY: style
style:
	pre-commit run --all-files -c .pre-commit-config.yaml
