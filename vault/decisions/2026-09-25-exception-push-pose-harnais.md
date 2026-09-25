---
date: 2026-09-25
tags: [decision, harnais, exception]
---
# Exception unique au hook pre-push : publication de la pose du harnais (25/09, 20:37)

Le commit `343e839` (« chore(harnais): pose du harnais v1.0.0 [M0095] ») a été refusé par le hook `pre-push` que la pose venait
d'activer (sur `main`, seuls passent `vault/` seul ou un merge couvert par une revue GO). Décision de Malik : il l'a poussé lui-même
avec `--no-verify`, une seule fois. Raison : copie conforme du harnais v1.0.0 déjà promu et revu, aucun code écrit.
Cause : le mandat M0095 (orchestration) n'avait pas prévu que la pose active le hook avant son propre push — erreur de l'orchestrateur.
À partir de maintenant, la règle s'applique sans exception.
Visibilité du dépôt GitHub : **public, choix explicite de Malik** (25/09 20:39 : « c'est de la recherche, je laisse ouvert »). Il avait été passé en privé par erreur à 20:37 sur alerte de l'orchestrateur, puis remis en public.
