from PIL import Image

im = Image.open('animation.gif')
num_key_frames = im.n_frames
print(num_key_frames)

for i in range(num_key_frames):
    im.seek(i)
    im.save('frame{}.png'.format(i + 5))
