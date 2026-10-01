# Scissor Boom Deployment Model

Senior Design models for a scissor boom deployed by hinge springs and an
inflatable kink tube. Python models, the derivation they implement, and the
supporting studies.

## Layout

| Path | Contents |
|---|---|
| `src/` | Core model and analysis scripts (run from inside `src/`) |
| `derivation/` | LaTeX derivation (`main.tex`, PDF) that the code implements |
| `studies/deployment_time/` | Quasi-static / deployment-time study, with report |
| `studies/friction_table/` | Friction budget script and tables (long and short) |
| `notes/` | Loose design notes |
| `archive/` | Superseded early models, kept for reference |

### `src/`

- `params.py`: all design parameters. Set `USE_TESTING_PARAMS` to switch
  between the production design and the bench-test values in `testingParams.py`.
- `Phase1.py`: hinge-spring-only deployment, stowed to the handoff angle theta_1.
- `Phase2.py`: spring plus inflatable kink, theta_1 to fully deployed.
- `solve_design.py`: runs Phase 1 then Phase 2 in one pass.
- `friction_sweep.py`: sweeps friction; writes `friction_sweep.csv`.
- `quasi_static_check.py`: checks the quasi-static assumption.
- `max_spring_force.py`, `spring_upper_bound.py`, `outward_force_envelope.py`: spring and force bounds.

## Usage

```
pip install numpy scipy matplotlib
cd src
python solve_design.py
```

Studies find `src/` on their own and can be run from anywhere:

```
python studies/deployment_time/deploy_time_study.py
python studies/friction_table/friction_budget.py
```

## Building the PDFs

Use `latexmk -pdf main.tex` (or the equivalent) in `derivation/` and in the
study folders. Build artifacts are git-ignored; the PDFs are committed.
