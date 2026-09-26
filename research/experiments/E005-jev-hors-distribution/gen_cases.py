#!/usr/bin/env python3
"""Genere cases.json (E005) -- corpus preenregistre, meme schema qu'E001. Stdlib."""
import json
from pathlib import Path

Q_GRAM = {"correcte": {"type": "boolean",
                       "instructions": "Cette phrase est-elle orthographiquement correcte en francais ?"}}
STATUT = {"type": "choice",
          "instructions": "En appliquant uniquement les faits et regles donnes, l'ensemble est-il contradictoire, coherent, ou indetermine faute de regle ?",
          "criteria": {"contradiction": "Une regle explicitement donnee est violee par des faits donnes ou deduits",
                       "coherent": "Aucune regle donnee n'est violee",
                       "indetermine": "Il manque une definition ou une regle pour trancher"}}
R1 = "Regle 1 : si X > Y et Y > Z alors X > Z."
R2 = "Regle 2 : si incompatible(X, Y) alors ni X > Y ni Y > X."
R3 = "Regle 3 : si couleur(X, bleu) alors X > D."


def gram(cid, fam, phrase, ok, why):
    return {"id": cid, "famille": fam,
            "state": "Phrase ecrite par un eleve : « {} »".format(phrase),
            "questions": Q_GRAM, "attendu": {"correcte": ok}, "justification": why}


def boolq(txt):
    return {"type": "boolean", "instructions": "Peut-on deduire {} uniquement a partir des faits et regles donnes ?".format(txt)}


F1, F2, F3 = "F1-accords-rares", "F2-homophones-rares", "F3-juste-atypique"
cases = [
    gram("F1-01", F1, "Les pommes qu'il a mangées étaient délicieuses.", True,
         "PP avec avoir, COD « qu' » (= les pommes) antéposé : accord fém. plur."),
    gram("F1-02", F1, "Les pommes qu'il a mangé étaient délicieuses.", False,
         "Même phrase sans l'accord exigé par le COD antéposé."),
    gram("F1-03", F1, "Elles se sont lavé les mains avant le repas.", True,
         "Pronominal : COD « les mains » postposé, « se » est COI : PP invariable."),
    gram("F1-04", F1, "Elles se sont lavées les mains avant le repas.", False,
         "Même phrase : l'accord avec « se » (COI) est fautif."),
    gram("F1-05", F1, "Ils se sont parlés pendant des heures.", False,
         "Parler à quelqu'un : « se » est COI, PP invariable (« se sont parlé »)."),
    gram("F1-06", F1, "Elles se sont succédé à la tribune.", True,
         "Succéder à quelqu'un : « se » est COI, PP invariable."),
    gram("F1-07", F1, "Les robes qu'elle a fait faire sont superbes.", True,
         "« fait » suivi d'un infinitif est toujours invariable."),
    gram("F1-08", F1, "Les robes qu'elle a faites faire sont superbes.", False,
         "« fait » + infinitif ne s'accorde jamais."),
    gram("F1-09", F1, "Les enfants que j'ai laissé partir sont rentrés.", True,
         "« laissé » + infinitif invariable (rectifications 1990) ; forme admise."),
    gram("F1-10", F1, "Les fortes chaleurs qu'il a faites cet été ont épuisé tout le monde.", False,
         "« il a fait » impersonnel : PP invariable (« qu'il a fait »)."),
    gram("F2-01", F2, "Quelle que soit ta décision, je te soutiendrai.", True,
         "« quel que » + être, « quel » accordé au sujet « décision »."),
    gram("F2-02", F2, "Quelque soit ta décision, je te soutiendrai.", False,
         "Devant le verbe être : « quel(le) que », jamais « quelque »."),
    gram("F2-03", F2, "Je ne sais pas qu'elle heure il est.", False,
         "Déterminant interrogatif « quelle » (heure), pas « qu'elle »."),
    gram("F2-04", F2, "Il est censé arriver à midi.", True,
         "« censé » = supposé, suivi d'un infinitif."),
    gram("F2-05", F2, "Il est sensé arriver à midi.", False,
         "« sensé » = raisonnable, ne prend pas d'infinitif ; ici « censé »."),
    gram("F2-06", F2, "Le train est près de partir.", True,
         "« être près de » + infinitif = être sur le point de."),
    gram("F2-07", F2, "Nous sommes près à partir.", False,
         "« prêt à » = disposé à ; ici « prêts à partir »."),
    gram("F2-08", F2, "Elle a appris à lire à son fils.", True,
         "Auxiliaire « a » puis deux prépositions « à »."),
    gram("F3-01", F3, "Ci-joint la facture demandée.", True,
         "« ci-joint » en tête de phrase devant le nom : invariable (juste mais sonne faux)."),
    gram("F3-02", F3, "Ci-jointe la facture demandée.", False,
         "Même position : l'accord de « ci-joint » est fautif (faute fluide)."),
    gram("F3-03", F3, "Elle porte des chaussures marron.", True,
         "Nom employé comme adjectif de couleur : invariable (juste mais sonne faux)."),
    gram("F3-04", F3, "Elle porte des chaussures marrons.", False,
         "« marron » adjectif de couleur est invariable (faute fluide)."),
    gram("F3-05", F3, "Elles se sont plu à Paris.", True,
         "« plu » (plaire) est invariable, même à la forme pronominale (juste mais sonne faux)."),
    gram("F3-06", F3, "Elles se sont plues à Paris.", False,
         "« se plaire » : PP invariable ; l'accord est fautif (faute fluide)."),
    {"id": "F4-01", "famille": "F4-logique-distracteurs",
     "state": "Faits : A > B. B > C. C > D. E > A. A > C. couleur(A, rouge). incompatible(D, E). {} {} {}".format(R1, R2, R3),
     "questions": {"statut": STATUT, "e_sup_d": boolq("E > D")},
     "attendu": {"statut": "contradiction", "e_sup_d": True},
     "justification": "T1-A + fait redondant (A > C) + regle 3 non pertinente (aucun bleu) : E > D deduit, R2 violee."},
    {"id": "F4-02", "famille": "F4-logique-distracteurs",
     "state": "Faits : A > B. B > C. C > D. E > A. A > C. couleur(A, rouge). incompatible(B, F). {} {} {}".format(R1, R2, R3),
     "questions": {"statut": STATUT, "e_sup_d": boolq("E > D")},
     "attendu": {"statut": "coherent", "e_sup_d": True},
     "justification": "Aucun fait ne relie B et F : R2 non violee, toutes regles definies ; E > A > C > D."},
    {"id": "F4-03", "famille": "F4-logique-distracteurs",
     "state": "Faits : A > B. B > C. C > D. E > A. A > C. couleur(A, rouge). incompatible(D, E). {} {} Aucune regle ne definit ce que signifie incompatible.".format(R1, R3),
     "questions": {"statut": STATUT, "e_sup_d": boolq("E > D")},
     "attendu": {"statut": "indetermine", "e_sup_d": True},
     "justification": "T1-B + distracteurs : incompatible non defini ; E > D deduit par R1."},
    {"id": "F4-04", "famille": "F4-logique-4-pas",
     "state": "Faits : D > E. A > B. E > F. C > D. B > C. incompatible(A, F). {} {}".format(R1, R2),
     "questions": {"statut": STATUT, "a_sup_f": boolq("A > F")},
     "attendu": {"statut": "contradiction", "a_sup_f": True},
     "justification": "Faits melanges ; A > C, A > D, A > E, A > F (4 pas R1) puis R2 violee."},
    {"id": "F4-05", "famille": "F4-logique-4-pas",
     "state": "Faits : D > E. A > B. E > F. D > C. B > C. incompatible(A, F). {} {}".format(R1, R2),
     "questions": {"statut": STATUT, "a_sup_f": boolq("A > F")},
     "attendu": {"statut": "coherent", "a_sup_f": False},
     "justification": "Variante de F4-04 avec D > C au lieu de C > D : aucun chemin de A a F, R2 non violee."},
    {"id": "F5-01", "famille": "F5-controle-trivial",
     "state": "Faits : X > Y. Y > Z. {}".format(R1),
     "questions": {"x_sup_z": boolq("X > Z"), "z_sup_x": boolq("Z > X")},
     "attendu": {"x_sup_z": True, "z_sup_x": False},
     "justification": "Transitivite en 1 pas (borne haute) ; l'inverse n'est pas deductible (borne basse)."},
    gram("F5-02", "F5-controle-trivial", "Le chat dort sur le canapé.", True,
         "Phrase simple sans difficulte."),
    gram("F5-03", "F5-controle-trivial", "Les chat dort sur le canapé.", False,
         "Determinant pluriel sur nom et verbe au singulier."),
]

doc = {"preregistre_le": "2026-09-26",
       "note": "E005 (M0009). Attentes fixees par la fenetre F05 AVANT tout appel, relues deux fois. "
               "Ne jamais modifier apres lancement : un ecart est un resultat. "
               "Consigne boolean identique a E001 ; format logique identique a T1.",
       "cases": cases}
Path(__file__).with_name("cases.json").write_text(
    json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(cases), "cas,", sum(len(c["questions"]) for c in cases), "questions")
