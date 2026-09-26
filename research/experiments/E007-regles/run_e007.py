#!/usr/bin/env python3
"""E007 -- appels rythmes a Jev : run_paced.py d'E006 importe tel quel (non modifie, non duplique).

Seuls changent : l'ordre des groupes (D, C, A, B -- fixe avant tout appel), le corpus, le dossier
de resultats et le budget dur (100 appels). Garde-fous herites de run_paced : intervalle >= 26 s
entre departs (y compris entre invocations ; le mandat exige >= 15 s), <= 8 appels par invocation
(mandat : <= 10), arret sur 401/403/404 (code 4) ou 3 echecs consecutifs, garde anti-fuite.

  python3 run_e007.py            # a relancer jusqu'au code 5 (« rien a faire »)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "E006-replication-frontiere"))
import run_paced  # noqa: E402

ORDRE_GROUPES = "DCAB"
BUDGET = 100


def main(argv=None, **kw):
    run_paced.ORDRE_GROUPES = ORDRE_GROUPES
    argv = list(sys.argv[1:] if argv is None else argv)
    base = ["--cases", str(HERE / "cases.json"), "--results", str(HERE / "results"),
            "--budget", str(BUDGET)]
    if "--budget" in argv and int(argv[argv.index("--budget") + 1]) > BUDGET:
        print("--budget > {} refuse".format(BUDGET), file=sys.stderr)
        return 2
    return run_paced.main(base + argv, **kw)  # argparse : la derniere occurrence l'emporte


if __name__ == "__main__":
    sys.exit(main())
