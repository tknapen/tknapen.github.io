# Knapen lab website

Based on the folio theme.

To work on the webpage: checkout the 'content' branch when you want to edit things. This 'content' branch is the development branch of the website. Change stuff there, and only when you git merge content while in master, will the changes affect the website after a push.

So, that is:

```git

git checkout content 

make your changes

git add .
git commit -am 'a message saying what I just changed'

git checkout master
git merge content

git push

```

and wrinse and repeat.