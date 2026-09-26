"""Mutations de la Mission 1 : python3 tests/mutations.py <dossier scratch> <chemin absolu de research/>.

Copie oracle/ dans un arbre miroir (A0, A0bis, experiments en liens), injecte chaque mutation une à une,
relance la suite et dit si elle échoue (DÉTECTÉE). Rien n'est écrit dans le dépôt.
"""
import os, shutil, subprocess, sys
S, W = sys.argv[1], sys.argv[2]
MUT = [
 ("M1 K_f créée au début du monde", "acquereur_oracle.py",
  "        if not self.connaissances:\n            return\n        m = _monde(vue)",
  "        m0 = _monde(vue)\n        self.connaissances.setdefault(m0['famille'], connaissance(m0))\n        if not self.connaissances:\n            return\n        m = _monde(vue)"),
 ("M2 amnésique garde la mémoire a0bis", "acquereur_oracle.py",
  "            self.memoire = memoire_initiale()\n", ""),
 ("M3 amnésique garde K_f", "acquereur_oracle.py",
  "            self.connaissances = {}\n", ""),
 ("M4 pas de bijection (identité)", "acquereur_oracle.py",
  "    perm = meilleur[1]", "    perm = tuple(rels)"),
 ("M5 acquéreur applique la vérité courante", "acquereur_oracle.py",
  "self.regles_oracle = vraies if self.EXACT else", "self.regles_oracle = vraies if True else"),
 ("M6 compositions ignorées dans σ", "acquereur_oracle.py",
  "POIDS_COMPOSITION = 4", "POIDS_COMPOSITION = 0"),
 ("M7 règles oracle non utilisées (tests d'A0-bis)", "acquereur_oracle.py",
  "        if self.regles_oracle is None:\n            return super()._etape_regles()",
  "        if True:\n            return super()._etape_regles()"),
 ("M8 seuil amnésique ≥ 1", "evaluer_oracle.py", "permissif = n_amn >= 2", "permissif = n_amn >= 1"),
 ("M9 K_f garde les noms", "acquereur_oracle.py",
  "    vecs = [[int(monde[\"proprietes\"][r][p]) for p in PROPRIETES] for r in rels]",
  "    vecs = [[r] + [int(monde[\"proprietes\"][r][p]) for p in PROPRIETES] for r in rels]"),
 ("M10 relance sans PYTHONHASHSEED=0", "evaluer_oracle.py",
  "    if os.environ.get(\"PYTHONHASHSEED\") != \"0\":", "    if False:"),
 ("M11 seuil acquéreur ≥ 2", "evaluer_oracle.py", "atteignable = n_acq >= 3", "atteignable = n_acq >= 2"),
]
base = os.path.join(S, "research")
if os.path.exists(base): shutil.rmtree(base)
os.makedirs(os.path.join(base, "candidats", "A0ter"))
os.symlink(os.path.join(W, "experiments"), os.path.join(base, "experiments"))
for d in ("A0", "A0bis"): os.symlink(os.path.join(W, "candidats", d), os.path.join(base, "candidats", d))
src = os.path.join(W, "candidats", "A0ter", "oracle"); dst = os.path.join(base, "candidats", "A0ter", "oracle")
for nom, f, a, b in MUT:
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("results", "__pycache__"))
    p = os.path.join(dst, f); t = open(p).read()
    assert t.count(a) == 1, (nom, t.count(a))
    open(p, "w").write(t.replace(a, b))
    r = subprocess.run([sys.executable, "-m", "unittest", "discover"], cwd=dst, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONHASHSEED="0"))
    last = [l for l in r.stderr.splitlines() if l.startswith(("FAILED", "OK", "Ran"))]
    echecs = sorted({l.split("(")[0].split()[-1] for l in r.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))})
    print("%-50s %s %s" % (nom, "DÉTECTÉE" if r.returncode else "NON DÉTECTÉE", " ".join(last[-1:]) + " " + ",".join(echecs)))
