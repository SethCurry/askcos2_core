# Install issues

- Depends on `python` being in PATH, but new ubuntu does not symlink `python` to `python3`
  - Can be fixed with `apt install python-is-python3`
- `Downloaded X%` messages flash too quickly, should only update once a second or so
- Image downloading could probably be parallelized
