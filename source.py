#!/usr/bin/env python3

from multiprocessing import Pool
import os
from pathlib import Path

from PIL import Image, ImageDraw

from util import Vec2

BLACK = (0, 0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)


def create_arm(rotor_size):
    image = Image.new(mode='RGBA', size=rotor_size, color=BLACK)
    return image


def create_rotor(size, arm, arm_offset, radiuscircle, nb):
    center = size // 2
    image = Image.new(mode='RGBA', size=size)
    draw = ImageDraw.Draw(image)

    draw.ellipse([tuple(center - radiuscircle), tuple(center + radiuscircle)], fill=(0, 0, 0, 255), outline=None)

    top = Image.new(mode=image.mode, size=image.size)
    arm_topleft = center + Vec2(arm_offset, -arm.height // 2)
    top.paste(arm, box=arm_topleft)

    for i in range(nb):
        new_top = top.rotate(i * 360 / nb)
        image = Image.alpha_composite(image, new_top)
    return image


def create_rotor_sequence(rotor, rpm, fps, frames_start, frames_stop, outputdir):
    for i in range(frames_start, frames_stop):
        angle = 6 * rpm * i / fps
        frame_i = rotor.rotate(angle)
        frame_i.save(str(outputdir / 'frame{:08}.png'.format(i)), 'PNG')


def create_all(frames_start, frames_stop, rotor_size, arm_offset, radiuscircle, size, nb, rpm, fps, outputdir):
    arm = create_arm(rotor_size=rotor_size)
    rotor = create_rotor(size=size, arm=arm, arm_offset=arm_offset, radiuscircle=radiuscircle, nb=nb)
    create_rotor_sequence(rotor=rotor, rpm=rpm, fps=fps, frames_start=frames_start, frames_stop=frames_stop, outputdir=outputdir)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Generate a source rotor image sequence')
    parser.add_argument('--rpm', type=float, default=15, help='rpm of the rotor')
    parser.add_argument('--fps', type=float, default=60, help='fps of the fast camera')
    parser.add_argument('--width', type=int, default=1920, help='Width of the image')
    parser.add_argument('--height', type=int, default=1080, help='Height of the image')
    parser.add_argument('--frames', type=int, default=1080, help='Number of frames')
    parser.add_argument('--radiuscircle', type=int, default=75, help='Radius of the center circle')
    parser.add_argument('--rlength', type=int, default=400, help='Length of a rotor arm')
    parser.add_argument('--rwidth', type=int, default=75, help='Width of a rotor arm')
    parser.add_argument('--rnb', type=int, default=3, help='Number of arms of the rotor')
    parser.add_argument('--roffset', type=int, default=10, help='Offset of a rotor arm')
    parser.add_argument('--outputdir', type=Path, default=Path('frames'), help='Output folder')
    parser.add_argument('--parallel', type=int, default=8, help='Number of workers')

    args = parser.parse_args()
    kwargs = {
        'rpm': args.rpm,
        'fps': args.fps,
        'size': Vec2(args.width, args.height),
        'nb': args.rnb,
        'rotor_size': Vec2(args.rlength, args.rwidth),
        'arm_offset': args.roffset,
        'radiuscircle': args.radiuscircle,
        'outputdir': args.outputdir,
    }
    args.outputdir.mkdir(exist_ok=True)

    frames = args.frames

    res = []

    nb_processes = args.parallel
    pool = Pool(nb_processes)
    for i in range(nb_processes):
        start = i * frames // nb_processes
        stop = (i+1) * frames // nb_processes
        res_obj = pool.apply_async(create_all, args=(start, stop), kwds=kwargs)
        res.append(res_obj)

    for r in res:
        r.get()
