# Summer1400-Front-End-Contest
مسابقه فرانت اند تابستان 1400 کداستار

## ffmpeg
#### Speed Up The Video
`ffmpeg -i original.mp4 -filter:v "setpts=0.1*PTS" timelapse.mp4`

#### Make Color Palette
`ffmpeg -i frame.jpg -vf palettegen=16 palette.png`

#### Convert to GIF
`ffmpeg -i original.mp4 -i palette.png -filter_complex "fps=15,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse" result.gif`
