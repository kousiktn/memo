### Memo app

A simple app to take notes of a meeting

----

### Features
1. Write notes in textual form
2. Add meeting date
----

### Architecture/Code organization
All of the backend code goes into the `src/` folder.
`views.py` contains all APIs that interact with the front-end
`utils/` contain search and S3 interaction utilities
`models.py` contains the data models

All `notes` are stored as blobs on S3 bucket. This app does not use any relational database. It also doesn't have the concept of users(for now)
----

#### Why does my JS look like sphagetti?
Oh four reasons:
1. I should've used React or any other single page app framework because this app naturally lends itself to be a single page app
2. I suck at UI
3. I'm lazy and didn't want to setup a single page app for a weekend project

(Did I say four reasons? Did I also say I'm lazy?)
----

### Deploy(just so I don't forget)
I use `Zappa` to deploy the code to AWS lambda + API gateway

#### Deploy commands
`zappa deploy dev` - deploys to dev environment
`zappa update dev` - update the dev environment with latest version of code
`zappa certify` - (rarely used) use to certify my new domain name
