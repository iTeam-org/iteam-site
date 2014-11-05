---
title: "Projet informatique de deuxième année"
subtitle: "Logiciel de dessin vectoriel"
author: "Adrien \\bsc{Chardon}, Joris \\bsc{Gahéry} (TD01)"
date: "Octobre 2014"
geometry: margin=3.5cm
---


# Introduction et cahier des charges

## Rappel du sujet

Le but de ce projet est que chaque groupe d’étudiants développe, en langage C et à l’aide de la bibliothèque Allegro, un logiciel de dessin vectoriel, tout en respectant un cahier des charges proposé par M. \bsc{Fercoq}.

Voici les principales caractéristiques du cahier des charges :

- Le logiciel doit pouvoir afficher des polygones tracés
- Une palette de couleurs permet de colorier les polygones
- Les polygones peuvent être déplacés
- Un presse-papiers permet de dupliquer les polygones
- Les polygones peuvent être gérés sous forme de groupes
- Les polygones peuvent être sauvegardés et chargés vers et depuis un fichier
- Les polygones peuvent être supprimés

## Groupe

Nous sommes un groupe de deux ING2.

Adrien Chardon était en ING1 à l’ECE l’année dernière. Brillant en informatique, il maîtrise différents langages comme le C, le Python, ou le HTML5.

Joris Gahéry est un ING2 Nouveau, il a commencé le langage C en début d’année lors de la pré-rentrée avec M. \bsc{Fauberteau}. Il dispose de quelques notions en Python acquises en classe préparatoire.

## Organisation du groupe

Étant d’un meilleur niveau en informatique que Joris, Adrien a pris le poste de chef de projet ;  Bien qu’un projet de cette envergure puisse se passer de hiérarchie clairement définie.

L’avancement des TP s’est déroulé de manière atypique du fait de l’extrême diversité des deux profils : Adrien avait déjà les idées pour finaliser le programme alors que Joris n’avait jamais vraiment codé.
De ce fait, nous avons décidé, dans un premier temps de laisser Joris avancer seul le projet. Ce choix, décidé par lui-même, afin de se mettre dans la difficulté dès le début pour acquérir le plus rapidement possible les compétences nécessaires pour rattraper le niveau des ING2. Adrien, par ses capacités, servi de soutien à Joris pour lui permettre de dépasser les difficultés lorsque celui-ci n’arrivait pas à réaliser certaines choses. De cette manière, toutes les techniques de programmation et de résolution de bugs ont été assimilées de manière optimale par Joris.

Une fois les TP1 et TP2 finalisé par Joris, nous avons décidé de désormais coder ensemble.
Joris n’arrivant pas à réellement comprendre comment il allait réaliser le TP3, Adrien reprit en main le projet et envoya à Joris toutes les instructions pour qu’il travaille en sachant quoi faire. Pendant ce temps là, Adrien coda les fonctions compliquées. C’est ainsi que ce groupe a atteint la majorité des objectifs du cahier des charges.

En conclusion, le TP1 et le TP2 ont été codé par Joris avec l’aide précieuse d’Adrien, le TP3 a été codé en collaboration par Adrien et Joris. Le TP4 a été entièrement codé par Adrien.

# Partie conception
## Organisation de l’équipe et planning

Le cahier des charges du projet était découpé en quatre TPs. Joris a commencé à travailler sur les deux premiers TPs, plus faciles, puis Adrien a intégré les fonctionalités les plus complexes. Chaque TP a mené à la création d’un ou plusieurs modules, afin d’offrir un niveau d’abstraction pour isoler chaque module et faciliter le développement des fonctionnalités futures.

- TP1 : Mise en place d’une ébauche fonctionelle : possibilité de dessiner un segment puis un polygone et gestion de la sauvegarde et du chargement. Les modules Primitive et Dessin on été créés.
- TP2 : gestion de la couleur et ébauche du mode édition (choix de la couleur des polygones). Le module Editeur a été créé, et beaucoup de code a été réécris.
- TP3 : gestion de la sélection, menu d’aide et copier coller (déplacement). Le module Cadre a été créé.
- TP4 : gestion du recoloriage des primitives déjà dessinées et zoom pour un travail plus précis. Le module Group a été créé.


## Modèle et contrôleur des parties clefs du projet

### Modèles

**Objet  Primitive :**

- t_point *tab : coordonnées des sommets
- int nb\_points\_alloues : nombre de points alloués en mémoire
- int nb\_points\_actifs : nombre de points utilisés
- int color : couleur du polygone

**Objet  Editeur :**

- t_dessin *dessin : primitives enregistrées
- t_primitive current : primitive en train d’être dessinée
- t_cadre cadre : cadre de séléction
- t_group *selected :  primitives sélectionnées
- t_point mouseRel : déplacement relatif de la souris
- int action_state : status du cadre ou du dessin (en attente ou actif)
- int drawing_mode : mode (ajout ou édition)
- double zoom : zoom
- t_vector offset : décalage
- t_point mousePosPxl : coordonnées de la souris dans un repère associé à la fenêtre
- t_vector mousePosCoord : coordonnées de la souris dans un repère absolu


### Contrôleur : analyse chronologique descendante

1. Événements
    1. Clavier et souris
    1. Zoom
    1. Palette
    1. Sauvegarder et charger
    1. Mode ajout
        1. Clic gauche
        1. Clic droit
    1. Mode édition
        1. Sélection
        1. Translater
        1. Duppliquer
        1. Recolorier
    1. Afficher l’aide
1. Affichages
    1. Dessiner les primitives du dessin
    1. Dessiner la primitive en cours d’ajout
    1. Dessiner le cadre
    1. Dessiner la palette


## Présentation des modules et de leurs entrées-sorties

Tous les modules présentent des fonctions abstraites pour faciliter l’utilisation des instances : création (allocation et initialisation), suppression, sauvegarde, chargement et affichage. En fonction de l’utilité du module, ce dernier peut proposer d’autres fonctions, détaillées ci-dessous. Les fonctions utilisent une instance de l’objet  Editeur (détaillé un peu plus haut) pour communiquer.

- **Primitive :** module de base du projet
    - `primitive_is_in_cadre()` : indique si la primitive est dans le cadre de sélection.

- **Dessin :** rassemble l'ensemble des primitives dessinées
    - `dessin_ajout_primitive()` : ajoute une primitive au dessin.

- **Editeur :** gestion des fonctionnalités (mode dessin / édition, couleur, sauvegarde, chargement)
    - `editeur_update_souris_zoom()` : mise à jour du zoom.
    - `editeur_gestion_gauche()` et `editeur_gestion_droit()` : gestion des clic gauche et droit.
    - `editeur_mode_manip()` et `editeur_mode_ajout()` : gestion des modes ajout et édition.

- **Cadre :** gestion de la sélection
    - `cadre_add_to_selection()` : ajoute un objet a la sélection.
    - `cadre_unselect()` : retire tous les objets de la sélection.

- **Group :** structure en arbre pour stocker les primitives du dessin de manière plus optimisée
    - `group_add_form()` : ajoute une primitive à un groupe.
    - `dessin_translater()` : déplace toutes la primitives du groupe d'un décalage donné.
    - `group_recolor()` : recolorise toutes les primitives du groupe.

- **Compalleg et Pallette :** surcouche allegro et gestion des couleurs, dévelopés par M. \bsc{Fercoq}

# Partie réalisation
## Choix de programmation

Le choix de programmation s’oriente sur un nombre de modules importants afin de modulariser au maximum le code. Ainsi, la fonction `main()` fait seulement appel à des fonctions développées dans les modules. De plus, nous avons créé un certain nombre de structures afin d’abstraire au maximum les variables et le fonctionnement interne du logiciel. Cela a parfois pour effet de complexifier certains traitements mais nous permet en revanche de mieux isoler chaque fonctionnalité.

**Stockage des primitives :**

Nous avons commencé par un tableau de pointeurs, afin d’avoir rapidement une ébauche fonctionnelle. À la fin du projet, un stockage en arbre a été utilisé afin de faciliter la sélection et d’optimiser l’utilisation de la mémoire.

## Astuces et autres originalités

Nous avons réalisé un zoom qui, comme son nom l’indique, permet d’afficher avec plus de précisions les polygones. De par le cahier des charges du projet (logiciel de dessin vectoriel), le zoom n’engendre pas de pixellisation.

## Protocole de test

À chaque ajout d’un module ou d’une fonctionnalité, des tests étaient lancés pour vérifier le respect du cahier des charges de ce module ou cette fonctionnalité ainsi que l’abscence d’introduction de bugs. A quelques jours du rendu, de nombreux tests ont été lancés afin de vérifier le respect global du cahier des charges.

Ces tests ont permis de pointer plusieurs bugs, comme par exemple pour la sélection : celle-ci n'était possible qu'en partant du coin supérieur-gauche. Apres investigation, il s'est avéré que le problème provenait de la fonction qui déterminait si une primitive était dans le cadre.


## Bilan collectif et individuel

### Bilan de Joris
Je suis très heureux d’avoir participé à ce projet, les connaissances que j’ai accumulées durant cette période me permettent de désormais me sentir plus à l’aise avec le C. Adrien a été indispensable à mon évolution, sans son extrême connaissance dans le domaine, je n’aurais pas eu l’opportunité d’évoluer comme je l’ai fait.

### Bilan d’Adrien
Bien que les niveau en programmation de Joris et moi même ne soient pas très homogènes, ce projet s’est très bien déroulé, particulièrement pour la répartition du travail qui a permis à chacun de progresser en travaillant sur des problématiques adaptées a son niveau.

### Bilan collectif
Une grande satisfaction d’avoir réussi à bien travailler ensemble, notre log SVN témoigne de notre grande solidarité et collaboration. Malgré les différences de niveau, la logique de groupe a pris le pas et cela nous a permis de travailler en confiance.
L’esprit d’équipe s’étant extrêmement bien développé, nous souhaiterons nous remettre ensemble pour le prochain TP d’informatique.
Notre plus grande déception est de ne pas avoir eu le temps de compléter tous les objectifs du cahier des charges et principalement le group/ungroup

