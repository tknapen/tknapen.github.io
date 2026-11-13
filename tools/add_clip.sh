#!/usr/bin/env bash
# Prepare an animation for the website: a web-ready MP4 and a poster image in assets/clips/.
#
#   tools/add_clip.sh <input video> <id> [--dark] [--poster-at SECONDS] [--width PIXELS]
#
#   <id>         short name used on the site, e.g. prf-fit  ->  assets/clips/prf-fit.mp4 and prf-fit.webp
#   --dark       the input is the dark-background render of an existing clip: it goes to
#                assets/clips/dark/<id>.mp4 and is shown automatically to visitors in dark mode
#   --poster-at  time of the still shown before the clip plays (default: the last frame, the finished picture)
#   --width      maximum width in pixels (default 1280)
#
# The MP4 is H.264 without sound, with the index at the front so it starts playing while it loads.
# Needs ffmpeg with libx264 and libwebp. Prints the entry to add to _data/clips.yml (light renders only).
set -euo pipefail

usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[ $# -ge 2 ] || usage
in=$1; id=$2; shift 2
dark=0; poster_at=""; width=1280
while [ $# -gt 0 ]; do
  case $1 in
    --dark) dark=1 ;;
    --poster-at) poster_at=$2; shift ;;
    --width) width=$2; shift ;;
    *) usage ;;
  esac
  shift
done
[ -f "$in" ] || { echo "no such file: $in" >&2; exit 1; }
case $id in *[!a-z0-9-]*|"") echo "id must be lower-case letters, digits and hyphens: $id" >&2; exit 1 ;; esac

root=$(cd "$(dirname "$0")/.." && pwd)
dir=$root/assets/clips; [ $dark -eq 1 ] && dir=$dir/dark
mkdir -p "$dir"
out=$dir/$id.mp4; poster=$dir/$id.webp

# never upscale; even dimensions for H.264
scale="scale='min($width,iw)':-2:flags=lanczos,scale=trunc(iw/2)*2:trunc(ih/2)*2"
ffmpeg -v error -y -i "$in" -an -vf "$scale" -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -preset slow -crf 23 -movflags +faststart "$out"

if [ -n "$poster_at" ]; then
  ffmpeg -v error -y -ss "$poster_at" -i "$out" -frames:v 1 -c:v libwebp -quality 88 "$poster"
else
  ffmpeg -v error -y -sseof -0.2 -i "$out" -update 1 -frames:v 1 -c:v libwebp -quality 88 "$poster"
fi

read -r w h dur < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration -of csv=p=0 "$out" | tr ',\n' '  '; echo)
printf 'wrote %s (%s bytes) and %s\n' "${out#$root/}" "$(stat -c %s "$out" 2>/dev/null || stat -f %z "$out")" "${poster#$root/}"
if [ $dark -eq 0 ]; then
  cat <<YAML

Add to _data/clips.yml:

- id: $id
  title: ""
  caption: ""
  width: $w
  height: $h
  seconds: $(printf '%.0f' "$dur")
YAML
fi
