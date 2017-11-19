### Memo app
A simple app to take notes of a meeting

### Features
1. Write notes in textual form
2. Attach images to a note
3. Add attendees
4. Add meeting date
5. Search/filter for notes

### Architecture/Code organization
All of the backend code goes into the `src/` folder.
`views.py` contains all APIs that interact with the front-end
`utils/` contain search and S3 interaction utilities
`models.py` contains the data models

#### How are the notes/images stored?
The images are uploaded to S3 and the S3 path is stored in the database.

Note content is stored as plain-text in the database(TODO: Maybe move this to S3 as well and encrypt it)

#### TL;DR on data models please?
The app has two tables:
1. `Memo` - this table stores info about the memo/note itself along with other associated attributes.
2. `Users` - this table stores the list of attendees. This table is basic and only has `name` attribute - can grow based on future needs

`Memo` and `Users` table have a `ManyToMany` relationship - a meeting can be attended by multiple users and 
multiple meetings can be attended by the same user

#### How does search work?
Text search is based on a Trie. Each word in each note is processed and stored in an in-memory trie and when a 
particular word is searched for, the trie is traversed to figure out all notes containing that word.

##### Why a Trie?
I could've used a library like `Whoosh`, but I wanted to try implement my own search since I've never done that so far.
Plus, I didn't want this project to be a stringing of various libraries.

##### More trivia on search implementation
The Trie is maintained in-memory for each server process or thread, and whenever a new note is created OR a search is performed,
I check to make sure if all notes are indexed or not and if a note is not indexed, it is indexed and updated in the in-memory Trie.

For demonstration purposes, each server process/thread will have its own in-memory Trie. In practice, there should probably be a separate 
search worker that writes the intermediate representation of Trie to disk as and when each node is created.

#### Why does my JS look like sphagetti?
Oh four reasons:
1. I should've used React or any other single page app framework because this app naturally lends itself to be a single page app
2. I suck at UI
3. I'm lazy and didn't want to setup a single page app for a weekend project

(Did I say four reasons? Did I also say I'm lazy?)
