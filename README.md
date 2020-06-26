# flux-projects
A Discord bot to store, manage and interact with Flux official and volunteer projects. *Including some scope creep*
This bot is the successor of [KipCrossing/Flux-Project-Manager](https://github.com/KipCrossing/Flux-Project-Manager).

## Features

- Create a Flux project. `new`
  * The creator of the project is set as the lead of the project.
  * Users with the 'Flux Vetted' role will be prompted whether the project they're creating is Flux Official or Flux Volunteer based.
- Recall brief project information. (by project ID) `info`
  * The author can react for 1 minute after being sent the project information to recieve detailed information privately.
- Mass list projects. `filter`
  * Sorted by project status. (Active, closed, etc.)
  * Variable levels of detail for each project.
- Create a DigiPol issue `issue`
  * Users with the 'App Issue Creator' role are able to create an issue to be listed in the DigiPol by Flux app.

### Planned features
- Edit projects.
- Easily update project status.
- *(See issues tab)*

## Commands

| Command | Usage | Purpose | Permissions |
|--|--|--|--|
| help | help [command] | Display information about all commands in Discord. Optionally display help about a specific command. |  Everyone  |
| new | new | Create a new project. You will be privately prompted to answer questions. | Flux Vetted |
| info | info [id] | Recall brief information about a particular project. | Everyone |
| filter | filter [status] [detail] | Recall information about all projects with a specific status. | Server Admin |
| issue | issue | Create an issue for the DigiPol app. You will be privately prompted to answer questions. | App Issue Creator |

# *Below coming soon*

## Contributing

## Setup guide to run the bot

### Prequisited software

### Database structure

### Steps