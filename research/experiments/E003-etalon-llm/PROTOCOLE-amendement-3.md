# E003 — Amendement 3 (26/09) : fournisseur imposé et journalisé, arrêt net sur 402

Mandat M0019. Committé et poussé **avant** tout commit de code, et avant tout appel fait sous
cet amendement. `PROTOCOLE.md` n'est pas modifié. `cases.json`, le prompt, les modèles, les
réglages (Amendements 1 et 2), le parse strict et la règle conforme / faux et sûr sont
**inchangés**.

## Défaut constaté

- [VÉRIFIÉ] `run_llm.py` (tip `bbc50ae`) n'envoie aucun `providerOptions`. La passerelle Vercel
  AI Gateway choisit donc le fournisseur (backend) appel par appel, selon sa disponibilité et sa
  latence.
- [VÉRIFIÉ] Le journal de la passerelle montre que `google/gemini-2.5-flash` a été servi au moins
  en partie par Google Vertex AI.
- [VÉRIFIÉ] `filter_response` ne garde pas le champ fournisseur de la réponse : aucun des 12
  `raw.public.jsonl` publiés ne dit quel backend a répondu.
- Conséquence : dans les mesures M0006 à M0010, le backend est une **variable non contrôlée**.
  Pour un étalon de comparaison, deux vagues servies par deux backends différents ne sont pas
  comparables avec certitude.

## Changements

1. **Fournisseur imposé par modèle** (liste `only` de la passerelle, champ
   `providerOptions.gateway.only` du corps de `/v1/chat/completions`, doc Vercel lue le 26/09) :

   | modèle | fournisseurs autorisés |
   |---|---|
   | `openai/gpt-4.1-mini` (LLM-1) | `["openai"]` |
   | `google/gemini-2.5-flash` (LLM-2) | `["vertex"]` (Google Vertex AI) |

   Un modèle sans entrée dans cette table est refusé **avant tout appel** (pas de repli sur le
   choix de la passerelle). Un pilote `--pilot-model` sur un autre modèle exige donc d'abord un
   nouvel amendement.
2. **Fournisseur réel journalisé** : de la réponse HTTP 200, le champ `provider` (premier niveau
   du corps) est gardé dans `response`, `null` s'il est absent.
   [HYPOTHÈSE] Le nom et l'emplacement de ce champ ne sont pas garantis par la doc lue ; ils
   seront vérifiés au premier appel réel (M0021). S'il est toujours `null`, le fournisseur réel
   reste non journalisé et cela sera écrit au README.
3. **HTTP 402 = arrêt** : un budget de dépense est posé sur la passerelle ; au dépassement, elle
   répond 402 `quota_for_entity_exceeded`. Un 402 n'est **jamais** relancé : le lancement
   s'arrête sur-le-champ (aucun appel suivant), ce qui est acquis est écrit, et le script sort
   avec un code distinct (documenté dans le README).

## Conséquence sur les résultats existants

- Les réponses M0006–M0010 restent valides **comme réponses observées** : chiffres inchangés.
- Leur comparabilité entre vagues (M0008, M0010) et avec une vague future n'est pas garantie :
  le backend est inconnu. La ligne « LLM-1 faux et sûr sur T1-A `e_sup_d` » est qualifiée
  « backend non contrôlé, à rejouer (M0021) ».
- Rejeu sous cet amendement : mandat séparé (M0021). Aucun appel dans M0019.
