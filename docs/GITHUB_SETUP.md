# Publishing the CAPC Simulator on GitHub

This checklist is intended for publishing the Chapter 5 implementation repository without accidentally presenting development evidence as final thesis results.

## 1. Recommended repository name

A clear public name is:

```text
capc-simulator
```

or, if you want the thesis context visible:

```text
capc-blockchain-iot-simulator
```

## 2. Before the first push

Review these files:

- `README.md`
- `CITATION.cff`
- `LICENSE-NOTICE.md`
- `configs/dev.yaml`
- `configs/primary_template.yaml`

Do **not** replace the `null` CAPC values in `primary_template.yaml` with development values unless the Chapter 4 parameter-freezing decision has been completed and documented.

## 3. Create the Git repository locally

From the `capc-sim` directory:

```bash
git init
git add .
git commit -m "Initial CAPC simulator implementation"
```

## 4. Create an empty repository on GitHub

Create a new GitHub repository without automatically adding another README, `.gitignore`, or licence, because these files already exist in the project.

## 5. Connect and push

GitHub will provide commands similar to:

```bash
git branch -M main
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
```

## 6. Verify the published repository

After pushing:

1. confirm that `README.md` renders correctly;
2. confirm that the Mermaid architecture diagram renders;
3. confirm that `docs/COMPONENTS.md` is accessible;
4. confirm that `.github/workflows/tests.yml` appears under Actions;
5. run the test workflow;
6. verify that no local virtual environment, temporary result directory, or private file was committed.

## 7. Recommended first release strategy

Do not create a thesis-result release before the primary parameter set, source revision, configuration hash, seed list, and experiment outputs are frozen.

A reasonable sequence is:

- development repository / main branch;
- verified implementation commit;
- frozen primary-configuration commit;
- experiment execution tag;
- final thesis artefact release after analysis is complete.

## 8. Research-integrity rule

The README intentionally labels the included V1-V12 output as **implementation verification**, not performance evidence. Preserve that distinction when adding future figures or result tables.
