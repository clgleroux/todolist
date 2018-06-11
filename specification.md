# Spécification d'application

## Description

Notre application nous permettra de gérer des taches a effectuer avec une liste qui regroupera toute nos taches et un statut qui définira où en sont les taches (new / pending / done). Toutes les taches pourront être listé et supprimer si nécessaire.

Se type de service est connu sous le nom de todo list, exemple :
[Google Keep](https://keep.google.com/u/0/)

## Diagramme d'interaction

### Connexion

```
________                          _______________                             _______
| User |                          | Application |                             | BDD |
|______|                          |_____________|                             |_____|
   |                                     |                                       |
   |------------------------------------>|                                       |
   |  se connect à l'url home            |                                       |
   |                                     |-------------------------------------->|
   |                                     | Récupère les taches en BDD            |
   |                                     |                                       |
   |                                     |<--------------------------------------|
   |                                     | Retourne les taches du user           |
   |<------------------------------------|                                       |
   | Affiche home avec toutes les taches |                                       |
   |                                     |                                       |
```

### Ajouter une tache

```
________                          _______________                             _______
| User |                          | Application |                             | BDD |
|______|                          |_____________|                             |_____|
   |                                     |                                       |
   |------------------------------------>|                                       |
   |  se connect à l’URL du formulaire   |                                       |
   |                                     |                                       |
   |<------------------------------------|                                       |
   |  Retourne le formulaire de création |                                       |
   |                                     |                                       |
   |------------------------------------>|                                       |
   | Renseigne et renvoie le formulaire  |                                       |
   |                                     |-------------------------------------->|
   |                                     | Enregistrer la tache en BDD           |
   |                                     |                                       |
   |<------------------------------------|                                       |
   | Redirige vers la vue en liste       |                                       |
   |                                     |                                       |
```

### Supprimer une tache

```
________                          _______________                             _______
| User |                          | Application |                             | BDD |
|______|                          |_____________|                             |_____|
   |                                     |                                       |
   |------------------------------------>|                                       |
   |  se connect à l’URL de la liste     |                                       |
   |                                     |                                       |
   |<------------------------------------|                                       |
   |Retourne la liste des taches         |                                       |
   |                                     |                                       |
   |------------------------------------>|                                       |
   | click sur un bouton supprimer       |                                       |
   |                                     |-------------------------------------->|
   |                                     | Supprimer l'enregistrement en BDD     |
   |                                     |                                       |
   |<------------------------------------|                                       |
   | Redirige vers la vue en list        |                                       |
   |                                     |                                       |
```

### Attribuer un statu pour une tache

```
________                          _______________                             _______
| User |                          | Application |                             | BDD |
|______|                          |_____________|                             |_____|
   |                                     |                                       |
   |------------------------------------>|                                       |
   |  se connect à l’URL de la liste     |                                       |
   |                                     |                                       |
   |<------------------------------------|                                       |
   |Retourne la liste des taches         |                                       |
   |                                     |                                       |
   |------------------------------------>|                                       |
   | Change le status (mene deroulant)   |                                       |
   | et click sur le bouton update status|                                       |
   |                                     |-------------------------------------->|
   |                                     | Mettre a jour le status en BDD        |
   |                                     |                                       |
   |<------------------------------------|                                       |
   | Redirige vers la vue en liste       |                                       |
   |                                     |                                       |
```

## Définition de classes

Définir les models de données avec leur champs et attributs, ainsi qu’éventuellement leurs méthodes

Classe : Task

Attributs:

- Description : textField [maxLength = 240]
- status : choiceField [new / pending / done, default="new"]

L'ensemble des methode necessaire seront gerer par l'ORM de django.


## Points d'entrée de l'application (endpoints)

Définir les points d'entrées de l'application :

### Afficher page d'accueil (toutes les taches)

HTTP Verb : GET
Endpoint : `/`

### Création d'une nouvelle tache

- HTTP Verb : POST
- Endpoint : `/new`
- Payload parameter :
	- tasks:String

### Suppression d'une tache

- HTTP Verb : DELETE
- Endpoint : `/delete`
- Playload parameter :
    - id:Number

### Changement de status d'une tache

- HTTP Verb : PUT
- Endpoint : `/update`
- Playload parameter :
    - id:Number
    - string: status
