# branchProtectionSample
A simple web service that listens for organization events to know when a repository has been created.

This web service is intended to listen for a GitHub organization event triggered when a repository has been created and will trigger an api which does the following.
* Set protection of the master branch of that created repository.
* Create a issue in the created repository and notify me with an @mention.


