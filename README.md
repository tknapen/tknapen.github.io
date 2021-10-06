# Knapen lab website

Based on the folio theme.


## Environment

This is a jekyll website, so when working on changes you can 'host' the website on your own computer by installing and running jekyll. See instructions [here](https://jekyllrb.com)


## To Edit:

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

## For creating movies that work in the webpage

This assumes you have a bunch of .png files that are, for instance, screenshots of a brain viewer, and that next to the folder containing these .png files, there exist folders named _bg_ and _cropped_ for subsequent processing steps.

```
for s in *
do
convert -background "rgb(225,225,225)" -flatten ../cropped/$s ../bg/$s &
done


cd ../bg

for s in *
do
convert -crop 800x600+560+200 $s ../cropped/$s &
done

```
_________________________

```
cd ../cropped

ffmpeg -y -framerate 30 -pattern_type glob -i "*.png" -b:v 4M -c:v libx264 -pix_fmt yuv420p -profile:v baseline ../rotate_avs.mp4
ffmpeg -y -framerate 30 -pattern_type glob -i "*.png" -b:v 4M -c:v libtheora ../rotate_avs.ogv
ffmpeg -y -framerate 30 -pattern_type glob -i "*.png" -b:v 4M -c:v libvpx-vp9 ../rotate_avs.webm
```

