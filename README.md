# ALGTankGame
Tank Game for Spring 2024, CSET3150:001 Introduction to Algorithms

### Here is how to download your branch onto your computer using CLI commands
`git clone -b noah https://github.com/bunnycou/ALGTankGame`

Replace noah with your own name (collin, robby, xander)

Basic CLI git commands for updating your branch

This will add all files in the directory to be tracked in github
`git add .`

This will commit all changes and add a message, typically used to describe what changed.
`git commit -m "Updated files"`

This will push your changes to your branch, origin is the repository, name is your name/name of the branch
`git push origin name` or for example `git push origin noah` is what I would do

This will download your changes in case you work on multiple devices
`git pull origin name`

To get the latest changes from the main branch do
`git rebase master`
This will attempt to apply your commits on top of the latest main commit
